from cryptography.fernet import Fernet


# key generation
def keygen():
    try:
        key = Fernet.generate_key()

        # string the key in a file
        with open('file.key', 'wb') as file_key:
            file_key.write(key)
        return True
    except Exception as e:
        print(e)
        return False


# read key file
def read_key():
    try:
        with open('file.key', 'rb') as file_key:
            key = file_key.read()
        return key
    except Exception as e:
        print(e)
        return False


# encrypt file
def encrypt_file():
    key = read_key()
    if not key:
        return False
    fernet = Fernet(key)

    try:
        with open('nba.csv', 'rb') as file:
            original = file.read()
        encrypted = fernet.encrypt(original)

        # opening file in write mode and writing encrypted data
        with open('nba.csv', 'wb') as encrypted_file:
            encrypted_file.write(encrypted)
        return True
    except Exception as e:
        print(e)
        return False


# decrypt file
def decrypt_file():
    # read key
    key = read_key()
    if not key:
        return False
    fernet = Fernet(key)

    try:

        with open('nba.csv', 'rb') as file:
            encrypted = file.read()

        # decrypting the file
        decrypted = fernet.decrypt(encrypted)

        # opening the file in write mode and
        # writing the decrypted data
        with open('nba.csv', 'wb') as decrypted_file:
            decrypted_file.write(decrypted)
        return True
    except Exception as e:
        print(e)
        return False
