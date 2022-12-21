from cryptography.fernet import Fernet


# key generation
def key_gen():
    key = Fernet.generate_key()

    # string the key in a file
    with open('file.key', 'wb') as file_key:
        file_key.write(key)

    fernet = Fernet(key)

    with open('nba.csv', 'rb') as file:
        original = file.read()

    encrypted = fernet.encrypt(original)

    # opening the file in write mode and
    # writing the encrypted data
    with open('nba.csv', 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

    return True


def decrypt():
    # read key
    with open('file.key', 'rb') as file_key:
        key = file_key.read()

    fernet = Fernet(key)

    with open('nba.csv', 'rb') as file:
        encrypted = file.read()

    # decrypting the file
    decrypted = fernet.decrypt(encrypted)

    # opening the file in write mode and
    # writing the decrypted data
    with open('nba.csv', 'wb') as decrypted_file:
        decrypted_file.write(decrypted)
