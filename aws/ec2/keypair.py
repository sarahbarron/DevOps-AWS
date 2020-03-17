#!/usr/bin/env python3
import boto3
import re
import datetime
import subprocess
from check_for_exit import checkForExit
import sys 
import logging


'''
AWS EC2 key pair methods to create, validate, return or use existing key pairs
'''

ec2 = boto3.resource('ec2')


'''
Method to create a new key pair
'''

def create_new_key_pair(keypair_name):
    try:

        # get the keyname with out .pem extension if one is included
        key_name = get_key_name(keypair_name)
      
        # create a file to store the key locally
        keypair_file = open('./%s.pem' %key_name, 'w')

        logging.info('%s.pem file created with write access'%key_name)

        # create the key pair
        key_pair = ec2.create_key_pair(KeyName = key_name)
        
        logging.info('keypair created')

        # capture the key and store it in the file
        KeyPairOut = str(key_pair.key_material)
        keypair_file.write(KeyPairOut)

        logging.info('keypair written to file')
        
        # For security reasons the keypair pem file must not be accessable externally
        subprocess.run('chmod 400 ./%s.pem'%key_name, shell=True)        
        
        logging.info('%s.pem access levels amended to only have read access from owner - for security reasons'%key_name)
        
        # return the key name
        return key_name

    except (Exception) as error:
        if '(InvalidKeyPair.Duplicate)' in str(error):
            logging.error(error)
            print(error)
        else:
            logging.error(error)
    except(KeyboardInterrupt):
        sys.exit("\n\nProgram exited")



'''
Method Counts the number of existing keypairs
'''
def count_existing_keypairs():
    try:

        existing_key_pair_list = ec2.key_pairs.all()

        logging.info('list of ec2 key pairs returend')

        num_existing_key_pair = 0

        for kp in existing_key_pair_list:
            num_existing_key_pair += 1
        
        logging.info('Number of keypairs available : %s' %num_existing_key_pair)

        return num_existing_key_pair

    except (Exception) as error:
        print(error)
    except(KeyboardInterrupt):
        sys.exit("\n\nProgram exited")



'''
Method Prints a list of exisiting key pairs
'''

def print_exisiting_keypairs():
    try:
        existing_key_pair_list = ec2.key_pairs.all() 

        print('\n--------------------------------------------------------------------------------------------------------')
        print('Existing Key Pairs \n')
        for kp in existing_key_pair_list:
            print(kp.name)
        print('\n--------------------------------------------------------------------------------------------------------')

        logging.info('available keypairs printed to terminal')

    except (Exception) as error:
        print(error)
    except(KeyboardInterrupt):
        sys.exit("\n\nProgram exited")




'''
Function to check if the user input is in the list of available keypairs
'''
def check_input_is_in_keypair_list(user_input):
    
    try:
        existing_key_pair_list = ec2.key_pairs.all()

        # convert to lower case to compare
        user_input_lower = user_input.lower()

        for kp in existing_key_pair_list:
            kp_lower = kp.name.lower()

            if kp_lower == user_input_lower:
                logging.info('Keypair name inputted is on the available keypair list')    
                return kp.name

        logging.info('Keypair name is not on the available keypair list')
        return 'DOES NOT EXIST!'

    except (Exception) as error:
        logging.error(error)
    except(KeyboardInterrupt):
        sys.exit("\n\nProgram exited")



'''
Check for a vaild keypair name using regex
'''

def check_keypair_regex(user_input):
    try:
        if re.search(r'^[_\-a-zA-Z0-9]{1,255}\.pem$', user_input) or re.search(r'^[_\-a-zA-Z0-9]{1,255}$', user_input):
            logging.info('The keypair name: %s passed the regex test'%user_input)
            return True
        
        else:
            logging.info('The keypair name: %s failed the regex test'%user_input)
            print('\nINVALID Key Pair Name \n')
            return False

    except (Exception) as error:
        logging.error(error)
    except(KeyboardInterrupt):
        sys.exit("\n\nProgram exited by keyboard interupt")



'''

This method takes a keypair name and seperates the key name from the file name
and returns the keyname

'''
def get_key_name(keypair):
    try:

        # If the keypair supplied has the .pem extension seperate it and return only the name
        if re.search(r'\.pem$', keypair):
            name = re.findall(r'^([_\-a-zA-Z0-9]{1,255})(\.pem)$', keypair)
            logging.info('The .pem extension has been removed from %s and only the keypair name has been returned'%keypair)
            return name[0][0]
        # Otherwise there was not extension so return the keypair name
        else:
            logging.info('%s had no .pem extension so the keyname has been returned unedited')
            return keypair
        
    except (Exception) as error:
        logging.error(error)
    except(KeyboardInterrupt):
        sys.exit("\n\nProgram exited by keyboard interupt")



'''
Setup Key Pair Method
'''
def setup_keypair_name():
    try:
        outer_invalid_input = True

        while(outer_invalid_input):
            
            # Get the number of existing keypairs available
            num_existing_keypairs = count_existing_keypairs()

            # If there are exisiting keypairs available ask the user would they like to 
            # use an existing key pair
            # If there are no exisiting keypairs move on to create an instance
            if num_existing_keypairs > 0:
                print('\nKEYPAIR: Would you like to use an existing key pair (y or n or press enter for default value): ', end='')
                use_existing_kp = input()
                logging.info('User Input: Use existing keypair : %s'%use_existing_kp)
                checkForExit(use_existing_kp)
            
            else:
                logging.info('There are no existing keypairs available')
                use_existing_kp = 'n'
            

            # If the user enters y ask them to enter the name of the keypair they want to use
            # check that their input is valid
            if use_existing_kp == 'y' or use_existing_kp == 'Y':
                
                # Print the available key pairs
                print_exisiting_keypairs()
                
                print('Please ensure the .pem file of the keypair you choose from the list above is stored in the Assignment1 Directory')
                
                while True:
                    print ('\nEnter the name of the keypair you want to use from the list (or press enter to create a new one): ', end='')
                    user_input = input()
                    logging.info('User Input for existing keypair: %s'%user_input)
                    checkForExit(user_input)

                    # If the user hits return automatically revert to creating a new keypair
                    if len(user_input) == 0:
                        logging.info('User pressed enter divert user from using an existing keypair to creating a keypair')
                        use_existing_kp = 'n'
                        break

                    checkForExit(user_input)

                    # If the user has entered .pem remove it 
                    keypair_name = get_key_name(user_input)
                
                    # check the user has entered the correct key pair name 
                    keypair_name = check_input_is_in_keypair_list(keypair_name)

                    # check the keypair is located in the Assignment1 folder
                    stored_locally = subprocess.check_output('ls|grep -s %s|wc -l' %keypair_name, shell=True)
            
                    if int(stored_locally) > 0:
                        logging.info('%s is stored locally' %keypair_name)

                        # if the user hasn't entered the correct keypair name the string 'DOES NOT EXIST!' is returned
                        if keypair_name == 'DOES NOT EXIST!':
                            logging.warning('This Keypair does not exist')
                            print('\nYou have entered an incorrect key pair name\n')
                        # if the user has entered a correct key pair name exit and return the keypair name
                        
                        else:
                            logging.info('%s keypair name enter is on the list of existing keypairs')
                            outer_invalid_input = False
                            break
                    
                    else:
                        logging.warning('keypair is not stored locally')
                        print("\nKeypair is not stored in the Assignment1 directory")

            # If there are no existing key pairs or the user wants to create a new key pair 
            elif use_existing_kp == 'n' or use_existing_kp == 'N':

                logging.info('Create a new keypair....')

                # loop trigger set to true to start
                inner_invalid_input = True

                while inner_invalid_input:

                    # valid keypair name loop trigger set to True to start        
                    valid_keypair_name = False

                    # Get user input for a key pair name and check the regex is correct
                    while not valid_keypair_name:

                        print ('\nCREATE KEY PAIR NAME: Valid characters include _ - a-z A-Z and 0-9 with a max of 255 characters')
                        print('\nEnter a unique key pair name (press enter for a default name): ', end='')
                        user_input = input()
                        checkForExit(user_input)

                        logging.info('User Input for keypair name: %s'%user_input)

                        # if the user does not enter anything use the default key name assignment1 appended with a date stamp
                        if len(user_input)<=0:
                            user_input = ('kp-assignment1-{:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()))
                            logging.info('User pressed enter, default keypair name created: %s'%user_input)
                        
                        # If the user entered a name with .pem extension remove it from the name
                        keypair_name = get_key_name(user_input)

                        # check if the regex of the keypair is valid
                        valid_keypair_name = check_keypair_regex(keypair_name)

                    # Check to make sure the user input for the key name does not already exist
                    already_exists = True
                    while already_exists:
                    
                        # method to check if  keypair name exists
                        existing_keypair_name = check_input_is_in_keypair_list(keypair_name)
                        
                        # If the user input doesn't exist already create a new key pair
                        if existing_keypair_name == 'DOES NOT EXIST!':
                            logging.info('The keypair %s does not exist already'%keypair_name)
                            already_exists = False
                            inner_invalid_input = False
                            outer_invalid_input = False
                            name = get_key_name(keypair_name)
                            keypair_name = create_new_key_pair(name)
                          

                        # Otherwise the key pair already exists ask they user would they like to use the existing one
                        else:
                            while True:
                                logging.warning('keypair name %s already exists'%keypair_name)
                                print('\nThe key pair name you have entered already exists')
                                print('Would you like to use the existing key pair y or n?', end='')
                                user_input = input()
                                checkForExit(use_existing_kp)
                                logging.info('User Input: use an existing pair (y/n): %s'%user_input)

                                # If the user chooses to use the existing one exit loops and return the keypair_name
                                if user_input == 'y' or user_input == 'Y':
                                    already_exists = False
                                    inner_invalid_input = False
                                    outer_invalid_input = False
                                    keypair_name = existing_keypair_name
                                    logging.info('Existing keypair %s will be used for this EC2 instance')
                                    break
                                
                                # If they choose n return to the start an ask the user to input a key pair name
                                elif user_input == 'n' or user_input == 'N':
                                    already_exists = False
                                    break
                                
                                # otherwise the input has been invalid so print this message
                                else:
                                    logging.warning('Invalid user input')
                                    print('\nInvalid input you must enter y or n')

            # If user presses enter use the default value
            elif use_existing_kp == '' or use_existing_kp == '':                       
                keypair_name = ('kp-assignment1-{:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()))  
                name = get_key_name(keypair_name)
                keypair_name = create_new_key_pair(name)
                outer_invalid_input = False

            else:
                logging.warning('Invalid user input')
                print ('\nInvalid input please enter y or n')

        logging.info('Keypair %s Created'%keypair_name)
        print('\nKeypair: %s'%keypair_name)
        return keypair_name

    except (Exception) as error:
        logging.error(error)
    except(KeyboardInterrupt):
        sys.exit("\n\nProgram exited by keyboard intereupt")

'''
Method for when a user chooses to use a default keypair name
default keypair name will be kp-assignment1 with timestamp 
'''
def setup_default_keypair():
    try:
        name = ('kp-assignment1-{:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()))  
        keypair_name = create_new_key_pair(name)
        logging.info('Keypair %s Created'%keypair_name)
        return keypair_name

    except (Exception) as error:
        logging.error(error)
    except(KeyboardInterrupt):
        sys.exit("\n\nProgram exited by keyboard intereupt")
