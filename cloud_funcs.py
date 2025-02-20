import os
import sys
import json
import pyperclip
import time
from classes.credential import Credential

from cryptography.fernet import Fernet
key_file = "encryption_key.key"

#load ddb
import boto3
dynamodb = boto3.client('dynamodb')
table_name = "ab_cred_table"

def load_key(key_file):
    global enc_key
    with open(key_file, "rb") as file:
        enc_key = file.read()

def create_new_cred(new_cred_name):
    os.system('cls' if os.name == 'nt' else 'clear')
    fernet = Fernet(enc_key)

    print(f"Credential name: {new_cred_name}")

    fields = {}
    while True:
        field_name = input("\nEnter the field name or press Enter to create: ").lower()
        if len(field_name) == 0:
            break
        value = input(f"Enter the value for the {field_name}: ")
        encrypted_value = fernet.encrypt(value.encode()).decode()
        fields[field_name] = encrypted_value

    if len(fields) == 0:
        #go up one line
        sys.stdout.write("\033[F")
        input("You cannot create a credential with 0 fields. Press Enter to continue...")
        return
    new_cred = Credential(new_cred_name, **fields)
    convert_and_put_to_ddb(new_cred, '0')

    os.system('cls' if os.name == 'nt' else 'clear')

    input(f"Created credential: {new_cred.credential_name}.\n\nPress Enter to continue...")
    for key, value in new_cred.__dict__.items():
        if key != "cred":
            print(f"{key}: {value}")

def read_cred():
    os.system('cls' if os.name == 'nt' else 'clear')
    user_rq_cred = input("Enter a credential name or Ctrl+C to exit: ")
    os.system('cls' if os.name == 'nt' else 'clear')
    matching_creds = scan_db(user_rq_cred)

    #if search returns 0 items, ask to create the requested cred
    if not matching_creds:
        print(f"\"{user_rq_cred}\" not found.\n")
        choice = input(f"Would you like to store {user_rq_cred}? (yes/no): ").strip().lower()
        if choice[0] == 'y':
            create_new_cred(user_rq_cred)
        else:
            read_cred()

#find items with cred_name containing search_item
def scan_db(search_item):
    response = dynamodb.scan(
        TableName=table_name,
        FilterExpression='contains(cred_name, :cred_name)',
        ExpressionAttributeValues={
            ':cred_name': {'S': search_item.lower()}
        }
    )
    return response.get('Items', [])

def convert_and_put_to_ddb(cred, acc_id):
    cred_name = cred.credential_name.lower()
    attributes = {key: value for key, value in cred.__dict__.items() if key != "credential_name"}
    
    #convert attributes to JSON string
    attributes_json = json.dumps(attributes)
    
    #create the item dictionary
    item = {
        'cred_name': {'S': cred_name},
        'account_id': {'N': acc_id},
        'attributes': {'S': attributes_json}
    }
    
    #put to DynamoDB
    dynamodb.put_item(TableName=table_name, Item=item)
    print(f"Inserted credential: {cred_name}")
    

#load the encryption key
load_key(key_file)
