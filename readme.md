# Password Manager

This password manager allows you to securely store, retrieve, edit, delete, and copy passwords to the clipboard. The application uses encryption to protect your credentials and ensures that passwords are never displayed in plain text.

## Features

- **Store Credentials**: Add new credentials with encrypted fields.
- **Retrieve Credentials**: Search for credentials by name.
- **Edit/Update Credentials**: Modify existing credentials.
- **Delete Credentials**: Remove credentials from the database.
- **Copy to Clipboard**: Copy credentials to the clipboard for easy pasting into password fields.

## Future Plans

- **Cloud Sync**: Move the database to a cloud NoSQL DB to enable synchronization across multiple devices.

### Prerequisites

- Python 3.x
- `cryptography` library
- `pyperclip` library

### Setup

```sh
# Clone the repository
git clone https://github.com/yourusername/password-manager.git
cd password-manager

# Install required libraries
pip install cryptography pyperclip

# Create an encryption key
from cryptography.fernet import Fernet

key = Fernet.generate_key()
with open("encryption_key.key", "wb") as key_file:
    key_file.write(key)

# Ensure the .gitignore file includes sensitive files
echo "backup/*" >> .gitignore
echo "__pycache__/*" >> .gitignore
echo "classes/__pycache__/*" >> .gitignore
echo "credentials.json" >> .gitignore
echo "encryption_key.key" >> .gitignore
echo "run_script.sh" >> .gitignore