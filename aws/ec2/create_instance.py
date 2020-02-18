#!/usr/bin/env python3
import boto3

def new_instance(tag_value):
    try:
        print("\n-------------------------------------------------------------------------------------")
        print("             CREATING AN EC2 INSTANCE                                                ")
        print("-------------------------------------------------------------------------------------\n")
        ec2 = boto3.resource('ec2')
        instance = ec2.create_instances(

            # Amazon Linux 2 AMI (HVM), SSD Volume Type
            ImageId='ami-099a8245f5daa82bf',
            KeyName = 'assignment1-keypair',
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.nano',
            # SSH and HTTP
            SecurityGroupIds=['sg-0225d02f7158ea993'],
            # Tags
            TagSpecifications=[{'ResourceType': 'instance', 'Tags': [{'Key':'Name', 'Value':tag_value}]}],
            # Updates to the OS and install, enable and start the webserver apache
            UserData = ''' #!/bin/bash
                        yum update -y
                        yum install httpd -y
                        systemct1 enable httpd
                        systemctl start httpd
                        ''',
            )
        inst = instance[0]
        inst_id = instance[0].id
        print ("Created Instance ID: %s \n please wait while we get the instance up and running ....\n"% inst_id)
        inst.wait_until_running()
        inst.reload()
        print ("Thank you for waiting Instance ID: %s is now running \n"% inst_id)
        return inst
    except Exception as error:
            print (error)