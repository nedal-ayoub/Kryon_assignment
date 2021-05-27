# Kryon AWS home assignment.

the assignment was to program two lambda functions in AWS. 
1.	First lambda function is triggered from S3 bucket when uploading a json file which contains elements that contains well-formed phone number and a text message, the function parses the elements and send them to SQS service.
2.	 Second lambda function receive all elements and send to each number SMS with the content of the message, and then add the phone number and the message content and  last time we sent SMS to  dynamo table, if an SMS was sent in the last 24 hours, then the function will not send a new SMS.

## required 
1)  Account at AWS.
2)  S3 bucket (doesn't matter the name) .
3)  SQS with name "phone-messages".
4)  DynamoDB table with name "messages" and 3 indexes "phone", "msg" , "last_SMS_date".
5) Two AWS lambda functions , choose python 3.7 as programming language.
6) permissions.

so after that you have to upload the two lambda function files( messages_sender is first lambda ,messages_receiver is second lambda )  and  put first lambda to be triggered from  s3 bucket  "PUT" event , and  put second lambda  to be triggered from SQS.   
## permissions

you have to add to messages_sender lambda the following permissions: 
1) AmazonSQSFullAccess
2) AmazonS3FullAccess
3) AWSResourceAccessManagerFullAccess

and for ,messages_receiver lambda:
1) AmazonSQSFullAccess
2) AmazonDynamoDBFullAccess
3) AmazonSNSFullAccess 
4) AWSResourceAccessManagerFullAccess

and to your user permission to execute lambda function. 
## installation
no need to install anything.  
## how to run: 
since lambda functions are triggered from diffrent services, there is no need to run lambda code , lambda code run automatically, and all what you have to do is to upload in  S3 bucket (first trigger) appropriate json file and give the user permission to read it .

## results
After uploading a JSON file to S3, the text will be sent via SMS to the related phone numbers in the file. The system will not send an  SMS to this user (phone number) if it has already sent an SMS to them within the last 24 hours. There will be a table in DynamoDB for messages that stores the phone number & the content of the message and the time of sending last SMS to the phone number .
