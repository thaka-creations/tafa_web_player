import random
from cryptography.fernet import Fernet
from moviepy.editor import *
from video.models import KeyStorage


# key generation
# generate a unique key
def keygen():
    try:
        key = Fernet.generate_key()
        if KeyStorage.objects.filter(key=str(key).encode()).exists():
            keygen()
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
        with open('playing.mp4', 'wb') as encrypted_file:
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
            # Set the speed and direction of the movement
            speed_x = 50
            speed_y = 30
            direction_x = 1
            direction_y = -1

            # Calculate the position at the current time
            x = (video.w / 2) + (speed_x * t * direction_x)
            y = (video.h / 2) + (speed_y * t * direction_y)

            # Keep the watermark within the bounds of the screen
            if x < 0:
                x = 0
                direction_x = 1
            elif x > video.w - text_clip.w:
                x = video.w - text_clip.w
                direction_x = -1

            if y < 0:
                y = 0
                direction_y = -1
            elif y > video.h - text_clip.h:
                y = video.h - text_clip.h
                direction_y = -1

            return x, y

        # Add the watermark to the video
        watermarked_video = CompositeVideoClip([video, text_clip.set_pos(watermark_position)])

        # Save the watermarked video to a new file
        watermarked_video.write_videofile("watermarked_video.mp4")
        return True
    except Exception as e:
        print(e)
        return False
