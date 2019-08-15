import boto3
import datetime

now = datetime.datetime.now()

client = boto3.client(
    's3',
    aws_access_key_id='AKIA6BX4WBMPBRX5OTIF',
    aws_secret_access_key='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'
)
client.upload_file('output.log','gigaoutput','gigaoutput' + str(now.month) + '-' + str(now.day))