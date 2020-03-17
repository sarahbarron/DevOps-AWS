#!/usr/bin/env python3

import subprocess
import boto3
import time
import sys
import logging

'''
Build an index.html web page to show an image, Availability Zone, Public DNS
and local IPV4 Address
'''

def create_index_html_page(key_name, public_ip_address, bucket_name):

    try:
        print('\n--------------------------------------------------------------------------------------------------------')
        print('             CREATE WEBPAGE')
        print('\n--------------------------------------------------------------------------------------------------------')

        # image tag
        image_html = "\'echo \"<img src=\"https://%s.s3-eu-west-1.amazonaws.com/image.jpg\" \
            alt=\"Image from s3 bucket unavailable\">\" >> index.html\'" %bucket_name

        # title, body, header and opening div
        subprocess.run("ssh -o StrictHostKeyChecking=no -i %s.pem ec2-user@%s \
            'echo \"<html>\
                <title>DevOps Assignment 1</title>\
                    <body>\
                        <h1>Developer Operations Assingment 1 - AWS EC2 and S3 </h1>\
                            <div>\" \
                                > index.html'" %(key_name, public_ip_address), shell=True)
        
        logging.info('start of index.html page build ...')


        print("Please wait while we try to build your index.html page....")
        
        # Add the image
        subprocess.run('ssh -o StrictHostKeyChecking=no -i %s.pem ec2-user@%s %s'  %(key_name, public_ip_address, image_html), shell=True)
    
        logging.info('image.jpg added')

        # Availability Zone tag
        subprocess.run("ssh -o StrictHostKeyChecking=no -i %s.pem ec2-user@%s \
            'echo \"<H2> Availablility Zone: \" >> index.html'" %(key_name, public_ip_address), shell=True)
    
        logging.info('Availability zone tag added')

        # Availability Zone value
        subprocess.run("ssh -o StrictHostKeyChecking=no -i %s.pem ec2-user@%s \
            'curl --silent http://169.254.169.254/latest/meta-data/placement/availability-zone >> index.html'" %(key_name, public_ip_address) , shell=True)
    
        logging.info('Availability zone value added')

        # Local IPV4 tag
        subprocess.run("ssh -o StrictHostKeyChecking=no -i %s.pem ec2-user@%s \
            'echo \"<H2>Local IPV4: \" >> index.html'" %(key_name, public_ip_address), shell=True)
    
        logging.info('Local IPV4 tag added ')

        # Local IPV4 value
        subprocess.run("ssh -o StrictHostKeyChecking=no -i %s.pem ec2-user@%s \
            'curl --silent http://169.254.169.254/latest/meta-data/local-ipv4 >> index.html'" %(key_name, public_ip_address) , shell=True)

        logging.info('Local IPV4 value added ')

        # Public DNS tag
        subprocess.run("ssh -o StrictHostKeyChecking=no -i %s.pem ec2-user@%s \
            'echo \"<H2>Public DNS: \" >> index.html'"%(key_name, public_ip_address), shell=True)
        
        logging.info('Public DNS tag added')

        # Public DNS value
        subprocess.run("ssh -o StrictHostKeyChecking=no -i %s.pem ec2-user@%s \
            'curl --silent http://169.254.169.254/latest/meta-data/public-hostname >> index.html'"%(key_name, public_ip_address) , shell=True)

        logging.info('Public DNS value added')

        # wait for the apache server to be up and running
        apache_not_running = True
        count = 0
        logging.info('Attempt to connect to the Apache server....')

        while True:
            count += 1

            # checks to see if apache is on the list 
            apache_num = subprocess.check_output("ssh -o StrictHostKeyChecking=no -i %s.pem ec2-user@%s 'ps -eaf | grep apache | wc -l'" %(key_name, public_ip_address) \
                , shell=True, universal_newlines=True)

            # if the return is equal to 2\n then apache is not yet running
            if apache_num == '2\n':
                print("Connecting to server please wait this can take a few minutes ......")
            # otherwise apache is up and running so exit
            else:
                break
            # only check 12 times if no response after 60 seconds exit
            if count > 12:
                break
            time.sleep(5)
        
        
        # If after 1 minute apache server wasnt detected exit the program
        if apache_num == '2\n':
            
            logging.info('Could not connect to the apache server. sys.exit(1)')
            print("Sorry we could not connect with the server")
            
            sys.exit(1)


        # Otherwise the apache server was detected copy the index.html page to /var/www/html/index.html 
        else: 
            subprocess.run("ssh -o StrictHostKeyChecking=no -i %s.pem ec2-user@%s 'cp -f index.html /var/www/html/index.html'" %(key_name, public_ip_address) , shell=True)
            
            logging.info('index.html copied to /var/www/html/ on the apache server')
            
            print("\nindex.html created and can be viewed at the following link index.html http://%s" %public_ip_address)
            
            # If you want to automatically fireup firefox with the webpage uncomment the below command
            # subprocess.run(["firefox", "http://%s"%public_ip_address])

        return(True)

    except (Exception, KeyboardInterrupt) as error:
        logging.error(error)
        return(False)
