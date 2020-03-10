#!/usr/bin/env python3

import subprocess
import boto3
import time
import sys
'''

Author: Sarah Barron
College: Waterford Institute of Technology
Course: HDip Computer Science
Module: Developer Operations
Assingment 1.

Create the index.html web page

'''

def create_index_html_page(key_name, public_ip_address, bucket_name):

    try:
        print('\n-------------------------------------------------------------------------------------')
        print('             CREATE WEBPAGE                                                            ')
        print('-------------------------------------------------------------------------------------\n')

        image_html = "\'echo \"<img src=\"https://%s.s3-eu-west-1.amazonaws.com/image.jpg\" \
            alt=\"Image from s3 bucket unavailable\">\" >> index.html\'" %bucket_name

    
        subprocess.run("ssh -o StrictHostKeyChecking=no -i %s.pem ec2-user@%s \
            'echo \"<html>\
                <title>DevOps Assignment 1</title>\
                    <body>\
                        <h1>Developer Operations Assingment 1 - AWS EC2 and S3 </h1>\
                            <div>\" \
                                > index.html'" %(key_name, public_ip_address), shell=True)
        print("Please wait while we try to build your index.html page....")
        subprocess.run('ssh -o StrictHostKeyChecking=no -i %s.pem ec2-user@%s %s'  %(key_name, public_ip_address, image_html), shell=True)
    
        subprocess.run("ssh -o StrictHostKeyChecking=no -i %s.pem ec2-user@%s \
            'echo \"<H2> Availablility Zone: \" >> index.html'" %(key_name, public_ip_address), shell=True)
    
        subprocess.run("ssh -o StrictHostKeyChecking=no -i %s.pem ec2-user@%s \
            'curl --silent http://169.254.169.254/latest/meta-data/placement/availability-zone >> index.html'" %(key_name, public_ip_address) , shell=True)
    
        subprocess.run("ssh -o StrictHostKeyChecking=no -i %s.pem ec2-user@%s \
            'echo \"<H2>Local IPV4: \" >> index.html'" %(key_name, public_ip_address), shell=True)
    
        subprocess.run("ssh -o StrictHostKeyChecking=no -i %s.pem ec2-user@%s \
            'curl --silent http://169.254.169.254/latest/meta-data/local-ipv4 >> index.html'" %(key_name, public_ip_address) , shell=True)

        subprocess.run("ssh -o StrictHostKeyChecking=no -i %s.pem ec2-user@%s \
            'echo \"<H2>Public DNS: \" >> index.html'"%(key_name, public_ip_address), shell=True)

        subprocess.run("ssh -o StrictHostKeyChecking=no -i %s.pem ec2-user@%s \
            'curl --silent http://169.254.169.254/latest/meta-data/public-hostname >> index.html'"%(key_name, public_ip_address) , shell=True)

        apache_not_running = True
        count = 0
        while apache_not_running:
            count += 1
            apache_num = subprocess.check_output("ssh -o StrictHostKeyChecking=no -i %s.pem ec2-user@%s 'ps -eaf | grep apache | wc -l'" %(key_name, public_ip_address) \
                , shell=True, universal_newlines=True)
            
            apache_not_running = False
            if apache_num == '2\n':
                print("Connecting to server please wait this can take a few minutes ......")
                apache_not_running = True
            else:
                apache_not_running = False
            if count > 10:
                apache_not_running = False
            time.sleep(5)

        if apache_num == '2\n':
            print("Sorry we could not connect with the server")
            sys.exit(1)
         
        else: 
            subprocess.run("ssh -o StrictHostKeyChecking=no -i %s.pem ec2-user@%s 'cp -f index.html /var/www/html/index.html'" %(key_name, public_ip_address) , shell=True)
            subprocess.run(["xdg-open", "http://%s"%public_ip_address])
               
              
    except (Exception, KeyboardInterrupt) as error:
        if error == "ssh: connect to host %s port 22: Connection refused" %public_ip_address:
            print(error)
            sys.exit(1)

        print (error)

