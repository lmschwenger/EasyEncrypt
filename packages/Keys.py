import base64
from typing import Union

from cryptography.fernet import Fernet

from packages.ErrorHandler import ErrorHandler


class Keys:

    @classmethod
    def generate_key(cls) -> bytes:
        return Fernet.generate_key()

    @classmethod
    def save_key(cls, key: bytes, path: str) -> None:
        with open(path, 'wb') as f:
            encoded_key = base64.urlsafe_b64encode(key)
            f.write(encoded_key)

    @classmethod
    def is_valid_key(cls, key: bytes) -> bool:
        try:
            Fernet(key)
            print("True")
            return True
        except ValueError:
            return False

    @classmethod
    def load_key(cls, path: str) -> Union[bytes, None]:
        try:
            with open(path, 'rb') as f:
                encoded_key = f.read()
                key = base64.urlsafe_b64decode(encoded_key)
                if not cls.is_valid_key(key):
                    ErrorHandler.invalid_key_error()
                    return None
        except Exception:
            ErrorHandler.invalid_key_error()
            return None
        return key
