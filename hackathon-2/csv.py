import boto3
import json
import csv

def lambda_handler(event, context):
    region = 'ap-south-1'
    record_list = []
    
    try:
        s3 = boto3.client('s3')
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('csvdynamo')
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        print('Bucket: ', bucket , 'Key: ', key)
        csv_file = s3.get_object(Bucket=bucket, Key=key)
        record_list = csv_file['Body'].read().decode('utf-8').split('\n')
        csv_reader = csv.reader(record_list,delimiter=',',quotechar='"')
        for row in csv_reader:
            id = row[0]
            name = row[1]
            yearofbirth = row[2]
        print('id: ', id,'name: ', name,'yearofbirth: ', yearofbirth)
        table.put_item(
            Item =  {
                "id":str(record_list[0]),
                "name":str(record_list[1]),
                "yearofbirth":str(record_list[2])
            }
            )
    except Exception as e:
        print(str(e))
    return {
        'statuscode': 200,
        'body':json.dumps('csv to DynamoDB success')
    }