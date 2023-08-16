import base64
import os
from typing import Union

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import aead
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from packages.ErrorHandler import ErrorHandler


class KeyManager:
    @classmethod
    def generate_key(cls) -> bytes:
        return Fernet.generate_key()

    @classmethod
    def is_valid_key(cls, key: bytes) -> bool:
        try:
            Fernet(key)
            return True
        except ValueError:
            return False

    @classmethod
    def create_key(cls, password: str, salt: bytes) -> bytes:
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,  # HKDF can use a salt, but it's optional
            info=None,
            backend=default_backend()
        )
        derived_key = hkdf.derive(password.encode())
        return derived_key

    @classmethod
    def save_key(cls, key: bytes, password: str, path: str) -> None:
        salt = os.urandom(16)
        derived_key = cls.create_key(password, salt)
        aesgcm = aead.AESGCM(derived_key)
        nonce = os.urandom(12)
        encrypted_key = aesgcm.encrypt(nonce, key, None)
        with open(path, 'wb') as f:
            f.write(salt + nonce + encrypted_key)

    @classmethod
    def load_key(cls, password: str, path: str) -> Union[bytes, None]:
        if os.path.getsize(path) > 10E6:
            ErrorHandler.invalid_key_error()
            raise Exception("Error")
        with open(path, 'rb') as f:
            data = f.read()
        salt, nonce, encrypted_key = data[:16], data[16:28], data[28:]
        derived_key = cls.create_key(password, salt)
        aesgcm = aead.AESGCM(derived_key)
        decrypted_key = aesgcm.decrypt(nonce, encrypted_key, None)
        return base64.urlsafe_b64encode(decrypted_key)
