#!/usr/bin/env python3

import subprocess
import aws.ec2.create_instance
import aws.ec2.security_group
import aws.s3.create_bucket
import aws.ec2.key_pair.keypair
import boto3
import datetime
import re
try:
    
    
    # removes any files already created called assignment1-keypair.pem
    subprocess.run('rm *.pem', shell=True)

    # Create a key pair
    key_name = aws.ec2.key_pair.keypair.setup_key_pair()

    # Get a security id 
    security_group_id = aws.ec2.security_group.setup_security_group()
    print(security_group_id)

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

    # Create an instance
    instance = aws.ec2.create_instance.new_instance(key_name, security_group_id, tag_value)
    print("Returned Instance ID: %s \n"% (instance))
    
    # # Create a bucket and put an image inside the bucket
    # bucket_details = aws.s3.create_bucket.new_bucket()
    # print("Returned Bucket Name: %s\n Returned File Name: %s \n"%(bucket_details[0], bucket_details[1]))

except Exception as error:
            print (error)