from cryptography.fernet import Fernet

def load_key(key_file_path):
    """Load the key from the specified file."""
    with open(key_file_path, 'rb') as key_file:
        key = key_file.read()
    return key

def decrypt_string(encrypted_string, key):
    """Decrypt the given string using the provided key."""
    fernet = Fernet(key)
    decrypted_string = fernet.decrypt(encrypted_string.encode()).decode()
    return decrypted_string

if __name__ == "__main__":
    key_file_path = 'encryption_key.key'
    encrypted_string = ''  # Replace with your encrypted string

    key = load_key(key_file_path)
    decrypted_string = decrypt_string(encrypted_string, key)
    print(f"Decrypted string: {decrypted_string}")