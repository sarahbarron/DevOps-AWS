#!/usr/bin/env python3
import sys
import boto3
import datetime
import urllib.request
import time
import subprocess

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
        print ('%s has been created \n' % response)

        # Put the image into the bucket
        response = s3.Object(bucket_name, object_name).put(ACL='public-read', Body=open(object_name, 'rb'))
        print ('The %s file has been put into the %s S3 bucket \n\n %s \n' %(object_name, bucket_name, response))

        # Remove the file from the local directory
        subprocess.run('rm %s'%object_name, shell=True)
        print('local copy of the file %s has been removed successfully \n'% object_name)
        return(bucket_name)

    except Exception as error:
        print (error)

def setup_s3_bucket():
    
    try:
        print('\n-------------------------------------------------------------------------------------')
        print('             CREATING AN S3 BUCKET                                                   ')
        print('-------------------------------------------------------------------------------------\n')

        print('Enter a name for your S3 bucket or press enter for a default name: ', end='')
        bucket_name = input()

        if len(bucket_name) <= 0:
            bucket_name = 'assignment1'

        
        bucket_details = create_new_bucket(bucket_name)

        return bucket_details
    except Exception as error:
        print (error)