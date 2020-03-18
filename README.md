
## Developer Operations Assignment1. 

### Core assignment specification

The overall objective of this assignment is to automate using Python 3 the process of creating, 
launching and monitoring a public-facing web server in the Amazon cloud. 
The web server will run on an EC2 instance and display some static content that is stored in S3. 
The program that does this must be called run_newwebserver.py


More detailed specification:
- Firstly, your Python program should create and launch a new Amazon EC2 nanoinstance. You must use the boto3 API library to launch from a free tier Amazon Linux AMI. Use an up-to-date AMI version. You will need to have your Amazon credentials in a configuration file (~/.aws/credentials) and not in the Python code. 
- Ensure your program launches the instance into an appropriate security group (you can optionally create one programmatically) and is accessible using your SSH key.
- You should provide a “User Data” start-up script when creating the instance. This start-up script should apply any required patches to the operating system and then install the web server(e.g. Apache).
- Another core requirement is that you write Python 3 code to create an S3 bucket and copy an image up to this bucket. We will make this image available at http://devops.witdemo.net/image.jpg .The image at this URL will change so your code will need to handle this in a generic manner. Your webserver main (home) page should then be configured so that this image will be visible (and loaded from yourownS3 URL)by a browser visiting the website. 
- You must use ssh remote command execution to use curl or equivalent to retrieve a piece of information from instance metadata(e.g. availability zone or subnet) and display it on the web server home page with the image. You will need to use the public IP address or DNS name assigned to your instance to connect to it using ssh. 
- Use boto to monitor a selection of EC2 and/or S3 metrics using Cloudwatch. 
- Your code should perform appropriate error handling (using exceptions) and output meaningful messages to the user. Implement logging functionality so that details of what is happening (whether normal or errors) can be written to the console or a file.

### Some additional functionality
The above is the core assignment specification. In addition you are expected to explore one or more other tasks. The following would be reasonable examples:
- Configure other services remotely
- Pass parameters as command line arguments 
- Query web server access/error logs using grep or equivalent
- Expand on the CloudWatch monitoring step to take some action –for example create and start another instance automatically if some threshold is exceeded
- Monitor resource usage using custom Cloudwatch metrics (e.g. website page views)

### Non-functional issues: readability, robustness, user-friendliness
As well as for core functionality and testing, marks will be awarded for:
- Testing – for example using Python’s unittest module or alternatives.
- Script readability –it helps to have good code comments, appropriate code layout/spacing, and good variable and function names.
- Robustness – how the script deals with error conditions and unexpected situations.
- User-friendliness of the scripts –meaningful messages provided to user and opportunities for user interaction.

__________

### Tool and Technologies 

- VMWare - Virtual Machine
- Ubuntu - Open Source Linux Operating System
- AWS - Cloud service provider 
  - EC2 - Elastic Compute Cloud
  - S3 - Cloud storage
  - CloudWatch - Cloud monitoring of the EC2 Instance
- Python - programming language
- Python packages:
  - Boto3 - Connecting to AWS
  - subprocess - running command line arguments
  - datetime - time stamps
  - time - sleep or pause a program for a certain amount of seconds
  - logging - logging developer debugging messages
  - sys - To exit the program during keyboard interrupt
  - re - regex searching
  - urllib.request - retrieving the image from the web address

_____________
### Running the program

- Open a terminal window inside the Assignment1 directory

- run the command `./run_newwebserver.py`

- When the run_newwebserver.py program has completed you can then run the monitor program from the same directory (Assignment1)

- run the command `./aws/cloudwatch/monitor.py`

_______________
### What I completed
#### EC2 nano Instance
An EC2 nano Instance is created. The instance includes:
- The most current free tier AMI
- minCount = 1
- maxCount = 1
- Instance type = t2 nano
- monitoring is enabled
- security group with access from SSH, HTTP and HTTPS
- Name tag
- User Data - Installs and starts up the apache server with an index.html home page

#### S3 Bucket
An S3 Bucket is created. The image.jpg is retrieved from http://devops.witdemo.net/image.jpg and stored in the S3Bucket and image and is given public read access.

#### Security Group
The security group is created with a name, description and SSH, HTTP and HTTPS access.

#### Keypair 
A keypair can be created stored and used by the program

#### Webpage
The apache servers home page is created showing the image.jpg and details about the instance using subprocess.run() to run shell and curl commands. 

#### CloudWatch
CloudWatch monitors the EC2 instance. The project includes a CloudWatch monitor program that returns information from the previous 5 minutes for CPU Utilization, Network In data and Network Out data.

#### Additional Functionality
- User Input: The user has the option to select setup by default or to have input into the setup. They can choose security group names, description, keypair names and bucket names
- Use existing security groups and keypairs: The user can choose to use existing security groups and keypairs that are eligible from their AWS account.
- Command line argument: To run the monitor.py file the user has the option to include the instance Id here so the program returns monitor details for that instance directly.
- CloudWatch Alarm: I put a cloudwatch alarm onto the instance which monitors if the instance has been below an average of 1 threshold for 1 hour, if it has it shows the instance is not in use so terminates the instance.

#### Non Functional
- Robustness: I have tried to cover all scenarios and areas that could cause errors or unexpected situations such as dealing with invalid input, duplicate names, regex checking of names, checking to make sure a keypair.pem file is stored locally, retrieving only existing security groups are returned using filtering etc.
- Handling of Errors: I have included pythons Try Except blocks on all functions in my program and have handled keyboard interrupts
- Logging: I include many logging messages with are logged to the mylog.log file in the root directory
- Testing: I included Python Unittesting for regex, existing keypairs, getting key names and duplicate security groups.
- User Friendly: I feel the program is user friendly as they only have to run one main program to create the EC2 with Apache server, S3 Bucket, build a webpage, setup monitoring and an alarm. The user has the choice to let the program setup everything by default or they can interact with the program to setup the settings themselves if they do it this way the program uses meaningful messages and are notified of any times where they may have to wait longer than expected.
