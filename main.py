# filepath: /c:/Users/andy/Documents/Projects/Python/Encryption/main.py
import os
from cloud_funcs import *

key = "encryption_key.key"

def main():
    load_key(key)

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        # always search first to ensure dupe isnt made
        read_cred()


if __name__ == "__main__":
    main()