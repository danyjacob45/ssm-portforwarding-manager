import boto3
import socketserver

AWS_CONNECTED = False


def executeSSM( instance_id, platform, profile,port=0):
    if AWS_CONNECTED:
        with socketserver.TCPServer(("localhost", 0), None) as s:
            free_port = s.server_address[1]
        boto3.setup_default_session(profile_name=profile)
        client = boto3.client('ssm', region_name='ap-southeast-1')
        if platform == "windows":
            response = client.start_session(
                Target=instance_id,
                DocumentName='AWS-StartPortForwardingSession',
                Parameters={
                    'portNumber': [
                        '3389',
                    ],
                    'localPortNumber': [
                        str(free_port),
                    ]
                }
            )
        if platform == "linux":
            response = client.start_session(
                Target=instance_id,
                DocumentName='AWS-StartPortForwardingSession',
                Parameters={
                    'portNumber': [
                        '22',
                    ],
                    'localPortNumber': [
                        str(free_port),
                    ]
                }
            )
        print (response)
        print (free_port)
        return response,free_port

def setup():
    a = ["dltest", "dlprod"] #to be loaded from a config if possible
    list_info = []
    my_json = {}
    for i in a:
        my_json["profile"] = i
        boto3.setup_default_session(profile_name=i)
        ec2 = boto3.resource('ec2', region_name='ap-southeast-1')
        # ec2.describe_instances(Filters={"tag:environment" :   Env, "tag:role" : Role})
        for instance in ec2.instances.all():
            my_json['instance_id'] = instance.id
            my_json['platform'] = instance.platform
            # print (instance.id , instance.platform)
            for tag in instance.tags:
                if tag["Key"] == "Name":
                    my_json['tag_tame'] = tag["Value"]
        list_info.append(my_json)
    print(list_info)
    return list_info


executeSSM("i-01f747b2283fde7d3","linux","network")
