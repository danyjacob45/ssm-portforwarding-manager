import socketserver
import subprocess
import boto3
from config import profiles

AWS_CONNECTED = True


def executeSSM(instance_id, platform, profile):
    if AWS_CONNECTED:
        #To find a free port to initiate the connection
        with socketserver.TCPServer(("localhost", 0), None) as s:
            connect_port = s.server_address[1]
        if platform == "windows":
            connect_parameters="portNumber=3389,localPortNumber=" + str(connect_port) + ""
        if platform == "linux":
            connect_parameters="portNumber=22,localPortNumber=" + str(connect_port) + ""
        aws_ssm_start = "aws ssm --profile "+ profile +" start-session --target " + instance_id + " --document-name AWS-StartPortForwardingSession --parameters " + connect_parameters
        #Subprocess is used because the above command does not exit until the session is terminated. So to start in background
        subprocess.Popen(aws_ssm_start)
        return connect_port


def setup():
    aws_profiles = profiles
    list_info = []
    filters = [
        {
            'Name': 'instance-state-name', 
            'Values': ['running']
        }
    ]
    for x in range(len(aws_profiles)):
        boto3.setup_default_session(profile_name=aws_profiles[x])
        ec2 = boto3.resource('ec2', region_name='ap-southeast-1')
        #Will be good if can do some error handling here
        for instance in ec2.instances.filter(Filters=filters):    
            if instance.platform == "windows":
                my_json = {"profile": aws_profiles[x], 'instance_id': instance.id, 'platform': "windows"}
            else:
                my_json = {"profile": aws_profiles[x], 'instance_id': instance.id, 'platform': "linux"}
                # print (instance.id , instance.platform)
            for tag in instance.tags:
                if tag["Key"] == "Name":
                    my_json['tag_name'] = tag["Value"]
            list_info.append(my_json)
    print(list_info)
    return list_info


def setupDummy():
    #This function for test purpose only
    #a = ["dltest", "dlprod"] #to be loaded from a config if possible
    list_info = []

    for x in range(len(a)):

        for instance in range(1,4):
            my_json = {}
            my_json["profile"] = a[x]
            my_json['instance_id'] = str(instance*1)+a[x]
            my_json['platform'] = str(instance*1)
            # print (instance.id , instance.platform)
            my_json['tag_name'] = "Value"

            list_info.append(my_json)
    print(list_info)
    return list_info
