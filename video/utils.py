from cryptography.fernet import Fernet
from moviepy.editor import *


# key generation
def keygen():
    try:
        key = Fernet.generate_key()
        return key
    except Exception as e:
        print(e)
        return False


# encrypt file
def encrypt_file(key):
    fernet = Fernet(key)

    try:
        with open('test.mp4', 'rb') as file:
            original = file.read()
        encrypted = fernet.encrypt(original)

        # opening file in write mode and writing encrypted data
        with open('test.mp4', 'wb') as encrypted_file:
            encrypted_file.write(encrypted)
        return True
    except Exception as e:
        print(e)
        return False


# decrypt file
def decrypt_file(key):
    fernet = Fernet(key)

    try:

        with open('test.mp4', 'rb') as file:
            encrypted = file.read()

        # decrypting the file
        decrypted = fernet.decrypt(encrypted)

        # opening the file in write mode and
        # writing the decrypted data
        with open('test.mp4', 'wb') as decrypted_file:
            decrypted_file.write(decrypted)
        return True
    except Exception as e:
        print(e)
        return False


def add_watermark():
    try:
        video = VideoFileClip('test.mp4')
        watermark = ImageClip('watermark.png').set_duration(video.duration)
        final = CompositeVideoClip([video, watermark])
        final.write_videofile('test.mp4')
        return True
    except Exception as e:
        print(e)
        return False
