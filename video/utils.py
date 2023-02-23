import base64
import hashlib
import random
import datetime
import aws_encryption_sdk
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from aws_encryption_sdk.key_providers.raw import RawMasterKeyProvider
from aws_encryption_sdk.identifiers import Algorithm, CommitmentPolicy, EncryptionKeyType, WrappingAlgorithm
from aws_encryption_sdk.internal.crypto.wrapping_keys import WrappingKey
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from moviepy.editor import *
from video.models import Product, KeyStorage


# key generation
# generate a unique key
# generate aes (advcanced encryption standard) key
class StaticRandomMasterKeyProvider(RawMasterKeyProvider):
    """Randomly generates and provides 4096-bit RSA keys consistently per unique key id."""

    provider_id = "static-random"

    def __init__(self, **kwargs):  # pylint: disable=unused-argument
        """Initialize empty map of keys."""
        self._static_keys = {}

    def _get_raw_key(self, key_id):
        """Retrieves a static, randomly generated, RSA key for the specified key id.

        :param str key_id: User-defined ID for the static key
        :returns: Wrapping key that contains the specified static key
        :rtype: :class:`aws_encryption_sdk.internal.crypto.WrappingKey`
        """
        try:
            static_key = self._static_keys[key_id]
        except KeyError:
            private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096, backend=default_backend())
            static_key = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
            self._static_keys[key_id] = static_key
        return WrappingKey(
            wrapping_algorithm=WrappingAlgorithm.RSA_OAEP_SHA1_MGF1,
            wrapping_key=static_key,
            wrapping_key_type=EncryptionKeyType.PRIVATE,
        )


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
        master_key_provider = StaticRandomMasterKeyProvider()
        master_key_provider.add_master_key(derived_key)

        if Product.objects.filter(encryptor=derived_key).exists():
            keygen()
        return master_key_provider
    except Exception as e:
        print(e)
        return False


def numeric_keygen(quantity):
    key_list = []
    for i in range(quantity):
        time_stamp = str(datetime.datetime.timestamp(datetime.datetime.now()))
        time_list = time_stamp.split('.')
        random_num = random.randint(0, 999)
        random_str = str(random_num).zfill(3)
        data = time_list[0] + random_str
        hasher = hashlib.sha256()
        hasher.update(data.encode())
        key = int(hasher.hexdigest(), 16) % 1000000000000
        key = str(key).zfill(12)
        if KeyStorage.objects.filter(key=key).exists():
            numeric_keygen(quantity)
        key_list.append({"key": key, "time_stamp": time_stamp})
    return key_list


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


def get_date():
    return datetime.date.today()

