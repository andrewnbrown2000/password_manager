import json
import boto3
from classes.credential import Credential

#load ddb
dynamodb = boto3.client('dynamodb')
table_name = "ab_cred_table"
creds_converted = []

#variables
cred_file = "credentials.json"

#convert json to list
with open(cred_file, "r") as file:
    cred_list = json.load(file)

#convert list items to objects. primarily for uniformity
for cred in cred_list:
    cred_name = cred.pop("credential_name")
    cred_obj = Credential(cred_name)
    for key, value in cred.items():
        setattr(cred_obj, key, value)
    creds_converted.append(cred_obj)

for cred in creds_converted:
    cred_name = cred.name
    attributes = {key: value for key, value in cred.__dict__.items() if key != "credential_name"}
    
    # Convert attributes to JSON string
    attributes_json = json.dumps(attributes)
    
    # Create the item to be inserted into DynamoDB
    item = {
        'cred_name': {'S': cred_name.lower()},
        'account_id': {'N': '0'},
        'attributes': {'S': attributes_json}
    }
    
    # Insert the item into DynamoDB
    dynamodb.put_item(TableName=table_name, Item=item)