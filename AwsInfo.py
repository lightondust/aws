import boto3
import json

class AwsInfo:
    """
    リソースの情報を取得する
    """
    def __init__(self):
        self.get_instance_info()

    def get_name_from_tags(self, inst):
        if inst.tags:
            for tag in inst.tags:
                if "Name" == tag["Key"]:
                    return tag["Value"]
                    
    def get_instance_info(self, print_it=False):
        """
        ec2インスタンスの一覧情報を取得する
        インスタンス名をキーにインタンスid、インスタンス状態、インスタンス種類を格納
        """
        ec2r = boto3.resource("ec2")
        info = {}
        for inst in ec2r.instances.all():
            try:
                name = self.get_name_from_tags(inst)
                inst_id = inst.id
                inst_state = inst.state["Name"]
                inst_type = inst.instance_type
                if print_it:
                    print("{}, {}, {}, {}".format(name, inst_state, inst_id, inst_type))
                info[name] = {"id": inst_id, "status": inst_state, "type": inst_type}
            except Exception as e:
                print(e)
                print(inst)
        self.instance_info = info 
        return info
	
    def get_target_info(self, target_name):
        """
        ターゲットグループ名を与えてarnを取得
        """
        info = {}
        elb = boto3.client("elbv2")
        info["arn"] = elb.describe_target_groups(Names=[target_name])["TargetGroups"][0]["TargetGroupArn"]
        info["name"] = target_name
        return info
    
    def get_ebs_volume_information(self, name):
        info = {}
        ec2c = boto3.client("ec2")
        volume_info = ec2c.describe_volumes()["Volumes"]
        for vol in volume_info:
            tags = vol["Tags"]
            for pair in tags:
                if pair["Key"] == "Name":
                    if pair["Value"] == name:
                        info["name"] = name
                        info["id"] = vol["VolumeId"]
                        return info 

