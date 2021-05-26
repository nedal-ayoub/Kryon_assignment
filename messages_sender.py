import json
import boto3

s3_service_client=boto3.client("s3")

sqs_service_client=boto3.resource("sqs")
q_name='phone-messages' #sqs bucket queue name 

# we read from event the file name and bucket name , then we get the content of the file which is json string , and we use json.loads in order to return json_objects of the elements in the file . 
def get_json_objects(event):
    filename=str(event['Records'][0]['s3']['object']['key'])
    S3_bucket_name=event['Records'][0]['s3']['bucket']['name']
    fileObject=s3_service_client.get_object(Bucket=S3_bucket_name ,Key=filename)
    file_content= fileObject["Body"].read().decode('utf-8')
    json_objects=json.loads(file_content)
    return json_objects

#sending messages we read from json file to sqs with name phone-message
def send_messages(json_objects):
    queue = sqs_service_client.get_queue_by_name(QueueName=q_name)
    for object in json_objects:
        queue.send_message(MessageBody=json.dumps(object))
    return
    
def lambda_handler(event, context):
    json_objects=get_json_objects(event)
    send_messages(json_objects)
    return 
    