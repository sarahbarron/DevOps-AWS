#!/usr/bin/env python3

import subprocess
import boto3
import time
'''

Author: Sarah Barron
College: Waterford Institute of Technology
Course: HDip Computer Science
Module: Developer Operations
Assingment 1.

Create the index.html web page

'''

def create_index_html_page(key_name, public_ip_address, bucket_name):

    print("keyname: %s" %key_name)
    print("public ip: %s" %public_ip_address)
    print("bucket_name: %s" %bucket_name)
    

    image_html = "\'echo \"<img src=\"https://%s.s3-eu-west-1.amazonaws.com/image.jpg\" \
        alt=\"s3 bucket_name\">\" >> index.html\'" %bucket_name

   
    subprocess.run("ssh -o StrictHostKeyChecking=no -i %s.pem ec2-user@%s \
        'echo \"<html>\
            <title>DevOps Assignment 1</title>\
                <body>\
                    <h1>Developer Operations Assingment 1 - AWS EC2 and S3 </h1>\
                        <div>\" \
                            > index.html'" %(key_name, public_ip_address), shell=True)
    print("one")
    subprocess.run('ssh -o StrictHostKeyChecking=no -i %s.pem ec2-user@%s %s'  %(key_name, public_ip_address, image_html), shell=True)
    print("two")
    subprocess.run("ssh -o StrictHostKeyChecking=no -i %s.pem ec2-user@%s \
        'echo \"<H2> Availablility Zone: \" >> index.html'" %(key_name, public_ip_address), shell=True)
    print("three")
    subprocess.run("ssh -o StrictHostKeyChecking=no -i %s.pem ec2-user@%s \
        'curl --silent http://169.254.169.254/latest/meta-data/placement/availability-zone >> index.html'" %(key_name, public_ip_address) , shell=True)
    print("four")
    subprocess.run("ssh -o StrictHostKeyChecking=no -i %s.pem ec2-user@%s \
        'echo \"<H2>Local IPV4: \" >> index.html'" %(key_name, public_ip_address), shell=True)
    print("five")
    subprocess.run("ssh -o StrictHostKeyChecking=no -i %s.pem ec2-user@%s \
        'curl --silent http://169.254.169.254/latest/meta-data/local-ipv4 >> index.html'" %(key_name, public_ip_address) , shell=True)
    print("six")
    subprocess.run("ssh -o StrictHostKeyChecking=no -i %s.pem ec2-user@%s \
        'echo \"<H2>Public DNS: \" >> index.html'"%(key_name, public_ip_address), shell=True)
    print("seven")
    subprocess.run("ssh -o StrictHostKeyChecking=no -i %s.pem ec2-user@%s \
        'curl --silent http://169.254.169.254/latest/meta-data/public-hostname >> index.html'"%(key_name, public_ip_address) , shell=True)
    print("eight")
    time.sleep(60)
    subprocess.run("ssh -t -o StrictHostKeyChecking=no -i %s.pem ec2-user@%s 'cp -f index.html /var/www/html/index.html'" %(key_name, public_ip_address) , shell=True)
    print("nine")
    
    subprocess.run(["firefox", "http://%s"%public_ip_address])