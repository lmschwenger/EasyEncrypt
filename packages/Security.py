import os.path

from PyQt6.QtWidgets import QProgressBar
from cryptography.fernet import Fernet

from packages.ErrorHandler import ErrorHandler


class Security:

    @staticmethod
    def binary_encrypt(key: bytes, input_path: str, output_dir: str, pg_bar: QProgressBar) -> bool:
        filename, ext = os.path.splitext(os.path.basename(input_path))
        chunk_size = 64 * 8196
        print(ext)
        if '.decrypted' in filename:
            output_path = input_path.replace('.decrypted', '.encrypted')
        else:
            output_path = os.path.join(output_dir, f"{filename}.encrypted{ext}")

        try:

            cipher = Fernet(key)
            input_size = os.path.getsize(input_path)

            with open(input_path, 'rb') as f_in:
                with open(output_path, 'wb') as f_out:
                    bytes_written = 0

                    while True:
                        pg_bar.show()
                        chunk = f_in.read(chunk_size)
                        if not chunk:
                            break
                        encrypted_chunk = cipher.encrypt(chunk)
                        f_out.write(encrypted_chunk)
                        bytes_written += len(encrypted_chunk)
                        progress = int(bytes_written / input_size * 100)
                        pg_bar.setValue(progress)

        except PermissionError:
            ErrorHandler.read_permission_error()
            return False
        except Exception:
            ErrorHandler.invalid_token_error()
            return False

        return True

    @staticmethod
    def binary_decrypt(key: bytes, input_path: str, output_dir: str, pg_bar: QProgressBar) -> bool:
        filename, ext = os.path.splitext(os.path.basename(input_path))
        chunk_size = 64 * 8196
        
        if '.encrypted' in filename:
            output_path = input_path.replace('.encrypted', '')
        else:
            output_path = os.path.join(output_dir, f"{filename}.decrypted{ext}")

        try:
            cipher = Fernet(key)
            input_size = os.path.getsize(input_path)

            with open(input_path, 'rb') as f_in:
                with open(output_path, 'wb') as f_out:
                    bytes_written = 0

                    while True:
                        chunk = f_in.read(chunk_size)
                        if not chunk:
                            break
                        decrypted_chunk = cipher.decrypt(chunk)
                        f_out.write(decrypted_chunk)
                        bytes_written += len(decrypted_chunk)
                        progress = int(bytes_written / input_size * 100)
                        pg_bar.setValue(progress)

        except PermissionError:
            ErrorHandler.read_permission_error()
            return False
        except Exception:
            ErrorHandler.invalid_token_error()
            return False

        return True
