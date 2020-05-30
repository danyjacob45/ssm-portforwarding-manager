import boto3
import socketserver
import websocket
AWS_CONNECTED = False



def executeSSM(instance_id, platform, profile, port=0):
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

        ws = websocket.WebSocket()
        ws.connect("ws://example.com/websocket", http_proxy_host="proxy_host_name", http_proxy_port=3128)

        print(response)
        print(free_port)
        return response, free_port


def setup():
    a = ["dltest", "dlprod"]  # to be loaded from a config if possible
    list_info = []
    for x in range(len(a)):
        boto3.setup_default_session(profile_name=a[x])
        ec2 = boto3.resource('ec2', region_name='ap-southeast-1')
        for instance in ec2.instances.all():
            my_json = {"profile": a[x], 'instance_id': instance.id, 'platform': instance.platform}
            # print (instance.id , instance.platform)
            for tag in instance.tags:
                if tag["Key"] == "Name":
                    my_json['tag_tame'] = tag["Value"]
            list_info.append(my_json)
    print(list_info)
    return list_info


def setupDummy():
    a = ["dltest", "dlprod"]  # to be loaded from a config if possible
    list_info = []
    my_json = {}
    for x in range(len(a)):
        for instance in range(2):
            my_json["profile"] = a[x]
            my_json['instance_id'] = instance * 1
            my_json['platform'] = instance * 1
            # print (instance.id , instance.platform)
            my_json['tag_tame'] = "Value"
            list_info.append(my_json)
    print(list_info)
    return list_info


executeSSM("i-01f747b2283fde7d3", "linux", "network")
