# filepath: /c:/Users/andy/Documents/Projects/Python/Encryption/main.py
import os
from funcs import *


def main():
    key_file = "encryption_key.key"

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # clear console
        load_creds()
        print("Choose an action:")
        print("1. Store a credential")
        print("2. View a credential")
        print("3. Exit")
        choice = input("Enter your choice: ").strip().lower()
        
        if choice == '1' or choice == 'store':
            os.system('cls' if os.name == 'nt' else 'clear')
            create_cred()
        elif choice == '2' or choice == 'view':
            os.system('cls' if os.name == 'nt' else 'clear')
            read_cred()
        elif choice == '3' or choice == 'exit':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()