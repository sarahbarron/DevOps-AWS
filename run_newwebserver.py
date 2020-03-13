#!/usr/bin/env python3

import subprocess
import aws.ec2.create_instance
import aws.ec2.security_group
import aws.s3.create_bucket
import aws.ec2.keypair
import boto3
import datetime
import re
import webpage
from check_for_exit import checkForExit
import sys
import time

try:
    subprocess.run('clear')
    
    print("This program will set up an: ")
    print("AWS EC2 and S3 Bucket")
    print("\n You can enter exit at any stage to exit the program early")
    print('\n-------------------------------------------------------------------------------------')

    invalid_input = True

    while(invalid_input):
        print("\n Would you like to use the default values to setup the EC2 and S3 Bucket (y or n): ", end='')
        user_input = input()
        checkForExit(user_input)    
        if user_input == 'n' or user_input == 'N': 
            
            # Setup a key pair
            key_name = aws.ec2.keypair.setup_keypair_name()

            # setup a security group 
            security_group_id = aws.ec2.security_group.setup_security_group()
        
            print('\n-------------------------------------------------------------------------------------')
            print('  SETUP TAG VALUE')
            print('\n-------------------------------------------------------------------------------------')
            print('\nYOU CAN ENTER EXIT AT ANY STAGE TO EXIT THE PROGRAM\n')
            # Look for input for a tag
            print('\nPlease enter a value you would like to tag your instance with \n \
                (or press enter for default value of Assignment 1) : ', end =''),
            tag = input()
            checkForExit(tag)

            if (len(tag)>0):
                tag_value = tag
            else:
                tag_value = 'Assignment 1'
            subprocess.run('clear')
            
            # exit the loop
            invalid_input = False
            default = "false"
        
        if user_input == 'y' or user_input == 'Y': 
            key_name = aws.ec2.keypair.setup_default_keypair()
            security_group_id = aws.ec2.security_group.setup_default_security_group()
            tag_value = "Assignment 1"
            default = "true"
            invalid_input = False
        
    # Create an instance
    instance = aws.ec2.create_instance.new_instance(key_name, security_group_id, tag_value)
    public_ip_address = instance.public_ip_address
    print("Public IP Address: %s" %public_ip_address)

    # Create a bucket and put an image inside the bucket
    bucket_details = aws.s3.create_bucket.setup_s3_bucket(default)
    webpage.create_index_html_page(key_name, public_ip_address, bucket_details)
    # sleep for 2 mins to set up an alarm
    print("Please wait for 2 minutes while we set up an alarm to terminate inactive instances ...")
    time.sleep(150)
    aws.ec2.create_instance.setup_low_cpu_alarm(instance.id)
    
    print("Would you like to wait for 5 minutes for monitoring to start (y or n or exit): ", end='')
    user_input = input()
    checkForExit(user_input)

    invalid_input = True
    while invalid_input:
        if user_input == 'y' or user_input == 'Y':
            print('Great come back in 5 minutes to see your monitor readings .....')
            print('\nWhile we are waiting for monitor results to be returned we will create your webpage')
            time.sleep(260)
            invalid_input= False

        if user_input == 'n' or user_input == 'N':
            print ("\nYou can monitor your Instance at any time using your Instance ID: %s"%instance.id)
            print("by running the following command in the root directory of the program:\n")
            print("./monitor.py %s" %instance.id)    
               
            invalid_input = False
    

except (Exception) as error:
            print (error)
except(KeyboardInterrupt):
        sys.exit("\n\nProgram exited by keyboard interupt")
