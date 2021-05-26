# AWS home assignment from Kryon. 

the assignment was to program two lambda function codes  in AWS , such that first lambda is triggered from S3 bucket when uploading json file witch contains elements that formed from   phone number and message, it reads  all elements and send them to  SQS , the second lambda function receive all elements and send to each number SMS with the content of the message , and then add the phone number and the message content and last time we sent SMS in dynamo table , if an SMS was sent in the last 24 hours then I  do not send a new one.

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
upload in  S3 bucket appropriate json file and give the user permission to read it . 

## results
every phone number in the json file will receive SMS with the content of the message if he didnt receive in less than 24 hours, and all the phone numbers with messages contents will be saved in messages dynamoDB table . 
