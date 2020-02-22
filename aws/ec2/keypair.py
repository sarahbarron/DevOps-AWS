#!/usr/bin/env python3
import boto3
import re
import datetime
'''

Author: Sarah Barron
College: Waterford Institute of Technology
Course: HDip Computer Science
Module: Developer Operations
Assingment 1.

AWS EC2 key pair methods to create, validate, return or use existing key pairs

'''


ec2 = boto3.resource('ec2')


'''

Method to create a new key pair

'''
def create_new_key_pair(keypair_name):
    try:
        key_name = get_key_name(keypair_name)
              
        # create a file to store the key locally
        keypair_file = open('./%s.pem' %key_name, 'w')

        # create the key pair
        key_pair = ec2.create_key_pair(KeyName = key_name)
        
        # capture the key and store it in the file
        KeyPairOut = str(key_pair.key_material)
        keypair_file.write(KeyPairOut)
        
        # return the key name
        return key_name

    except Exception as error:
        if '(InvalidKeyPair.Duplicate)' in str(error):
            print ('\n %s this keypair already exists and will be used again to create this instance' %(keypair_name))
            return key_name
        else:
            print(error)






'''

Method Counts the number of existing keypairs

'''
def count_existing_keypairs():
    
    existing_key_pair_list = ec2.key_pairs.all()
    num_existing_key_pair = 0

    for kp in existing_key_pair_list:
       num_existing_key_pair += 1
    
    return num_existing_key_pair





'''

Method Prints a list of exisiting key pairs

'''
def print_exisiting_keypairs():
    existing_key_pair_list = ec2.key_pairs.all()
    print('\n-------------------------------------------------------------------------------------')
    print(' Existing Key Pairs')
    print('\n-------------------------------------------------------------------------------------')
    for kp in existing_key_pair_list:
        print(kp.name)
    print('\n-------------------------------------------------------------------------------------')





'''

Method to check if the key pair entered by the user is a duplicate
If it is a duplicate the original key pair name is returned
as it is an exact match (case sensitive)
otherwise return the string duplicate! (use ! as this can not be in a key pair name) 

'''
def check_if_keypair_is_duplicate(user_input):

    existing_key_pair_list = ec2.key_pairs.all()

    # convert to lower case for the comparison
    user_input_lower = user_input.lower()

    for kp in existing_key_pair_list:
        kp_lower = kp.name.lower()
        if kp_lower == user_input_lower:
            return kp.name

    return 'duplicate!'






'''

Function to check a users input for using an existing keypair is correct

'''
def check_input_is_in_keypair_list(user_input):
    
    existing_key_pair_list = ec2.key_pairs.all()

    # convert to lower case to compare
    user_input_lower = user_input.lower()

    for kp in existing_key_pair_list:
        kp_lower = kp.name.lower()

        if kp_lower == user_input_lower:
            return kp.name

    return 'DOES NOT EXIST!'





'''

Check for a vaild keypair name using regex

'''
def check_keypair_regex(user_input):
    try:
        if re.search(r'^[_\-a-zA-Z0-9]{1,255}\.pem$', user_input) or re.search(r'^[_\-a-zA-Z0-9]{1,255}$', user_input):
            return False
        
        else:
            print('\n Invalid key pair Name \n')
            return True
    except Exception as error:
        print(error)





'''

This method takes a keypair name and seperates the key name from the file name
and returns the keyname

'''
def get_key_name(keypair):
    try:
        if re.search(r'\.pem$', keypair):
            name = re.findall(r'^([_\-a-zA-Z0-9]{1,255})(\.pem)$', keypair)
            return name[0][0]
        else:
            return keypair
        
    except Exception as error:
        print(error)





'''

Setup Key Pair Method

'''
def setup_keypair_name():
    try:
        print('\n-------------------------------------------------------------------------------------')
        print('  SETUP KEY PAIR')
        print('\n-------------------------------------------------------------------------------------')
            
        outer_invalid_input = True

        while(outer_invalid_input):

            # If there are exisiting keypairs available ask the user would they like to 
            # use an existing key pair
            # If there are no exisiting keypairs move on to create an instance
            num_existing_keypairs = count_existing_keypairs()
            if num_existing_keypairs > 0:
                print('\nWould you like to use an existing key pair (y or n): ', end='')
                use_existing_kp = input()
            else:
                use_existing_kp = 'n'
            

            # If the user enters y ask them to enter the name of the keypair they want to use
            # check that their input is valid
            if use_existing_kp == 'y' or use_existing_kp == 'Y':
                
                inner_invalid_input = True

                while inner_invalid_input:
                    # Print the available key pairs
                    print_exisiting_keypairs()
            
                    print ('\nEnter the name of the keypair you want to use from the list: ', end='')
                    user_input = input()
                   
                    # If the user has entered .pem remove it 
                    keypair_name = get_key_name(user_input)
                
                    # check the user has entered the correct key pair name 
                    keypair_name = check_input_is_in_keypair_list(keypair_name)
                  
                    # if the user hasn't entered the correct keypair name the string 'DOES NOT EXIST!' is returned
                    if keypair_name == 'DOES NOT EXIST!':
                        print('\nYou have entered an incorrect key pair name\n')
                    # if the user has entered a correct key pair name exit and return the keypair name
                    else:
                        inner_invalid_input = False
                        outer_invalid_input = False
        
            # If there are no existing key pairs or the user wants to create a new key pair 
            elif use_existing_kp == 'n' or use_existing_kp == 'N':

                inner_invalid_input = True

                while inner_invalid_input:
                    bad_keypair_name = True

                    # Get user input for a key pair name and check the regex is correct
                    while bad_keypair_name:

                        print ('\nkey pair names can be up to 255 characters long. Valid characters include _ - a-z A-Z and 0-9')
                        print('\nEnter a unique key pair name (press enter for a default name): ', end='')
                        user_input = input()
                        
                        # if the user does not enter anything use the default key name assignment1 appended with a date stamp
                        if len(user_input)<=0:
                            keypair_name = ('assignment1-{:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()))
                        
                        keypair_name = get_key_name(user_input)
                        bad_keypair_name = check_keypair_regex(keypair_name)

                    # Check to make sure the user input for the key name does not already exist
                    already_exists = True
                    while already_exists:
                    
                        existing_keypair_name = check_input_is_in_keypair_list(keypair_name)
                        
                        # If the user input doesn't exist already create a new key pair
                        if existing_keypair_name == 'DOES NOT EXIST!':
                            already_exists = False
                            inner_invalid_input = False
                            outer_invalid_input = False
                            name = get_key_name(keypair_name)
                            keypair_name = create_new_key_pair(name)
                        
                        # Otherwise the key pair already exists ask they user would they like to use the existing one
                        else:
                            invalid_input = True
                            while invalid_input:
                                print('The key pair name you have entered already exists')
                                print('would you like to use the existing key pair y or n?', end='')
                                user_input = input()

                                # If the user chooses to use the existing one exit loops and return the keypair_name
                                if user_input == 'y' or user_input == 'Y':
                                    invalid_input = False
                                    already_exists = False
                                    inner_invalid_input = False
                                    outer_invalid_input = False
                                    keypair_name = existing_keypair_name
                                
                                # If they choose n return to the start an ask the user to input a key pair name
                                elif user_input == 'n' or user_input == 'N':
                                    invalid_input = False
                                    already_exists = False
                                
                                # otherwise the input has been invalid so print this message
                                else:
                                    print('Invalid input you must enter y or n')

            else:
                print ('Invalid input please enter y or n')

        print('keypair name being used: %s' % keypair_name)
        return keypair_name
    except Exception as error:
            print(error)
