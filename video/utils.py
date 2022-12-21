from cryptography.fernet import Fernet


# key generation
def key_gen():
    key = Fernet.generate_key()

    # string the key in a file
    with open('file.key', 'wb') as file_key:
        file_key.write(key)
    return True
