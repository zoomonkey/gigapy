import boto3
import datetime
from configparser import ConfigParser

parser = ConfigParser()
parser.read('config.ini')

mk = str(parser.get('myconfig', 'key'))
ms = str(parser.get('myconfig', 'secret'))

now = datetime.datetime.now()

client = boto3.client(
    's3',
    aws_access_key_id=mk,
    aws_secret_access_key=ms
)
client.upload_file('output.log','gigaoutput','gigaoutput' + str(now.month) + '-' + str(now.day))
