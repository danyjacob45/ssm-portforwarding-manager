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


executeSSM("i-01f747b2283fde7d3","linux","network")
