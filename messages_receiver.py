import json
import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime, timedelta
import dateutil.tz

# using dateutil library in order to get the time of our zone and not the time of AWS region. 
Israel_region= dateutil.tz.gettz('Israel')
datetime_ist = datetime.now(tz=Israel_region)
current_date=datetime_ist.strftime('%d/%m/%Y %H:%M:%S')

sns_client= boto3.client('sns')

# declaring dynamodb client service in order to reach "messages" table and to insert to it . 
dynamodb=boto3.resource('dynamodb')
table=dynamodb.Table('messages')

# this function checks if the difference between last time  a phone number recieved SMS and this time more than 24 hours  by using timedelta from datetime library
def check_time(current_date,previous_SMS_dt):
    return (datetime.strptime(current_date,"%d/%m/%Y %H:%M:%S") - datetime.strptime(previous_SMS_dt,"%d/%m/%Y %H:%M:%S")) > timedelta(1) # using strptime to convert from string to date formate  in order to compare 
    
# inserting  phone number to the table  if not exist with message content , if it does exist then replace the message content and in the end send SMS  if required
# the function receives message paramter which is the message we read from SQS , and response the element in the messages dynamoDB table.  
def dealing_with_message(message,response):
    if response['Items']==[]: # if respone==[] then we dont have any element in the table which has same phone number , so we have to insert phone number with message content . 
        table.put_item(Item={"phone" : message["phone"] , "msg": message["msg"] ,  "last_SMS_date":current_date})
        sns_client.publish(PhoneNumber='+972'+message["phone"] , Message=message["msg"])  
    else:
        previous_SMS_dt= (response['Items'][0]).get('last_SMS_date')   #get last time we send to the phone number SMS in order to check if passed 24 hour. 
        required_SMS_send=check_time(current_date,previous_SMS_dt)
        date_to_update=current_date
        if not required_SMS_send:
            date_to_update=previous_SMS_dt
        response = table.update_item(
            Key={
                "phone": message["phone"]
            },
            UpdateExpression="set msg = :r , last_SMS_date= :s",
            ExpressionAttributeValues={
                ':r': message["msg"],
                ':s': date_to_update,
            },
            ReturnValues="UPDATED_NEW"
        )
        if required_SMS_send:
            sns_client.publish(PhoneNumber='+972'+message["phone"] , Message=message["msg"])
    return

def lambda_handler(event, context):
    messages=[]
    for object in event["Records"]:
        messages=messages+[object["body"]] # collect  messages from SQS. 
    for message in messages:
        message=json.loads(message.replace("\'","\""))
        response= table.query(KeyConditionExpression=Key('phone').eq(message["phone"])) # getting all elements from table that have the same phone number 
        dealing_with_message(message,response)
    return 