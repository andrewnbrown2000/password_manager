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

    input(f"Created credential: {new_cred.name}\n\nPress Enter to continue...")
    for key, value in new_cred.__dict__.items():
        if key != "cred":
            print(f"{key}: {value}")

def create_dup_cred(dup_cred_name):
    input("\ncreate_dup_cred\n")

def read_cred():
    os.system('cls' if os.name == 'nt' else 'clear')
    user_rq_cred = input("Enter a credential name or Ctrl+C to exit: ")
    os.system('cls' if os.name == 'nt' else 'clear')
    matching_creds = scan_db(user_rq_cred)
    matching_creds = items_to_objs(matching_creds)

    #if search returns 0 items, ask to create the requested cred
    if not matching_creds:
        print(f"\"{user_rq_cred}\" not found.\n")
        choice = input(f"Would you like to store {user_rq_cred}? (yes/no): ").strip().lower()
        if choice[0] == 'y':
            create_new_cred(user_rq_cred)
            return
        else:
            return
    #if search returns 1 item
    elif len(matching_creds) == 1:
        selected_cred = matching_creds[0]
        print(f"Found: {selected_cred.name}")
        for key, value in selected_cred.__dict__.items():
            if key != "name":
                print(f"{key}: {value}")

        #user decides what to do with found cred
        action = input("\nWould you like to edit, delete, or copy this credential to clipboard? (edit/delete/copy): ").strip().lower()
        if action == "edit":
            upd_cred(selected_cred)
        elif action == "delete":
            del_cred(selected_cred)
        elif action == "copy":
            fernet = Fernet(enc_key)
            for key, value in selected_cred.__dict__.items():
                if key != "name":
                    value = fernet.decrypt(value.encode()).decode()
                    pyperclip.copy(value)
                    time.sleep(0.25)
            os.system('cls' if os.name == 'nt' else 'clear')
            input(f"\n{selected_cred.name} credentials have been copied to clipboard. You can use WindowsKey+V to view and paste them!"
                    "\n\nPress Enter to continue, or press Ctrl+C to leave the program...")
        else:
            print("Invalid choice. No action taken.")
        return selected_cred
    #if search returns multiple results
    elif len(matching_creds) > 1:
        print("Matching credentials:")
    for i, cred in enumerate(matching_creds, 1):
        print(f"{i}. {cred.name}")
    
    print("\nAlternative options:")
    print(f"{len(matching_creds) + 1}. Return to menu")
    print(f"{len(matching_creds) + 2}. Create new credential")

    choice = input(f"\nSelect the credential you want to view (1-{len(matching_creds) + 2}): ")
    os.system('cls' if os.name == 'nt' else 'clear')

    if choice.isdigit():
        choice = int(choice)
        if 1 <= choice <= len(matching_creds):
            selected_cred = matching_creds[choice - 1]
            print(f"Selected credential: {selected_cred.name}")
            for key, value in selected_cred.__dict__.items():
                if key != "name":
                    print(f"{key}: {value}")
            input("\nPress Enter to continue...")
            sys.stdout.write("\033[F")  # move cursor up one line to clear input statement

            action = input("Would you like to edit, delete, or copy this credential to clipboard? (edit/delete/copy): ").strip().lower()
            if action == "edit":
                upd_cred(selected_cred)
            elif action == "delete":
                del_cred(selected_cred)
            elif action == "copy":
                fernet = Fernet(enc_key)
                for key, value in selected_cred.__dict__.items():
                    if key != "name":
                        value = fernet.decrypt(value.encode()).decode()
                        pyperclip.copy(value)
                        time.sleep(0.25)
                sys.stdout.write("\033[2F")
                input("\nCredential attributes copied to clipboard. You can use win+v to view and select them!\n\nPress Enter to continue, or press Ctrl+C to leave the program...")
            else:
                print("Invalid choice. No action taken.")
            return selected_cred
        elif choice == len(matching_creds) + 1:
            print("Returning to main menu.")
            return None
        elif choice == len(matching_creds) + 2:
            create_dup_cred(user_rq_cred)
        else:
            print("Invalid choice. No credential selected.")
            return None
    else:
        print("Invalid choice. No credential selected.")
        return None

#find items with name containing search_item
def scan_db(search_item):
    response = dynamodb.scan(
        TableName=table_name,
        FilterExpression='contains(cred_name, :cred_name)',
        ExpressionAttributeValues={
            ':cred_name': {'S': search_item.lower()}
        }
    )
    return response.get('Items', [])

#convert all found ddb items to objects
def items_to_objs(items):
    credentials = []
    for item in items:
        attributes = json.loads(item['attributes']['S'])
        credentials.append(Credential(item['cred_name']['S'], **attributes))
    return credentials

def convert_and_put_to_ddb(cred, acc_id):
    name = cred.name.lower()
    attributes = {key: value for key, value in cred.__dict__.items() if key != "name"}
    
    #convert attributes to JSON string
    attributes_json = json.dumps(attributes)
    
    #create the item dictionary
    item = {
        'cred_name': {'S': name},
        'account_id': {'N': acc_id},
        'attributes': {'S': attributes_json}
    }
    
    #put to DynamoDB
    dynamodb.put_item(TableName=table_name, Item=item)
    print(f"Inserted credential: {name}")
    
def upd_cred(cred):
    os.system('cls' if os.name == 'nt' else 'clear')
    fernet = Fernet(enc_key)
    print(f"Updating credential: {cred.name}")

    fields = {}
    for key, value in cred.__dict__.items():
        if key != "name":
            decrypted_value = fernet.decrypt(value.encode()).decode()
            new_value = input(f"Enter new value for the '{key}' (press Enter to skip or type 'DELETE' to remove the field): ")
            if new_value == "DELETE":
                continue  # Skip adding this field to the updated credential
            elif new_value:
                encrypted_value = fernet.encrypt(new_value.encode()).decode()
                fields[key] = encrypted_value
            else:
                fields[key] = value
        #ask user to add new fields or skip
    choice = input("\nWould you like to add a new field? (yes/no): ")
    if choice.lower()[0] == 'y':
        while True:
            field_name = input("\nEnter the field name or press Enter to create: ").lower()
            if len(field_name) == 0:
                break
            value = input(f"Enter the value for the {field_name}: ")
            encrypted_value = fernet.encrypt(value.encode()).decode()
            fields[field_name] = encrypted_value

    updated_cred = Credential(cred.name, **fields)
    convert_and_put_to_ddb(updated_cred, '0')

    os.system('cls' if os.name == 'nt' else 'clear')
    input(f"Updated credential: {updated_cred.name}\n\nPress Enter to continue...")
    for key, value in updated_cred.__dict__.items():
        if key != "cred":
            print(f"{key}: {value}")

def del_cred(cred):
    dynamodb.delete_item(
        TableName=table_name,
        Key={
            'cred_name': {'S': cred.name.lower()},
            'account_id': {'N': '0'}
        }
    )
    os.system('cls' if os.name == 'nt' else 'clear')
    input(f"Deleted credential: {cred.name}\n\nPress Enter to continue...")

#load the encryption key
load_key(key_file)
