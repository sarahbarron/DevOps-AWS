#!/usr/bin/env python3

import boto3
from datetime import datetime, timedelta
import sys
from check_for_exit import checkForExit
import time


cloudwatch = boto3.resource('cloudwatch')
ec2 = boto3.resource('ec2')

'''
Function to check if the instance Id passed by command line
or inputted by the user is a valid instance id
'''
def check_for_valid_instance_id(instid):
    try:
        existing_instances = ec2.instances.all()
        instance = ec2.Instance(instid)
        if instance in existing_instances:
            return True
        return False
    except (Exception) as error:
            print (error)
    except(KeyboardInterrupt):
        sys.exit("\n\nProgram exited by keyboard interupt")

    
try:
    valid_instance = True

    # check if the instance id arguament has been passed from the command line
    if len(sys.argv)>1:
        # get the instance id from the command line arguement
        instid = sys.argv[1]
        # check to see if the instance ID is a valid instance ID
        valid_instance = check_for_valid_instance_id(instid)
        # If the input from command line is not a valid ID print the exit message
        if not valid_instance:
            print("\nYou can enter exit at any stage to exit the program early\n")
    
    # If no argument has been passed from command line ask the user to input the instance ID
    else:
        print("\nYou can enter exit at any stage to exit the program early\n")
        instid = input("Please enter instance ID(or exit to quit): ")    # Prompt the user to enter an Instance ID
        checkForExit(instid)
        valid_instance = check_for_valid_instance_id(instid)

    # check for a valid instance id and continue to ask until a valid id is entered
    valid_instance=True
    while not (valid_instance):
        print("\nInvalid instance ID. Please enter a valid instance ID: ", end='')
        instid = input()
        checkForExit(instid)
        valid_instance = check_for_valid_instance_id(instid)

    instance = ec2.Instance(instid)
    print('Instance retrieved %s\n'%instid)
    
    # Enables detailed monitoring on instance (1-minute intervals)
    instance.monitor()      

    # Get the CPU Utilization for the instance Id
    metric_iterator = cloudwatch.metrics.filter(Namespace='AWS/EC2',
                                                MetricName='CPUUtilization',
                                                Dimensions=[{'Name':'InstanceId', 'Value': instid}])
    # Extract the metric from teh list
    metric = list(metric_iterator)[0]   

    # Set up a CPU Utilization to monitor the last 5 minutes average, maximum and minimum values
    response = metric.get_statistics(StartTime = datetime.utcnow() - timedelta(minutes=5),   # 5 minutes ago
                                    EndTime=datetime.utcnow(),                              # now
                                    Period=300,                                             # 5 min intervals
                                    Statistics=['Average', 'Maximum', 'Minimum'])

    # Print the time of the Monitor
    print("Time: ", response['Datapoints'][0]['Timestamp'])

    # Print CPU Utilization values
    print ("\nCPU UTILISATION (over the last 5 minutes)")
    print ("\nMaximum CPU utilisation was:", response['Datapoints'][0]['Maximum'], response['Datapoints'][0]['Unit'])
    print ("Maximum CPU utilisation was:", response['Datapoints'][0]['Minimum'], response['Datapoints'][0]['Unit'])
    print ("Average CPU utilisation:", response['Datapoints'][0]['Average'], response['Datapoints'][0]['Unit'])

    time.sleep(1)

    # Get the metrics for Network in
    network_in_iterator = cloudwatch.metrics.filter(Namespace='AWS/EC2',
                                                MetricName='NetworkIn',
                                                Dimensions=[{'Name':'InstanceId', 'Value': instid}])

    # Extract the Network In for the instance
    network_in  = list(network_in_iterator)[0]

    # Set up the Network In to monitor the last 5 mins - min, max. avarage and total bytes
    response = network_in.get_statistics(StartTime = datetime.utcnow() - timedelta(minutes=5),   # 5 minutes ago
                                    EndTime=datetime.utcnow(),                              # now
                                    Period=300,
                                    Statistics=['Maximum', 'Minimum', 'Sum', 'Average'])
    # Print results
    print("\n\nNETWORK IN (over the last 5 minutes)")
    print ("\nMaximum Bytes received: ", response['Datapoints'][0]['Maximum'], response['Datapoints'][0]['Unit'])
    print ("Minimum Bytes received: ", response['Datapoints'][0]['Minimum'], response['Datapoints'][0]['Unit'])
    print ("Average Bytes Received: ", response['Datapoints'][0]['Average'], response['Datapoints'][0]['Unit'])
    print ("Total   Bytes received: ", response['Datapoints'][0]['Sum'], response['Datapoints'][0]['Unit'])
    time.sleep(1)

    # get the metrics for Network Out
    network_out_iterator = cloudwatch.metrics.filter(Namespace='AWS/EC2',
                                                MetricName='NetworkOut',
                                                Dimensions=[{'Name':'InstanceId', 'Value': instid}])
    # extract the network out for the instance
    network_out  = list(network_out_iterator)[0]

    # set up a Network Out monitor for the last 5 mins - min, max, average and total bytes
    response = network_out.get_statistics(StartTime = datetime.utcnow() - timedelta(minutes=5),   # 5 minutes ago
                                    EndTime=datetime.utcnow(),                              # now
                                    Period=300,
                                    Statistics=['Maximum', 'Minimum', 'Sum', 'Average'])
    # Print results
    print("\n\nNETWORK OUT (over the last 5 minutes)")
    print ("\nMaximum Bytes sent: ", response['Datapoints'][0]['Maximum'], response['Datapoints'][0]['Unit'])
    print ("Minimum Bytes sent: ", response['Datapoints'][0]['Minimum'], response['Datapoints'][0]['Unit'])
    print ("Average Bytes sent: ", response['Datapoints'][0]['Average'], response['Datapoints'][0]['Unit'])
    print ("Total   Bytes sent: ", response['Datapoints'][0]['Sum'], response['Datapoints'][0]['Unit'])

except (Exception) as error:
        print (error)
except(KeyboardInterrupt):
    sys.exit("\n\nProgram exited by keyboard interupt")
    