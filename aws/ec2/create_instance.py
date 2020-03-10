#!/usr/bin/env python3
import boto3
import sys
def new_instance(key_name, security_group_id, tag_value):
    try:
        print('\n-------------------------------------------------------------------------------------')
        print('             CREATING AN EC2 INSTANCE                                                ')
        print('-------------------------------------------------------------------------------------\n')
        ec2 = boto3.resource('ec2')
        instance = ec2.create_instances(

            # Amazon Linux 2 AMI (HVM), SSD Volume Type
            ImageId='ami-099a8245f5daa82bf',
            KeyName = key_name,
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.nano',
            # Only use Monitoring if needed this will cost more to run
            Monitoring={'Enabled':True},
            # SSH and HTTP
            SecurityGroupIds=[security_group_id],
            # Tags
            TagSpecifications=[{'ResourceType': 'instance', 'Tags': [{'Key':'Name', 'Value':tag_value}]}],
            # Updates to the OS and install, enable and start the webserver apache
            UserData = '''#!/bin/bash
yum update -y
yum install httpd -y
systemctl enable httpd
systemctl start httpd
touch /var/www/html/index.html
sudo chmod 777 /var/www/html/index.html
                        ''',
            )
        inst = instance[0]
        inst_id = instance[0].id
        print ('Instance ID (Note: Save this ID as you will need it for monitoring): %s \n please wait while we get the instance up and running this could take a few minutes....\n'% inst_id)
        inst.wait_until_running()
        inst.reload()
        print ('Thank you for waiting Instance ID: %s is now running \n'% inst_id)
        return inst
    except (Exception) as error:
            print (error)
    except(KeyboardInterrupt):
        sys.exit("\n\nProgram exited by keyboard interupt")