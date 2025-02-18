import os
import sys
import json
import pyperclip
import time
from cryptography.fernet import Fernet
from classes.credential import Credential

cred_file = "credentials.json"
key_file = "encryption_key.key"
list_of_creds = []

def load_key(key_file):
    global enc_key
    with open(key_file, "rb") as file:
        enc_key = file.read()
    
def load_creds():
    global list_of_creds
    if os.path.exists(cred_file):
        with open(cred_file, "r") as file:
            try:
                list_of_creds = [Credential(**cred) for cred in json.load(file)]
            except json.decoder.JSONDecodeError:
                print("Warning: The credentials file is empty or contains invalid JSON. Returning an empty list.")
                list_of_creds = []
    else:
        list_of_creds = []

def create_cred(cred_to_create):
    os.system('cls' if os.name == 'nt' else 'clear')
    fernet = Fernet(enc_key)

    print(f"Credential name: {cred_to_create}")
    fields = {}
    while True:
        field_name = input("\nEnter the field name or press Enter to create: ")
        if len(field_name) == 0:
            break
        value = input(f"Enter the value for {field_name}: ")
        encrypted_value = fernet.encrypt(value.encode()).decode()
        fields[field_name] = encrypted_value

    if len(fields) == 0:
        #go up one line
        sys.stdout.write("\033[F")
        input("You cannot create a credential with 0 fields. Press Enter to continue...")
        return
    new_cred = Credential(cred_to_create, **fields)
    list_of_creds.append(new_cred)

    os.system('cls' if os.name == 'nt' else 'clear')
    input(f"Created credential: {new_cred.credential_name}.\n\nPress Enter to continue...")
    for key, value in new_cred.__dict__.items():
        if key != "cred":
            print(f"{key}: {value}")

    # sort and save the updated list to the JSON file
    list_of_creds.sort(key=lambda x: x.credential_name)
    with open(cred_file, "w") as file:
        json.dump([cred.__dict__ for cred in list_of_creds], file, indent=4)

def read_cred():
    os.system('cls' if os.name == 'nt' else 'clear')
    search_term = input("Enter a credential name or Ctrl+C to exit: ")
    os.system('cls' if os.name == 'nt' else 'clear')
    matching_creds = [cred for cred in list_of_creds if search_term.lower() in cred.credential_name.lower()]
    
    if not matching_creds:
        print(f"\"{search_term}\" not found.\n")
        choice = input("Would you like to create this credential? (yes/no): ").strip().lower()
        if choice == "yes":
            create_cred(search_term)
        elif choice == "no":
            return None
        else:
            print("Invalid choice. Returning to main menu.")
        return None

    if len(matching_creds) == 1:
        selected_cred = matching_creds[0]
        print(f"Found: {selected_cred.credential_name}")
        for key, value in selected_cred.__dict__.items():
            if key != "credential_name":
                print(f"{key}: {value}")
        input("\nPress Enter to continue...")

        sys.stdout.write("\033[F") # move cursor up one line to clear input statement
        action = input("Would you like to edit, delete, or copy this credential to clipboard? (edit/delete/copy): ").strip().lower()
        if action == "edit":
            upd_cred(selected_cred)
        elif action == "delete":
            del_cred(selected_cred)
        elif action == "copy":
            fernet = Fernet(enc_key)
            for key, value in selected_cred.__dict__.items():
                if key != "credential_name":
                    value = fernet.decrypt(value.encode()).decode()
                    pyperclip.copy(value)
                    time.sleep(0.25)
            os.system('cls' if os.name == 'nt' else 'clear')
            input(f"\n{selected_cred.credential_name} credentials have been copied to clipboard. You can use WindowsKey+V to view and paste them!"
                  "\n\nPress Enter to continue, or press Ctrl+C to leave the program...")
        else:
            print("Invalid choice. No action taken.")
        return selected_cred

    # select cred if multiple results are found
    print("Matching credentials:")
    for i, cred in enumerate(matching_creds, 1):
        print(f"{i}. {cred.credential_name}")
    
    print("\nAlternative options:")
    print(f"{len(matching_creds) + 1}. Return to menu")
    print(f"{len(matching_creds) + 2}. Create new credential")

    choice = input(f"\nSelect the credential you want to view (1-{len(matching_creds) + 2}): ")
    os.system('cls' if os.name == 'nt' else 'clear')

    if choice.isdigit():
        choice = int(choice)
        if 1 <= choice <= len(matching_creds):
            selected_cred = matching_creds[choice - 1]
            print(f"Selected credential: {selected_cred.credential_name}")
            for key, value in selected_cred.__dict__.items():
                if key != "credential_name":
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
                    if key != "credential_name":
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
            create_cred(search_term)
        else:
            print("Invalid choice. No credential selected.")
            return None
    else:
        print("Invalid choice. No credential selected.")
        return None

def upd_cred(cred):
    os.system('cls' if os.name == 'nt' else 'clear')
    fernet = Fernet(enc_key)
    fields = list(cred.__dict__.keys())

    print("Choose an action:")
    print("1. Update field(s)")
    print("2. Add new field")
    print("3. Remove a field")
    menu_choice = input("Enter your choice: ")
    sys.stdout.write("\033[4F")  # move cursor up one line to clear input statement

    if menu_choice == '1' or menu_choice == 'update':
        print("Choose a field to update or type 'all' to update all fields:")
        for i, field in enumerate(fields, 1):
            print(f"{i}. {field}")
        choice = input(f"Enter your choice (1-{len(fields)} or 'all'): ")

        if choice.isdigit() and 1 <= int(choice) <= len(fields):
            field = fields[int(choice) - 1]
            new_value = input(f"Enter new value for {field}: ")
            if field != "credential_name":
                encrypted_value = fernet.encrypt(new_value.encode()).decode()
                setattr(cred, field, encrypted_value)
            else:
                setattr(cred, field, new_value)
        elif choice.lower() == 'all':
            os.system('cls' if os.name == 'nt' else 'clear')
            for field in fields:
                new_value = input(f"Enter new value for {field}: ")
                if field != "credential_name":
                    encrypted_value = fernet.encrypt(new_value.encode()).decode()
                    setattr(cred, field, encrypted_value)
                else:
                    setattr(cred, field, new_value)
        else:
            print("Invalid choice. No updates made.")

    elif menu_choice == '2':
        os.system('cls' if os.name == 'nt' else 'clear')
        new_field = input("Enter the name of the new field: ")
        new_value = input(f"Enter the value for {new_field}: ")
        encrypted_value = fernet.encrypt(new_value.encode()).decode()
        setattr(cred, new_field, encrypted_value)

    elif menu_choice == '3':
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Choose a field to remove:")
        for i, field in enumerate(fields, 1):
            print(f"{i}. {field}")
        choice = input(f"Enter your choice (1-{len(fields)}): ")

        if choice.isdigit() and 1 <= int(choice) <= len(fields):
            field = fields[int(choice) - 1]
            if field != "credential_name":
                delattr(cred, field)
                print(f"Field '{field}' removed successfully.")
            else:
                print("Cannot remove 'credential_name' field.")
        else:
            print("Invalid choice. No fields removed.")
            input("\nPress Enter to continue...")

    else:
        print("Invalid choice. No updates made.")

    # clear and reprint updated cred
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Updated credential: {cred.credential_name}")
    for key, value in cred.__dict__.items():
        if key != "credential_name":
            print(f"{key}: {value}")
    input("\nSuccessfully updated. Press Enter to continue...")
    
    # save the updated list to the JSON file
    list_of_creds.sort(key=lambda x: x.credential_name)
    with open(cred_file, "w") as file:
        json.dump([cred.__dict__ for cred in list_of_creds], file, indent=4)

def del_cred(cred):
    os.system('cls' if os.name == 'nt' else 'clear')
    confirm = input(f"Are you sure you want to delete the credential '{cred.credential_name}'? (yes/no): ").strip().lower()
    if confirm == "yes":
        list_of_creds.remove(cred)
        with open(cred_file, "w") as file:
            json.dump([cred.__dict__ for cred in list_of_creds], file, indent=4)
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Credential '{cred.credential_name}' deleted successfully.")
        input("\nPress Enter to continue...")
    else:
        print("Deletion canceled.")
        input("\nPress Enter to continue...")

# Prep the key and json data
load_key(key_file)
load_creds()