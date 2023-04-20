import base64

from cryptography.fernet import Fernet


class Keys:

    @staticmethod
    def generate_key() -> bytes:
        return Fernet.generate_key()

    @staticmethod
    def save_key(key: bytes, path: str) -> None:
        with open(path, 'wb') as f:
            encoded_key = base64.urlsafe_b64encode(key)
            f.write(encoded_key)

    @staticmethod
    def load_key(path: str) -> bytes:
        with open(path, 'rb') as f:
            encoded_key = f.read()
            key = base64.urlsafe_b64decode(encoded_key)
        return key
