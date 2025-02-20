# Password Manager

This password manager allows you to securely store, retrieve, edit, delete, and copy passwords to the clipboard. The application uses encryption to protect your credentials and ensures that passwords are never displayed in plain text.

## Features

- **Store Credentials**: Add new credentials with encrypted fields.
- **Retrieve Credentials**: Search for credentials by name.
- **Edit/Update Credentials**: Modify existing credentials.
- **Delete Credentials**: Remove credentials from the database.
- **Copy to Clipboard**: Copy credentials to the clipboard for easy pasting into password fields.

## Future Plans

- **Synchronization and Cross-Platform Compatibility**: Enable synchronization across multiple devices.
- **UI Improvements**: Make the user interface prettier and more intuitive.
- **First Run Experience**: Enable for user's who are using for the first time to have a setup/installation experience. (i.e. implimenting pyinstaller, creating a personal key and security storing, creating and connecting to a NoSQL table, etc.)
- **Temporary Clipboard Functionality**: TTL for clipboard items

### Prerequisites

- Python 3.x
- `cryptography` library
- `pyperclip` library
- `boto3` library
- AWS account with DynamoDB setup

### Setup

```sh
# Clone the repository
git clone https://github.com/yourusername/password-manager.git
cd password-manager

# Install required libraries
pip install cryptography pyperclip boto3

# Create an encryption key
from cryptography.fernet import Fernet

key = Fernet.generate_key()
with open("encryption_key.key", "wb") as key_file:
    key_file.write(key)

# Ensure the .gitignore file includes sensitive/useless files
echo "backup/*" >> .gitignore
echo "__pycache__/*" >> .gitignore
echo "classes/__pycache__/*" >> .gitignore
echo "credentials.json" >> .gitignore
echo "encryption_key.key" >> .gitignore # DEFINITELY THIS ONE!!!
echo "run_script.sh" >> .gitignore
```

### Usage

1. Run the main script:

```sh
python main.py
```

2. Follow the on-screen prompts to manage your credentials.

### Security Considerations

- **Encryption**: All credentials are encrypted using the `cryptography` library.
- **Clipboard**: Credentials can be copied to the clipboard for easy pasting into password fields. Be cautious as this can be a security oversight.
- **Sensitive Files**: Ensure that sensitive files like `encryption_key.key` are not committed to version control.

## License

This project is licensed under the MIT License.