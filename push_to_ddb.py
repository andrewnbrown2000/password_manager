import boto3
import json

# Initialize a session using Amazon DynamoDB
dynamodb = boto3.client('dynamodb')

# Define the table name
table_name = "ab_cred_table"

def push_to_ddb(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    for item in data:
        cred_name = item.pop('credential_name').lower()
        
        attributes_json = json.dumps(item)
        
        ddb_item = {
            'cred_name': {'S': cred_name},
            'account_id': {'N': '0'},
            'attributes': {'S': attributes_json}
        }
        
        dynamodb.put_item(TableName=table_name, Item=ddb_item)
        print(f"Inserted credential: {cred_name}")

if __name__ == "__main__":
    push_to_ddb(r"backup\encrypted_backup_credentials2.json")

