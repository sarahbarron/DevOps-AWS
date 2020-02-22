#!/usr/bin/env python3

import subprocess

'''

Author: Sarah Barron
College: Waterford Institute of Technology
Course: HDip Computer Science
Module: Developer Operations
Assingment 1.

Create the index.html web page

'''
bucket = "assignment1-2020-02-22-01-49-50"
image_html = "\'echo \"<img src=\"https://%s.s3-eu-west-1.amazonaws.com/image.jpg\" alt=\"s3 bucket\">\" >> /var/www/html/index.html\'" %bucket

print(image_html)
public_ip = '34.241.90.222'


#subprocess.run("ssh -o StrictHostKeyChecking=no -i key_pair.pem ec2-user@%s 'touch /var/www/html/index.html'"%public_ip, shell=True)
#subprocess.run("ssh -o StrictHostKeyChecking=no -i key_pair.pem ec2-user@%s 'chmod 777 /var/www/html/index.html"%public_ip, shell=True)
subprocess.run("ssh -o StrictHostKeyChecking=no -i key_pair.pem ec2-user@%s \
    'echo \"<html>\
        <title>DevOps Assignment 1</title>\
            <body>\
                <h1>Developer Operations Assingment 1 - AWS EC2 and S3 </h1>\
                    <div>\" \
                        > /var/www/html/index.html'"%public_ip, shell=True)

subprocess.run('ssh -o StrictHostKeyChecking=no -i key_pair.pem ec2-user@%s %s'  %(public_ip, image_html), shell=True)

subprocess.run("ssh -o StrictHostKeyChecking=no -i key_pair.pem ec2-user@%s \
    'echo \"<H2> Availablility Zone: \" >> /var/www/html/index.html'"%public_ip, shell=True)
subprocess.run("ssh -o StrictHostKeyChecking=no -i key_pair.pem ec2-user@34.241.90.222 \
    'curl --silent http://169.254.169.254/latest/meta-data/placement/availability-zone >> /var/www/html/index.html'", shell=True)

subprocess.run("ssh -o StrictHostKeyChecking=no -i key_pair.pem ec2-user@%s \
    'echo \"<H2>Local IPV4: \" >> /var/www/html/index.html'" %public_ip, shell=True)

subprocess.run("ssh -o StrictHostKeyChecking=no -i key_pair.pem ec2-user@34.241.90.222 \
    'curl --silent http://169.254.169.254/latest/meta-data/local-ipv4 >> /var/www/html/index.html'", shell=True)

subprocess.run("ssh -o StrictHostKeyChecking=no -i key_pair.pem ec2-user@%s \
    'echo \"<H2>Public DNS: \" >> /var/www/html/index.html'"%public_ip, shell=True)
subprocess.run("ssh -o StrictHostKeyChecking=no -i key_pair.pem ec2-user@34.241.90.222 \
    'curl --silent http://169.254.169.254/latest/meta-data/public-hostname >> /var/www/html/index.html'", shell=True)


# subprocess.run("ssh -o StrictHostKeyChecking=no -i key_pair.pem ec2-user@34.241.90.222 'cat /var/www/http/index.html'", shell=True)
# subprocess.run("ssh -o StrictHostKeyChecking=no -i key_pair.pem ec2-user@34.241.90.222 'cp index.html /var/www/html'", shell=True)
# subprocess.run("ssh -o StrictHostKeyChecking=no -i key_pair.pem ec2-user@34.241.90.222 'cat /var/www/html/index.html'", shell=True)