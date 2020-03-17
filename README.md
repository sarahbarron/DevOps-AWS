
## Developer OperationsAssignment1. 

### Core assignment specification

The overall objective of this assignment is to automate using Python 3 the process of creating, 
launching and monitoring a public-facing web server in the Amazon cloud. 
The web server will run on an EC2 instance and display some static content that is stored in S3. 
The program that does this must be called run_newwebserver.py


More detailed specification:
- Firstly,your Python program should create and launch a new Amazon EC2 nanoinstance. You must use the boto3 API library to launch from a free tier Amazon Linux AMI. Use an up-to-date AMI version. You will need to have your Amazon credentials in aconfiguration file (~/.aws/credentials) and not in the Python code. 
- Ensure your programlaunches the instance into an appropriate security group (you can optionally create one programmatically) and is accessible using your SSH key.
- You should provide a “User Data”start-up script when creating the instance. This start-up script should apply any required patches to the operating system and then install the web server(e.g. Apache).
- Another core requirement is that you write Python 3 code to create an S3 bucket and copy an image up to this bucket. We will make this image available at http://devops.witdemo.net/image.jpg .The image at this URL will change so your code will need to handle this in a generic manner. Your webserver main (home) page should then be configured so that this image will be visible (and loaded from yourownS3 URL)by a browser visiting the website. 
- You must use ssh remote command executionto use curl or equivalent to retrieve a piece of information from instance metadata(e.g. availability zone or subnet) and display it on the web server home page with the image. You will need to use the public IP address or DNS name assigned to your instance to connect to it using ssh. 
- Use boto to monitor a selection of EC2 and/or S3 metrics using Cloudwatch. 
- Your code should perform appropriate error handling (using exceptions) and output meaningful messages to the user. Implement logging functionality so that details of what is happening (whether normal or errors) can be written to the console or a file.

### Some additional functionality
The above is the core assignment specification. In addition you are expected to explore one or more other tasks. The following would be reasonable examples:
- Configure other services remotely
- Pass parameters as command line arguments
- Query web server access/error logs using grep or equivalent
- Expand on the CloudWatch monitoring step to take some action –for example create and start another instance automatically if some threshold is exceeded
- Monitor resource usage using customCloudwatch metrics (e.g. websitepage views)
### Non-functional issues: readability, robustness, user-friendliness
As well as for core functionality and testing, marks will be awarded for:
- Testing –for example using Python’s unittest module or alternatives.
- Script readability –it helps to have good code comments, appropriate code layout/spacing, and good variable and function names.
- Robustness –how the script deals with error conditions and unexpected situations.
- User-friendliness of the scripts –meaningful messages provided to user andopportunities for user interaction.


