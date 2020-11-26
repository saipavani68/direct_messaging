# CPSC 449 Web Back-End Engineering - Fall 2020
Guided by Professor: Kenytt Avery @ProfAvery
# Project description: 
In this Project, a microservice is created for private Direct Messaging between users as like in Twitter. This microservice is written as a separate Flask application connected to an instance of Amazon's DynamoDB Local.

The following are the steps to run the project:
1. Clone the github repository https://github.com/nagisettipavani/direct_messaging

2. Install the pip package manager by running the following commands:

    > sudo apt update
    
    > sudo apt install --yes python3-pip
   
3. Install Flask by:
    
    > python3 -m pip install Flask python-dotenv
   
4. Run the following commands to install Foreman and HTTPie:

    > sudo apt update
    
    > sudo apt install --yes ruby-foreman httpie
    
5. Install Amazon's DynamoDB using https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html
    When you reach Step 4, you will not be able to run aws configure until you have installed the AWS CLI. You can use the following commands:

    > sudo apt update
    
    > sudo apt install --yes awscli
    
    For configuring AWS CLI you can use the below command:
    
     > $ aws configure
     
     > AWS Access Key ID [None]: fakeMyKeyId (sample)
     
     > AWS Secret Access Key [None]: fakeSecretAccessKey (sample)
     
     > Default region name [None]: us-west-2 (sample)
     
     > Default output format [None]: table
 
6.  Install Boto3

     > sudo apt install --yes python3-boto3

7. Then cd into the directMessaging folder in another terminal(other than the dynamodb one)
    Run the following commands:
    
    > flask init (This command should also be run in gateway folder if users or timelines microservice is being used to connect to schema.db
    
    > foreman start -m gateway=1,app=3,timelines=3,directMessaging=3 (Starting an instance of gateway and 3 instances each of timelines and app)


8. Since Api Gateway is being used for redirecting requests to the respective server instances of each microservice, we can test our apis using http://localhost:5000 (for example with Postman) which further redirects requests to nodes with ports 5300, 5301, 5302 as defined in routes.cfg

