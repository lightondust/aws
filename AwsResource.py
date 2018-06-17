import boto3
import os
import json
from AwsInfo import AwsInfo

class AwsResource:
	"""
	個別のリソースの操作
	"""   	
	def __init__(self, instance_name):
		self.instance_name = instance_name
		self.instance_info = AwsInfo().get_instance_info()
		self.instance_id = self.instance_info[self.instance_name]["id"]
		self.ec2r = boto3.resource("ec2")
		self.instance = self.ec2r.Instance(self.instance_id)

	def start_instance(self):
		"""
		インスタンス起動
		"""  		
		self.instance.start()
		self.instance.wait_until_running()
		self.ip_address = self.instance.public_ip_address
		return self.ip_address

	def stop_instance(self):
		"""
		インスタンス停止
		"""
		self.instance.stop()
		self.instance.wait_until_stopped()
		self.change_instance_type("t2.micro")
		return True

	def change_instance_type(self, inst_type):
		"""
		インスタンスタイプ変更
		"""
		self.instance.modify_attribute(InstanceType={"Value": inst_type})

	def restart_instance(self):
		"""
		インスタンス再起動
		"""
		self.stop_instance()
		return self.start_instance()

	def get_ip_address(self):
		"""
		インスタンスipアドレスを返す
		"""
		return self.instance.public_ip_address
	
	def regist_to_target_group(self, target_name, port):
		"""
		selfインスタンスを与えられたtarget_groupに登録する
		"""  		
		elb = boto3.client("elbv2")
		elb.register_targets(TargetGroupArn=AwsInfo().get_target_info(target_name)["arn"], Targets=[{
			'Id' : self.instance_id, 'Port': port 
		}])

	def attach_volume(self, volume_name, device_name="xvdf"):
		inst_id = self.instance_id
		volume_id = AwsInfo().get_ebs_volume_information(volume_name)["id"]
		ec2r = boto3.resource("ec2")
		volume = ec2r.Volume(volume_id)
		volume.attach_to_instance(Device=device_name, InstanceId=inst_id)

	def detach_volume(self, volume_name, device_name="xvdf"):
		inst_id = self.instance_id
		volume_id = AwsInfo().get_ebs_volume_information(volume_name)["id"]
		ec2r = boto3.resource("ec2")
		volume = ec2r.Volume(volume_id)
		volume.detach_from_instance(Device=device_name, InstanceId=inst_id)

	def assign_security_group(self, group_name):
		inst_id = self.instance_id
		ec2c = boto3.client("ec2")
		group_id = ec2c.describe_security_groups(GroupNames=[group_name])["SecurityGroups"][0]["GroupId"]
		ec2c.modify_instance_attribute(InstanceId = inst_id, Groups=[group_id])

