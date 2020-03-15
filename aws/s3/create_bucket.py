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

'''
Create a new S3 Bucket

'''
def create_new_bucket(bucket_name):

    # Bucket name with time date added to the end to make it unique
    bucket_name = ('%s-{:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()) %bucket_name)

    try:
        # Create an s3 bucket
        s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
        print ('S3 Bucket: %s has been created \n' % bucket_name)
        # upload the image to the created bucket
        upload_image_to_bucket(bucket_name)
    
        return(bucket_name)

    except (Exception) as error:
        print (error)
    except(KeyboardInterrupt):
        sys.exit("\n\nProgram exited by keyboard interupt")


''' 
Upload an image located at 'http://devops.witdemo.net/image.jpg'
to a choosen bucket
'''

def upload_image_to_bucket(bucket_name):

    # Url to the image
    image_url = 'http://devops.witdemo.net/image.jpg'
    # Name of the image
    object_name = 'image.jpg'

    try:
        # Retrieve the image from the url and save it as image.jpg
        urllib.request.urlretrieve(image_url, object_name)
        print ('Image file %s has been retrieved from %s \n'%(object_name, image_url))
        # Put the image into the bucket and make it public read
        s3.Object(bucket_name, object_name).put(ACL='public-read', Body=open(object_name, 'rb'))
        print ('The %s file has been uploaded to the %s S3 bucket\n' %(object_name, bucket_name))

        # Remove the file from the local directory
        subprocess.run('rm %s'%object_name, shell=True)

    except (Exception) as error:
        print (error)
    except(KeyboardInterrupt):
        sys.exit("\n\nProgram exited by keyboard interupt")


"""
Check the regex of the bucket name
"""

def check_bucket_name_regex(bucket_name):

    try: 
        # check if its formatted as an IP address
        if re.search(r'^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$', bucket_name):
            return True

        # check if it follows the correct Regex for a S3 Bucket Name
        if re.search(r'^[a-z0-9]{1}(?!.*[.-]{2})[a-z0-9-.]{1,61}[a-z0-9]{1}$', bucket_name):
            return False
        
        return True
    except (Exception) as error:
        print (error)
    except(KeyboardInterrupt):
        sys.exit("\n\nProgram exited by keyboard interupt")


'''
Get a list of bucket names and print them
'''
def get_existing_buckets():
    list_bucket_names =[]
    all_buckets = list(s3.buckets.all())
    print("\nExisting S3 Buckets")
    print('\n--------------------------------------------------------------------------------------------------------')
    for bucket in all_buckets:
        print(bucket.name)
        list_bucket_names.append(bucket.name)
    
    return list_bucket_names


'''
Setup of an S3 Bucket
'''
def setup_s3_bucket(default):
    
    try:
        print('\n--------------------------------------------------------------------------------------------------------')
        print('              CREATE AN S3 BUCKET FOR STORING IMAGE.JPG')
        print('\n--------------------------------------------------------------------------------------------------------')
        print("\nEXIT: You can enter exit at any stage to exit the program early\n")
        # if the user has selected to use all default values set the name here
        if default == "true":
            print("\nPlease wait a few moments while we create your S3 Bucket ....")
            bucket_name = 'assignment1-{:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now())
        # Otherwise the user has selected to setup the s3 bucket name 
        else:

            # check to see if there are any existing S3 Buckets that can be used
            buckets = s3.buckets.all()
            num_of_buckets = len(list(buckets))
            file_uploaded=False
            # If there are existing buckets that can be used ask the user do they want to use an
            # existing S3Bucket or not 
            if num_of_buckets > 0:
                while True:
                    print('\nWould you like to use an existing S3 Bucket (y/n) : ', end='')
                    user_input = input()
                    checkForExit(user_input)
                
                    if user_input == 'n' or user_input == 'N':
                        new_bucket = True
                        break
                    # If the user wants to use an existing bucket print a list of buckets and ask
                    # them to enter a valid name from the list
                    if user_input == 'y' or user_input == 'Y':
                        while True:
                            all_buckets = get_existing_buckets()
                            print("\nEnter the name of the of the S3 Bucket you want to use: ", end='')
                            s3_bucket_name = input()
                            checkForExit(s3_bucket_name)
                            # if the user input's name is in the list of bucket names
                            # upload the image to the bucket a exit
                            if s3_bucket_name in all_buckets:
                                upload_image_to_bucket(s3_bucket_name)
                                new_bucket = False
                                file_uploaded=True
                                break
                            else:
                                print('\nInvalid Bucket Name')
                    if file_uploaded:
                        break

            # If there are no existing S3 buckets a new one will have to be created
            else: 
                new_bucket = True
            

            # Create a new S3 bucket
            if new_bucket:
                while True:
                    print('Enter a name for your S3 bucket (or press enter for a default name): ', end='')
                    bucket_name = input()
                    checkForExit(bucket_name)

                    # if the user has pressed enter give the bucket name the default name
                    if len(bucket_name) <= 0:
                        bucket_name = 'assignment1-{:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now())
                    
                    # check the regex of the bucket name if false this will exit the loop
                    invalid_regex = check_bucket_name_regex(bucket_name)

                    # if the regex is invalid print the message and start the loop again
                    if invalid_regex:
                        print("\nYou have entered an invalid bucket name")
                        print("\nbucket names can not be in the format of an ip address (eg: 192.16.19.123)")
                        print("bucket names must begin and end in a lower case letter or number")
                        print("buckt names can contain . and - characters")
                        print("bucket names can not contain CAPITAL letters or underscores_\n")
                    else:
                        break
                # Create the bucket
                s3_bucket_name = create_new_bucket(bucket_name)
                
        # return bucket details
        return s3_bucket_name

    except (Exception) as error:
        if error == "<urlopen error [Errno 111] Connection refused>":
            print("Could not create the S3 Bucket - Your Firewall may be preventing the connection")
        else:
            print(error)
    except(KeyboardInterrupt):
        sys.exit("\nProgram exited by keyboard interupt")