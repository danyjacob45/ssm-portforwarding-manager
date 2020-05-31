# AWS SSM Session Manager Tool for Port Forwarding

This tool can be used to manage your SSM Port forwarding sessions from the browser.


# What problem does this solve?

SSM Session Manager Port Forwarding is great tool that can be used get rid of your bastion hosts or VPN servers to manage your private instances. However, when you have to manage many instances that are spread over multiple AWS accounts, it will become  a difficult task to remember their instance ids, and creating sessions based on some available free ports. Moreover, in windows, you probably need to open multiple terminal windows to open tunnels to multiple servers. 
This simple app will do the following this for you:

 1. Query the running instances in all your accounts specified and display it in a tabular format with an option for you to connect.
 2. Once you click connect, depending on the OS type of the instance, it will either create a tunnel to port 22 or 3389 to the instance, and display the local port number. So you can just use the local port number to connect.

So, no need to login to the EC2 console and get the information, no need to find free ports, and so on. 

## How to use

 1. Download the repo
 2. Modify the variable 'profiles' in the config.py file to include your AWS Config profiles to be used (Those found in ~/.aws/config)
 3. Run app.py
 4. Open your browser, and go to http://127.0.0.1:5000/

## Pre-Requisites

 1. Python3, boto3 and some other modules. (Refer to requirements.txt)
 2. AWS CLI installed and configured with profiles to use
 3. AWS Session Manager [plugin](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html) installed
 4. Your instances should have SSM agent installed and the IAM role should have permissions to be able to manage by SSM
 5. Your profiles should have the required IAM permissions

## Screenshots

 1. [HomePage](https://imgur.com/a/atoS8h2?raw=true)
 2. [After Connection](https://imgur.com/a/ruHWAyk)

## Known Issues

 1. Not able to handle SSM timeouts
 2. Not pretty - Just plain HTML
 3. Error handling is not great


