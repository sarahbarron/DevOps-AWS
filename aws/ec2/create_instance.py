#!/usr/bin/env python3
import boto3
import sys
import subprocess
import socket
import time
import logging


logging.basicConfig(level=logging.DEBUG, filename="mylog.log", filemode="w")

'''

Function to create a new EC2 Instance 
Install an apache server onto the instance
Create and index.html page and store it at /var/www/html/index.html
Set the instance up with an alarm that deletes the instance when it becomes inactive

'''
def new_instance(key_name, security_group_id, tag_value):

    try:
        print('\n--------------------------------------------------------------------------------------------------------')
        print('             CREATING AN EC2 INSTANCE')
        print('\n--------------------------------------------------------------------------------------------------------')
        
        ec2 = boto3.resource('ec2')

        # Create an EC2 Instance
        instance = ec2.create_instances(
            # Amazon Linux 2 AMI (HVM), SSD Volume Type
            ImageId='ami-04d5cc9b88f9d1d39',
            KeyName = key_name,
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.nano',
            Monitoring={'Enabled':True},
            # SSH and HTTP
            SecurityGroupIds=[security_group_id],
            # Tags
            TagSpecifications=[{'ResourceType': 'instance', 'Tags': [{'Key':'Name', 'Value':tag_value}]}],
            # Updates to the OS and install, enable and start the webserver apache with index.html created on the server
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
        
        logging.info('EC2 Instance Created : %s'%inst_id)
        
        print("\nCreating a new EC2 Instance with:\nKEY PAIR: %s,\nSECURITY GROUP: %s,\nTAG: %s." %(key_name, security_group_id, tag_value ))
        print("\nPlease be patient as we create your EC2 instance. This could take a few minutes .....")
        
        # wait for the instance to be running
        inst.wait_until_running()
        
        inst.reload()
        
        logging.info('EC2 instance %s running'%inst_id)
        print ('Thank you for waiting Instance ID: %s is now running \n'% inst_id)
        
        return inst
    
    except (Exception) as error:
            logging.error(error)
    except(KeyboardInterrupt):
        sys.exit("\n\nProgram exited by keyboard interupt")


'''
Setup An instance with an alarm
If the CPU Utilization goes below a threshold of 1 for a period of 1 hour
Terminate the instance
'''

def setup_low_cpu_alarm(instid):
    try:

        cloudwatch = boto3.resource('cloudwatch')
        
        # Get metrics for CPU utilisation
        metric_iterator = cloudwatch.metrics.filter(Namespace='AWS/EC2',
                                                MetricName='CPUUtilization',
                                                Dimensions=[{'Name':'InstanceId', 'Value': instid}])

        logging.info('A list of Cloudwatch metrics returned for CPUUtilization')

        # Extract the metric for the instance we want to use
        metric = list(metric_iterator)[0]    

        logging.info('Extracted The cloudwatch metric we want to use')
        
        # put an alarm on our instance 
        metric.put_alarm(
            AlarmName = 'Low_CPU_Utilisation',
            AlarmDescription= 'Delete EC2 Instance when not in use',
            AlarmActions=['arn:aws:automate:eu-west-1:ec2:terminate'],
            MetricName='CPUUtilization',
            Namespace='AWS/EC2',
            Statistic='Average',
            Dimensions=[{'Name':'InstanceId', 'Value': instid}],
            Period=300,
            EvaluationPeriods=12,
            Threshold=1.0,
            ComparisonOperator='LessThanThreshold')
        
        metric.reload()

        logging.info('Alarm put on the metric to monitor inactive CPU utilization')
        print("Low CPU Utilization Alarm created")
    
    except (Exception) as error:
            logging.error(error)
    except(KeyboardInterrupt):
        sys.exit("\n\nProgram exited by keyboard interupt")
        