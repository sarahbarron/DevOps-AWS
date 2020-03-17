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
import logging

'''
Main program to be run to create an AWS EC2 instance, S3Bucket, Cloudwatch monitor, Cloudwatch Alarm,
upload a file to the S3Bucket and create a webpage and store it on the apache server on the EC2 instance
'''
def main():
    try:
        subprocess.run('clear')
        
        print("\nThis program will set up an: ")
        print("AWS EC2 instance with a cloudwatch alarm and cloudwatch monitoring, an S3 Bucket to hold an image and a webpage")
        print("\nYou can enter exit at any stage to exit the program early")
        print('\n--------------------------------------------------------------------------------------------------------')

        while True:

            print("\nWould you like to use DEFAULT values to setup the EC2 and S3 Bucket (y or n): ", end ='')
            user_input = input()
            checkForExit(user_input)    
            logging.info('User input: use default (y/n) : %s'%user_input)


            # If the user does not want to setup with default values
            if user_input == 'n' or user_input == 'N': 

                # Setup a key pair
                key_name = aws.ec2.keypair.setup_keypair_name()
                
                # setup a security group 
                security_group_id = aws.ec2.security_group.setup_security_group()
                
                # Look for input for a tag
                print('\nTAG: Enter a tag name (or press enter for default) : ', end ='')
                tag = input()
                checkForExit(tag)
                logging.info('User Input - Tag Name : %s '%tag)

                # If the user enters something set the tag to what they have entered
                if (len(tag)>0):
                    tag_value = tag

                # otherwise the user has pressed enter so use default value
                else:
                    tag_value = 'Assignment 1'

                # clear the console
                subprocess.run('clear')
                # set default to false initially
                default = "false"

                logging.info('Tag Value : %s'%tag_value)
                
                # exit the loop
                break
                
            # If the user chooses to use all default values
            # set up a default keypair, security group and tag
            if user_input == 'y' or user_input == 'Y': 

                key_name = aws.ec2.keypair.setup_default_keypair()
                
                security_group_id = aws.ec2.security_group.setup_default_security_group()
                
                tag_value = "Assignment 1"
                
                default = "true"
                break
            
        # Create an instance
        instance = aws.ec2.create_instance.new_instance(key_name, security_group_id, tag_value)
        public_ip_address = instance.public_ip_address
        
        # Create a bucket and put an image inside the bucket
        s3_bucket_name = aws.s3.create_bucket.setup_s3_bucket(default)
        
        # Setup webpage
        web_page_created = webpage.create_index_html_page(key_name, public_ip_address, s3_bucket_name)
        
       

        print('\n--------------------------------------------------------------------------------------------------------')
        print('             CLOUDWATCH')
        print('\n--------------------------------------------------------------------------------------------------------')
        print("\nALARM setup: this will take approximatley 2-3 minutes ...")
        
        # seleep for 2 mins to set up an alarm
        time.sleep(150)
        
        # Setup a cloudwatch monitoring alarm to delete an 
        # instance if it is not used within the previous hour
        aws.ec2.create_instance.setup_low_cpu_alarm(instance.id)
        

        print ("\nMONITOR your Instance at any time by running the following command in the root directory of the program:\n")
        print("./aws/cloudwatch/monitor.py %s" %instance.id)    

        time.sleep(5)      
        
        # Print messages to the user of where they can view the webpage
        if web_page_created:
            print("\nWEBPAGE: Use the following link to view index.html http://%s\n" %public_ip_address)
        else:
            print("Unfortunatley we were unable to build index.html on the apace server")
        

    except (Exception) as error:
        logging.error(error)
    except(KeyboardInterrupt):
        logging.error('Keyboard Interrupt')
        sys.exit("\n\nProgram exited by keyboard interupt")

if __name__ == '__main__':
    main()