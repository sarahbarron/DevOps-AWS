#!/usr/bin/env python3
import boto3
import re

"""

Author: Sarah Barron
College: Waterford Institute of Technology
Course: HDip Computer Science
Module: Developer Operations
Assingment 1.

AWS EC2 key pair methods to:
- get user input for key pair details
- Add or remove the .pem extension for file name and group name
- Check for a valid key pair name using regex
- Create a new key pair

"""



"""
Method to create a new key pair
"""
def create_new_key_pair(keypair_name):
    try:
        ec2 = boto3.resource('ec2')

        # Using the keypair_name inputted by the user setup the file name
        # by adding the .pem extension to the name if it is not already present
        keypair_file_name = add_pem_file_extension(keypair_name)

        # Using the keypair_name inputted by the user setup the key name
        # by removing the .pem extension if the user had entered it at command line
        key_name = remove_pem_file_extension(keypair_name)
       
        # create a file to store the key locally
        keypair_file = open('./%s' %keypair_file_name, 'w')

        # create the key pair
        key_pair = ec2.create_key_pair(KeyName = key_name)
        
        # capture the key and store it in the file
        KeyPairOut = str(key_pair.key_material)
        keypair_file.write(KeyPairOut)
        
        # return the key name
        return key_name

    except Exception as error:
        if "(InvalidKeyPair.Duplicate)" in str(error):
            print ("\n %s this keypair already exists and will be used again to create this instance" %(keypair_name))
            return key_name
        else:
            print(error)


"""

Check for a vaild keypair name using regex

"""
def check_for_valid_keypair_name(keypair_name):
    try:
        if re.search(r'^[_\-a-zA-Z0-9]{1,255}""\.pem$', keypair_name) or re.search(r'^[_\-a-zA-Z0-9]{1,255}$', keypair_name):
            return False
        
        else:
            print("\n Invalid key pair Name \n")
            return True
    except Exception as error:
        print(error)


"""

Method adds a .pem file extension onto the key pair name
If the user has not included it during input.

"""
def add_pem_file_extension(keypair_name):
    try:
        if re.search(r'\.pem$', keypair_name):
            keypair_file = keypair_name
            
        else:
            keypair_file = "%s.pem" %keypair_name
            
        return keypair_file
    except Exception as error:
        print(error)


"""

Method removes the .pem file extension from the key pair file name
If the user has included it during input

"""
def remove_pem_file_extension(keypair_name):
    try:
        if re.search(r'\.pem$', keypair_name):
            keypair_name = keypair_name[0:-4]
            print(keypair_name)
            
        else:
            keypair_name = keypair_name
            
        return keypair_name
    except Exception as error:
        print(error)


"""

Setup the key pair with user input.
Ask the user for a name, check the name is a valid name, 
once the user has inputted a valid name send the name 
to the create_new_key_pair method. Return the key_name 

"""
def setup_key_pair():
    bad_key_pair_name = True
    while (bad_key_pair_name):
        # Look for input for a key pair name
        print ("\nkey pair names can be up to 255 characters long. Valid characters include _, -, a-z, A-Z, and 0-9.")
        print('\n\n Enter a unique key pair name (press enter for default assignment1): ', end='')
        keypair_name = input()
        # if the user wants to use a default key pair assign it to the assignment1 with a datetime stamp (avoids duplicates)
        if len(keypair_name) <= 0:
            keypair_name = ('assignment1-{:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()))    
        # checks for a valid key pair name
        bad_key_pair_name = check_for_valid_keypair_name(keypair_name)
    
    key_name = create_new_key_pair(keypair_name)
    
    return key_name
    