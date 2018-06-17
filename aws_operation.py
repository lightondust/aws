import subprocess
from AwsResource import AwsResource
from AwsInfo import AwsInfo
import sys

operation = sys.argv[1]

if operation in ["getInfo"]:
    awsInfo = AwsInfo().get_instance_info(print_it=True)
    
elif operation in ["start", "stop", "restart", "login"]:
    name = sys.argv[2]
    resource = AwsResource(name)

    if operation == "start":
        ip_address = resource.start_instance()
        print("started instance {} with ip_address {}".format(name, ip_address))

    if operation == "stop":
        if resource.stop_instance():
            print("stopped instance {}".format(name))

    if operation == "restart":
        resource.restart_instance()

    if operation == "login":
        arg = ["sh","awsLogin.sh"]
        ip_address = resource.get_ip_address()
        arg.append(ip_address)
        if len(sys.argv) > 3:
            user = sys.argv[3]
            if user == "ubuntu":
                arg.append(user)
        subprocess.run(arg)

elif operation in ["startas"]:
    inst_type = sys.argv[2]
    name = sys.argv[3]

    resource = AwsResource(name)

    if operation == "startas":
        resource.stop_instance()
        resource.change_instance_type(inst_type)
        resource.start_instance()
        print("started instance {} as {}".format(name, inst_type))

elif operation in ["regist", "attach", "detach", "assign"]:
    """
    regist:ターゲットグループ
    attach/detach:ebsボリューム
    assign:セキュリティグループ
    """
    instance = sys.argv[2]
    target = sys.argv[3]

    resource = AwsResource(instance)

    if operation == "regist":
        if len(sys.argv) <= 4:
            port = 8888
        resource.regist_to_target_group(target, port)
    
    elif operation == "attach":
        resource.attach_volume(target)
    elif operation == "detach":
        resource.detach_volume(target)

    elif operation == "assign":
        resource.assign_security_group(target)

