import json
from cryptography.fernet import Fernet

# Load the encryption key
with open("encryption_key.key", "rb") as key_file:
    enc_key = key_file.read()

fernet = Fernet(enc_key)

# Load the backup credentials
with open("backup/backup_credentials.json", "r") as backup_file:
    backup_credentials = json.load(backup_file)

# Encrypt the attributes
encrypted_credentials = []
for cred in backup_credentials:
    encrypted_cred = {}
    for key, value in cred.items():
        if key == "credential_name":
            encrypted_cred[key] = value
        else:
            encrypted_cred[key] = fernet.encrypt(value.encode()).decode()
    encrypted_credentials.append(encrypted_cred)

# Save the encrypted credentials to a new file
with open("backup/encrypted_backup_credentials2.json", "w") as encrypted_file:
    json.dump(encrypted_credentials, encrypted_file, indent=4)

print("Encryption complete. Encrypted credentials saved to 'backup/encrypted_backup_credentials2.json'.")