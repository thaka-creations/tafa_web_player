import base64
import random
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from moviepy.editor import *
from video.models import KeyStorage


# key generation
# generate a unique key
def keygen():
    try:
        key = Fernet.generate_key()
        salt = b'salt_'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        derived_key = base64.urlsafe_b64encode(kdf.derive(key))
        if KeyStorage.objects.filter(key=derived_key).exists():
            keygen()
        return derived_key
    except Exception as e:
        print(e)
        return False


# encrypt file
def encrypt_file(key):
    fernet = Fernet(key)

    try:
        with open('watermarked_video.mp4', 'rb') as file:
            original = file.read()
        encrypted = fernet.encrypt(original)

        # opening file in write mode and writing encrypted data
        with open('playing_one.mp4', 'wb') as encrypted_file:
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
        with open('playing.mp4', 'wb') as decrypted_file:
            decrypted_file.write(decrypted)
        return True
    except Exception as e:
        print(e)
        return False


def add_watermark():
    # Load the video file
    try:
        video = VideoFileClip("test.mp4")

        text_clip = (TextClip("My Watermark", fontsize=70, color='white')
                     .set_duration(video.duration)).set_opacity(0.5)

        # Define a function to return the watermark position at each frame
        def watermark_position(t):
            direction_x = 1
            direction_y = 1
            total_time = video.duration
            z = total_time - t
            total_distance_x = video.w - text_clip.w
            total_distance_y = video.h - text_clip.h
            x = (video.w / 2) + ((t / total_time) * total_distance_x * direction_x)
            y = (video.h / 2) + ((t / total_time) * total_distance_y * direction_y)

            if x < 0:
                x = (video.w / 2) + ((t / total_time) * total_distance_x * direction_x)
            elif x > video.w - text_clip.w:
                x = (video.w / 2) + ((z / total_time) * total_distance_x * direction_x)

            if y < 0:
                y = (video.h / 2) + ((t / total_time) * total_distance_y * direction_y)

            elif y > video.h - text_clip.h:
                y = (video.h / 2) + ((z / total_time) * total_distance_y * direction_y)

            return x, y
        # Add the watermark to the video
        watermarked_video = CompositeVideoClip([video, text_clip.set_pos(watermark_position)])

        # Save the watermarked video to a new file
        watermarked_video.write_videofile("watermarked_video.mp4")
        return True
    except Exception as e:
        print(e)
        return False
