import socketserver
import subprocess

import boto3

AWS_CONNECTED = True


def executeSSM(instance_id, platform, profile, port=0):
    if AWS_CONNECTED:
        with socketserver.TCPServer(("localhost", 0), None) as s:
            free_port = s.server_address[1]
        if platform == "windows":
            connect_parameters="portNumber=3389,localPortNumber=" + str(free_port) + ""
        if platform == "linux":
            connect_parameters="portNumber=22,localPortNumber=" + str(free_port) + ""
        aws_ssm_start = "aws ssm --profile "+ profile +" start-session --target " + instance_id + " --document-name AWS-StartPortForwardingSession --parameters " + connect_parameters
        subprocess.Popen(aws_ssm_start)
        return free_port


def setup():
    a = ["dltest", "dlprod"] #to be loaded from a config if possible
    list_info = []
    for x in range(len(a)):
        boto3.setup_default_session(profile_name=a[x])
        ec2 = boto3.resource('ec2', region_name='ap-southeast-1')
        for instance in ec2.instances.all():
            my_json = {"profile": a[x], 'instance_id': instance.id, 'platform': instance.platform}
            # print (instance.id , instance.platform)
            for tag in instance.tags:
                if tag["Key"] == "Name":
                    my_json['tag_name'] = tag["Value"]
            list_info.append(my_json)
    print(list_info)
    return list_info


def setupDummy():
    a = ["dltest", "dlprod"] #to be loaded from a config if possible
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
