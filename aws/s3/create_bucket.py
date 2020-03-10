#!/usr/bin/env python3
import sys
import boto3
import datetime
import urllib.request
import time
import subprocess
import re
from check_for_exit import checkForExit
s3 = boto3.resource('s3')

def create_new_bucket(bucket_name):

    # Bucket name with time date added to the end to make it unique
    bucket_name = ('%s-{:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()) %bucket_name)
    # Url to the image
    image_url = 'http://devops.witdemo.net/image.jpg'
    # Name of the image
    object_name = 'image.jpg'



    try:
       
        # Retrieve the image from the url and save it as image.jpg
        url = urllib.request.urlretrieve(image_url, object_name)
        print ('Image file %s has been retrieved from %s \n'%(object_name, image_url))
        # Create an s3 bucket
        response = s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
        print ('S3 Bucket: %s has been created \n' % bucket_name)

        # Put the image into the bucket
        response = s3.Object(bucket_name, object_name).put(ACL='public-read', Body=open(object_name, 'rb'))
        print ('The %s file has been put into the %s S3 bucket \n\n %s \n' %(object_name, bucket_name, response))

        # Remove the file from the local directory
        subprocess.run('rm %s'%object_name, shell=True)
    
        return(bucket_name)

    except (Exception) as error:
        print (error)
    except(KeyboardInterrupt):
        sys.exit("\n\nProgram exited by keyboard interupt")

"""

Check the regex of the bucket name

"""
def check_bucket_name_regex(bucket_name):

    # check that is not formatted as an IP address
    if re.search(r'^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$', bucket_name):
        return True

    # check that it follows all other rules of bucket names
    if re.search(r'^[a-z0-9]{1}[a-z0-9-.]{1,61}[a-z0-9]{1}$', bucket_name):
        return False
    
    return True

def setup_s3_bucket(default):
    
    try:
        # if the user has selected to use all default values set the name here
        if default == "true":
            print('\n-------------------------------------------------------------------------------------')
            print(' CREATING AN S3 BUCKET FOR STORING IMAGE.JPG                                           ')
            print('-------------------------------------------------------------------------------------\n')
            print("\nPlease wait a few moments while we create your S3 Bucket ....\n")
            bucket_name = 'assignment1-{:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now())
        # Otherwise the user has selected to setup the s3 bucket name 
        else:
            
            print('\n-------------------------------------------------------------------------------------')
            print('      CREATE AN S3 BUCKET TO STORE IMAGE.JPG                                           ')
            print('-------------------------------------------------------------------------------------\n')
            print('\nYOU CAN ENTER EXIT AT ANY STAGE TO EXIT THE PROGRAM\n')
            invalid_regex = True
            
            # Continues to loop until the correct regex for the file name passes
            while invalid_regex:
                print('Enter a name for your S3 bucket (or press enter for a default name): ', end='')
                bucket_name = input()
                checkForExit(bucket_name)

                # if the user has pressed enter give the bucket name the default name
                if len(bucket_name) <= 0:
                    bucket_name = 'assignment1-{:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now())
                
                # check the regex of the bucket name if false this will exit the loop
                invalid_regex = check_bucket_name_regex(bucket_name)

                # if the regex is invalid (true) print the message and start the loop again
                if invalid_regex:
                    print("\nYou have entered an invalid bucket name")
                    print("\nbucket names can not be in the format of an ip address (eg: 192.16.19.123)")
                    print("bucket names must begin and end in a lower case letter or number")
                    print("buckt names can contain . and - characters")
                    print("bucket names can not contain CAPITAL letters or underscores_\n")

        # Create the bucket
        bucket_details = create_new_bucket(bucket_name)

        # return bucket details
        return bucket_details

    except (Exception) as error:
        if error == "<urlopen error [Errno 111] Connection refused>":
            print("Could not create the S3 Bucket - Your Firewall may be preventing the connection")
    except(KeyboardInterrupt):
        sys.exit("\nProgram exited by keyboard interupt")