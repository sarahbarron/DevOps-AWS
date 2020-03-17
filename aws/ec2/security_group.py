#!/usr/bin/env python3

'''
AWS EC2 Security Group Methods
~ To look for user input for Security Group Details
~ To find valid reuseable Security Groups 
~ To create a security group with SSH, HTTP and HTTPS inbound access 
~ To check if the user inputs a unique name for a security group
~ To check that the user has inputted a valid group name and description

'''

import datetime
import sys
import logging
import boto3
import time
import re
from check_for_exit import checkForExit

ec2 = boto3.resource('ec2')

'''
Create a security group with user input group name and description passed
to the method.
Set the security group up with SSH, HTTP and HTTPS inbound access
Return the security group ID
'''
def create_security_group(GroupName, Description):
    try:
        # Create the security group
        security_group = ec2.create_security_group(
            Description=Description,
            GroupName=GroupName,
        )
        
        logging.info('Security group %s created'%security_group)

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
        
        logging.info('Inbound access for SSH, HTTP and HTTPS added to the security group')

        print('\nCreated Security Group ID : %s'%security_group.id)
        # return the security group id
        return security_group.id

    except (Exception) as error:
        logging.error(error)
    except(KeyboardInterrupt):
        sys.exit("\n\nProgram exited by keyboard interupt")


'''
Find all available security groups that can be used to create 
the instance. The Security group must have SSH inbound access
and belong to the default vpc
Returns a list of all valid security groups
'''

def find_available_security_groups():
    try:
        
        # Return the default vpc
        default_vpcs = ec2.vpcs.filter(
            Filters=[
                {
                    'Name': 'isDefault',
                    'Values': [
                        'true'
                    ] 
                },
            ]
        )

        for vpc in default_vpcs:
            vpc_id = vpc.id

        logging.info('Defalut vpc %s returned, for security group filtering'%vpc_id)


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
                    'Values': 
                    [
                        vpc_id
                    ],
                },
            ],
            
        )

        logging.info('List of filtered security groups returned')
        # return a list of security group objects
        return security_group_list

    except (Exception) as error:
        logging.error(error)
    except(KeyboardInterrupt):
        sys.exit("\n\nProgram exited by keyboard interupt")


'''
Check if the user has inputted a duplicate group name
Returns True if it is a duplicate or False if it is unique
'''

def check_for_duplicate_security_group_name(name):
    security_group_list = []
    try:
        # return all security group objects
        security_group_objects = ec2.security_groups.all()
        
        logging.info('All security groups retrieved')

        # iterate through the security group objects, extract
        # the group name, convert to lower case and add the 
        # name to a list security group names
        for sg in security_group_objects:
            security_group_list.append(sg.group_name.lower())
        
        # if the user input name (convert to lower case for comparison)
        # is in the security group name list return True 
        if name.lower() in security_group_list:
            logging.warning('%s security group is a duplicate'%name)
            return True
        
        # if the user group name is not in the security group name list
        # return false
        logging.info('%s security group is not a duplicate'%name)
        return False

    except (Exception) as error:
        logging.error(error)
    except(KeyboardInterrupt):
        logging.error('keyboard Interrupt')
        sys.exit("\n\nProgram exited by keyboard interupt")



'''
A function to check if the user has inputted a group name or description 
with valid characters, using regex
'''

def check_regex(input):
    try:

        # If the security group begins with sg- return false
        if re.search(r'^sg-', input):
            logging.warning('%s The security name entered began with sg-'%input)
            return False

        # If the security group name passes the regex test return true
        if re.search(r'^[._\-:/()#,@[\]\+=&;{}!$\* a-zA-Z0-9]{1,255}$', input):
            logging.info('%s has passed the regex test'%input)
            return True

        # If the security group name does not pass the regex test return false        
        else:
            logging.info('%s has failed the regex test'%input)
            return False

    except (Exception) as error:
        logging.error(error)
    except(KeyboardInterrupt):
        logging.error('keyboard Interrupt')
        sys.exit("\n\nProgram exited by keyboard interupt")




'''
Setup a default security group with a
default group name and default description
'''
def setup_default_security_group():
    group_name = ('assignment1-security-group-{:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()))
    description = "Assignment One Security Group"

    security_group_id = create_security_group(group_name, description)
    
    logging.info('Default security %s created'%security_group_id)
    
    return security_group_id




'''
Method to look for user input for a group name and description
Once the user enters valid input the security group is created
and the method returns the security group ID
'''
def setup_security_group():

    invalid_input = True
    available_security_groups = False
    list_security_groups = []
    group_name_is_duplicate = True
    valid_regex = False

     
    try:
        
        while (invalid_input):

            # returns a list off valid security groups
            security_groups_obj = find_available_security_groups()
            
            # append the id to a list of security group ids  
            for sg in security_groups_obj:
                list_security_groups.append(sg.id)

            # if there is a valid security group available ask the user do they want to 
            # use an existing security group 
            if len(list_security_groups) > 0:
                print('\nSECURITY GROUP: Do you want to use an existing security group (y/n or enter to use default): ', end='')
                yes_no = input()
                checkForExit(yes_no)
                logging.info('User Input for use exisiting security group (y/n): %s'%yes_no)

            # if there are no valid security groups available go direct to creating one
            else:
                logging.info('There are no existing security groups, user will have to create one')
                yes_no = 'n'
            
            # If the user wants to use an existing security group print the list of security groups
            # and ask the user to input the id of the user group they want to use
            if yes_no == 'y':
                print('\n--------------------------------------------------------------------------------------------------------')
                print('\nValid Security Group IDs: \n')

                for sg in list_security_groups:
                    print(sg)
                    
                print('\n--------------------------------------------------------------------------------------------------------')

                while True:
                    print('\nFrom the list above enter the ID of the security group you want to use: ', end='')
                    security_group_id = input()
                    checkForExit(security_group_id)
                    logging.info('User input for enter a existing security group name : %s'%security_group_id)

                    # if the user enters a valid security group exit the loop
                    if security_group_id in list_security_groups:
                        logging.warning('The security group %s already exists'%security_group_id)                            
                        invalid_input = False 
                        break
                       # security_group = ec2.SecurityGroup(security_group_id)

                    # If the user enters an invalid security group id continue to ask 
                    # the user for a valid id
                    else:
                        logging.warning('User has entered an invalid security group')
                        print('\nINVALID security group ID \n')
            
            # If there are no valid security groups available or the user wishes to
            # create a security group. Ask the user for a group name and description
            elif yes_no == 'n':
                
                # If the user enters a group name with invalid 
                # characters the user will be asked to enter a new valid group name
                while not valid_regex:

                    # set to true initially
                    group_name_is_duplicate = True

                    # If the user enters a group name that is already a security group name
                    # the user will be asked to enter another group name
                    while (group_name_is_duplicate):
                    
                        print('\nSECURITY GROUP: Enter A Group Name (or press enter to use default): ', end='')
                        group_name = input()
                        checkForExit(group_name)
                        logging.info('User input for enter a group name : %s'%group_name)

                        #If the user has pressed enter for default give the default group name
                        if len(group_name)<=0:
                            group_name = ('assignment1-security-group-{:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()))
                            logging.info('Default group name given : %s' %group_name)

                        # check if the entered group name is a duplicate
                        group_name_is_duplicate = check_for_duplicate_security_group_name(group_name)
                        
                        # if the group name is a default print the message to warn the user
                        if group_name_is_duplicate:
                            logging.warning('Duplicate security group name entered')
                            print('This is a Duplicate group name. Please enter a unique group name')
                        
                        # Otherwise the user has entered a valid group name so break the loop
                        else:
                            break

                    # check if the regex of the group name is invalid
                    valid_regex = check_regex(group_name)
                    if not valid_regex:
                        print('The name must not start with sg- and can only include the following characters:')
                        print('._-:()#,@[\]+=&;{\}!$\* a-z A-Z 0-9 ')
                    
                
                logging.info('Group name %s has been set'% group_name)
                
                # initially set valid regex to false until fist loop is done
                valid_regex = False
                # Continue to loop until the user enters a description with correct regex
                while not valid_regex:
                    
                    print('Enter A Description (or press enter to use default): ', end='')
                    description = input()
                    checkForExit(description)
                    
                    logging.info('User Input for a description: %s'%description)

                    # if the user has pressed enter set the default description
                    if len(description) <=0:
                        description = "Assignment One Security Group"
                    
                    # check if the descriptions regex is invalid
                    valid_regex = check_regex(description)
                    if not valid_regex:
                        print('The name must only include the following characters:')
                        print('._-:()#,@[\]+=&;{\}!$\* a-z A-Z 0-9 ')
                    

                logging.info('Description %s has be set'% description)

                # once a valid group name and description have been obtained
                # create the new security group
                security_group_id = create_security_group(group_name, description)

                # exit the loop
                invalid_input = False

            # IF the use pressed enter setup a default security group            
            elif yes_no == '':
                security_group_id = setup_default_security_group()
                # set to false to exit loop
                invalid_input = False

            # if the user doesn't enter y or n if asked do they want to use  
            # an existing security group
            else:
                logging.warning('Invalid User Input')
                print('Your input is invalid please enter y or n or enter for default values \n\n')

        logging.info('Security group ID %s returned'%security_group_id)      

        # return the security groups ID
        return security_group_id
    
    except (Exception) as error:
        logging.error(error)
    except(KeyboardInterrupt):
        sys.exit("\n\nProgram exited by keyboard interupt")
