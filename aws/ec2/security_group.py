#!/usr/bin/env python3
"""
Author: Sarah Barron
College: Waterford Institute of Technology
Course: HDip Computer Science
Module: Developer Operations
Assingment 1.


AWS EC2 Security Group Methods
~ To look for user input for Security Group Details
~ To find valid reuseable Security Groups 
~ To create a security group with SSH, HTTP and HTTPS inbound access 
~ To check if the user inputs a unique name for a security group
~ To check that the user has inputted a valid group name and description

"""

import boto3
import time
import re

ec2 = boto3.resource('ec2')

"""
Create a security group with user input group name and description passed
to the method.
Set the security group up with SSH, HTTP and HTTPS inbound access
Return the security group ID
"""
def create_security_group(GroupName, Description):
    try:
        # Create the security group
        security_group = ec2.create_security_group(
            Description=Description,
            GroupName=GroupName,
        )

        # load the security group
        security_group.load()
    
        # Add inbound access to the security group 
        # with SSH, HTTP and HTTPS access
        response = security_group.authorize_ingress(
        IpPermissions=[
            {
                'FromPort': 22,
                'IpProtocol': 'tcp',          
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            
            },
            {
                'FromPort': 80,
                'IpProtocol': 'tcp',            
                'ToPort': 80,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            
            },

            {
                'FromPort': 443,
                'IpProtocol': 'tcp',
                'ToPort': 443,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            },
        ],

        )
        # load the security group
        security_group.load()

        print("Created Security Group ID : %s"%security_group.id)
        # return the security group id
        return security_group.id
    except Exception as error:
        print (error)


"""
Find all available security groups that can be used to create 
the instance. The Security group must have SSH inbound access
and belong to the default vpc
Returns a list of all valid security groups
"""

def find_available_security_groups():
    try:
        # Filter all security groups 
        # that have ssh access
        # and have the default vpc
        security_group_list = ec2.security_groups.filter(

            Filters=[
                {
                    'Name': 'ip-permission.from-port',
                    'Values': [
                        '22'
                    ],   
                },
                {
                    'Name': 'ip-permission.to-port',
                    'Values': [
                        '22'
                    ],
                },
                {
                    'Name': 'vpc-id',
                    'Values': [
                        'vpc-91a988f7'
                    ],
                },
            ],
            
        )

        # return a list of security group objects
        return security_group_list
    except Exception as error:
        print (error)

"""
Check if the user has inputted a duplicate group name
Returns True if it is a duplicate or False if it is unique
"""

def check_for_duplicate_security_group_name(name):
    security_group_list = []
    try:
        # return all security group objects
        security_group_objects = ec2.security_groups.all()

        # iterate through the security group objects, extract
        # the group name, convert to lower case and add the 
        # name to a list security group names
        for sg in security_group_objects:
            security_group_list.append(sg.group_name.lower())
        
        # if the user input name (convert to lower case for comparison)
        # is in the security group name list return True 
        if name.lower() in security_group_list:
            return True
        
        # if the user group name is not in the security group name list
        # return false
        return False
    except Exception as error:
        print (error)


"""
A function to check if the user has inputted a group name or description 
with valid characters, using regex
"""

def check_regex(input):
    try:
        if re.search(r'^[._\-:/()#,@[\]\+=&;{}!$\* a-zA-Z0-9]{1,255}$', input):
            return False
        
        else:
            return True
    except Exception as error:
        print(error)

"""
Method to look for user input for a group name and description
Once the user enters valid input the security group is created
and the method returns the security group ID
"""
def setup_security_group():

    invalid_input = True
    invalid_security_group = True
    available_security_groups = False
    list_security_groups = []
    group_name_is_duplicate = True
    invalid_regex = True

    print("\n-------------------------------------------------------------------------------------")
    print("  SETUP SECURITY GROUP")
    print("\n-------------------------------------------------------------------------------------")
    
    try:
        
        while (invalid_input):

            # returns a list off valid security groups
            security_groups_obj = find_available_security_groups()
            for sg in security_groups_obj:
                list_security_groups.append(sg.id)

            # if there is a valid security group available ask the user do they want to 
            # use an existing security group 
            if len(list_security_groups) > 0:
                print('Do you want to use an existing security group (y/n)', end='')
                yes_no = input()
                

            # if there are no valid security groups available go direct to creating one
            else:
                yes_no = 'n'
            
            # If the user wants to use an existing security group print the list of security groups
            # and ask the user to input the id of the user group they want to use
            if yes_no == 'y':
                
                while invalid_security_group:
                    print("\n-------------------------------------------------------------------------------------")
                    print('\nValid Security Group IDs: \n')

                    for sg in list_security_groups:
                        print(sg)
                    
                    print("\n-------------------------------------------------------------------------------------")

                    print('\nFrom the list above enter the ID of the security group you want to use: ', end='')
                    security_group_id = input()
                    # if the user enters a valid security group exit the loop
                    if security_group_id in list_security_groups:                            
                        invalid_input = False 
                        invalid_security_group = False
                       # security_group = ec2.SecurityGroup(security_group_id)
                    # If the user enters an invalid security group id continue to ask 
                    # the user for a valid id
                    else:
                        print('\nThis is an invalid security group ID \n')
            
            # If there are no valid security groups available or the user wishes to
            # create a security group. Ask the user for a group name and description
            elif yes_no == 'n':
                
                print('Lets create a new security group \n')

                # If the user enters a group name with invalid 
                # characters the user will be asked to enter a new valid group name
                while (invalid_regex):

                    # set to true initially
                    group_name_is_duplicate = True

                    # If the user enters a group name that is already a security group name
                    # the user will be asked to enter another group name
                    while (group_name_is_duplicate):
                    
                        print('Enter A Group Name: ', end='')
                        group_name = input()

                        # check if the entered group name is a duplicate
                        group_name_is_duplicate = check_for_duplicate_security_group_name(group_name)
                        
                        if group_name_is_duplicate:
                            print('This is a Duplicate group name. Please enter a unique group name')

                    # check if the regex of the group name is invalid
                    invalid_regex = check_regex(group_name)
                    if invalid_regex:
                        print("The name must only include the following characters:")
                        print("._-:()#,@[\]+=&;{\}!$\* a-z A-Z 0-9 ")
                    
                    
                # reset invalid_regex back to true to check the description regex    
                invalid_regex = True

                # Continue to loop until the user enters a description with correct regex
                while(invalid_regex):
                    
                    print('Enter A Description: ', end='')
                    description = input()
                    
                    # check if the descriptions regex is invalid
                    invalid_regex = check_regex(description)
                    if invalid_regex:
                        print("The name must only include the following characters:")
                        print("._-:()#,@[\]+=&;{\}!$\* a-z A-Z 0-9 ")

                
                # once a valid group name and description have been obtained
                # create the new security group
                security_group_id = create_security_group(group_name, description)
                # exit the loop
                invalid_input = False
            
            # if the user doesn't enter y or n if asked do they want to use  
            # an existing security group
            else:
                print('Your input is invalid please enter y or n \n\n')
        
        # return the security groups ID
        return security_group_id
    except Exception as error:
        print (error)
