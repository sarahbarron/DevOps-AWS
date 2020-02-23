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

try:
    subprocess.run('clear')
    # Setup a key pair
    key_name = aws.ec2.keypair.setup_keypair_name()
    #subprocess.run("sudo chmod 400 %s.pem" %key_name)
    
    # setup a security group 
    security_group_id = aws.ec2.security_group.setup_security_group()
   
    print('\n-------------------------------------------------------------------------------------')
    print('  SETUP TAG VALUE')
    print('\n-------------------------------------------------------------------------------------')
    # Look for input for a tag
    print('\nPlease enter a value you would like to tag your instance with \n \
        (or press enter for default value of Assignment 1) : ', end =''),
    tag = input()
    if (len(tag)>0):
        tag_value = tag
    else:
        tag_value = 'Assignment 1'
    subprocess.run('clear')
    
    # Create an instance
    instance = aws.ec2.create_instance.new_instance(key_name, security_group_id, tag_value)
    public_ip_address = instance.public_ip_address
    print("Public IP Address: %s" %public_ip_address)
    # Create a bucket and put an image inside the bucket
    bucket_details = aws.s3.create_bucket.setup_s3_bucket()
    print(bucket_details)

    webpage.create_index_html_page(key_name, public_ip_address, bucket_details)

except Exception as error:
            print (error)