import boto3
import json
s3_client = boto3.client('s3')
dynamoDB = boto3.resource('dynamodb')
def lambda_handler(event,context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    json_file_name = event['Records'][0]['s3']['object']['key']
    json_object = s3_client.get_object(Bucket=bucket,Key=json_file_name)
    jsonFileReader = json_object['Body'].read()
    jsonDict = json.loads(jsonFileReader)
    table = dynamoDB.Table('S3-DynamoDB-Lambda')
    table.put_item(Item=jsonDict)
    return 'welcome'