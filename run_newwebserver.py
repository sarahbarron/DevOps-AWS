#!/usr/bin/env python3

import subprocess
import aws.ec2.create_instance
import aws.ec2.security_group
import aws.s3.create_bucket
import aws.ec2.keypair
import boto3
import datetime
import re
try:
    #subprocess.run('clear')
    # Setup a key pair
    key_name = aws.ec2.keypair.setup_keypair_name()
    #subprocess.run('clear')
    # setup a security group 
    security_group_id = aws.ec2.security_group.setup_security_group()
   
    #subprocess.run('clear')
    print("\n-------------------------------------------------------------------------------------")
    print("  SETUP TAG VALUE")
    print("\n-------------------------------------------------------------------------------------")
    # Look for input for a tag
    print("\nPlease enter a value you would like to tag your instance with \n \
        (or press enter for default value of Assignment 1) : ", end =''),
    tag = input()
    if (len(tag)>0):
        tag_value = tag
    else:
        tag_value = "Assignment 1"
    #subprocess.run('clear')
    # Create an instance
    instance = aws.ec2.create_instance.new_instance(key_name, security_group_id, tag_value)
    
    #subprocess.run('clear')
    # # Create a bucket and put an image inside the bucket
    # bucket_details = aws.s3.create_bucket.new_bucket()
    # print("Returned Bucket Name: %s\n Returned File Name: %s \n"%(bucket_details[0], bucket_details[1]))

except Exception as error:
            print (error)