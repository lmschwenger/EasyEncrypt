import os.path
from typing import Union

import cryptography.fernet
from cryptography.fernet import Fernet

from packages.ErrorHandler import ErrorHandler


class Security:

    @staticmethod
    def binary_encrypt(key: bytes, input_path: str, output_dir: str) -> bool:
        filename, ext = os.path.splitext(os.path.basename(input_path))

        if '.decrypted' in filename:
            output_path = os.path.join(output_dir, filename.replace('.decrypted', '') + ext)
        else:
            output_path = os.path.join(output_dir, f"{filename}.encrypted{ext}")
        try:
            with open(input_path, 'rb') as f:
                plaintext = f.read()

            cipher = Fernet(key)
            ciphertext = cipher.encrypt(plaintext)

            with open(output_path, 'wb') as f:
                f.write(ciphertext)
        except PermissionError:
            ErrorHandler.read_permission_error()
            return False
        return True

    @staticmethod
    def binary_decrypt(key: bytes, input_path: str, output_dir: str) -> bool:
        filename, ext = os.path.splitext(os.path.basename(input_path))

        if '.encrypted' in filename:
            output_path = os.path.join(output_dir, filename.replace('.encrypted', '') + ext)
        else:
            output_path = os.path.join(output_dir, f"{filename}.decrypted.{ext}")

        try:
            with open(input_path, 'rb') as f:
                ciphertext = f.read()
        except PermissionError:
            ErrorHandler.read_permission_error()
            return False

        cipher = Fernet(key)

        try:
            plaintext = cipher.decrypt(ciphertext)

            try:
                with open(output_path, 'wb') as f:
                    f.write(plaintext)
            except PermissionError:
                ErrorHandler.read_permission_error()
                return False

        except cryptography.fernet.InvalidToken:
            ErrorHandler.invalid_token_error()
            return False

        return True

