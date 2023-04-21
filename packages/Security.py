from typing import Union

import PyPDF2
from cryptography.fernet import Fernet


class Security:

    @staticmethod
    def encrypt_image(key: bytes, image_path: str, output_path: str) -> None:
        # Open the image file and read its contents
        with open(image_path, 'rb') as f:
            plaintext = f.read()

        cipher = Fernet(key)
        ciphertext = cipher.encrypt(plaintext)

        with open(output_path, 'wb') as f:
            f.write(ciphertext)

    @staticmethod
    def decrypt_image(key: bytes, image_path: str, output_path: str) -> None:
        with open(image_path, 'rb') as f:
            ciphertext = f.read()

        cipher = Fernet(key)
        plaintext = cipher.decrypt(ciphertext)

        with open(output_path, 'wb') as f:
            f.write(plaintext)

    @staticmethod
    def lock_pdf(password: str, pdf_path: str, output_path: str) -> None:
        # Open the PDF file in read-binary mode
        with open(pdf_path, 'rb') as pdf_file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            # Create a PDF writer object
            pdf_writer = PyPDF2.PdfWriter()

            # Add each page from the reader object to the writer object
            for page_num in range(len(pdf_reader.pages)):
                pdf_writer.add_page(pdf_reader.pages[page_num])

            # Encrypt the PDF file with the password
            pdf_writer.encrypt(password)

            # Save the encrypted PDF file to disk
            with open(output_path, 'wb') as encrypted_pdf:
                pdf_writer.write(encrypted_pdf)

    @staticmethod
    def unlock_pdf(password: str, pdf_path: str, output_path: str) -> Union[None, str]:
        # Open the PDF file in read-binary mode
        with open(pdf_path, 'rb') as pdf_file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            # Check if the PDF is encrypted
            if pdf_reader.is_encrypted:
                # Try to decrypt the PDF with the password
                if pdf_reader.decrypt(password) != 1:
                    return "Unable to decrypt PDF file. Incorrect password."
            else:
                return "PDF file is not encrypted."

            # Create a PDF writer object
            pdf_writer = PyPDF2.PdfWriter()

            # Add each page from the reader object to the writer object
            for page_num in range(len(pdf_reader.pages)):
                pdf_writer.addPage(pdf_reader.pages[page_num])

            # Save the decrypted PDF file to disk
            with open(output_path, 'wb') as decrypted_pdf:
                pdf_writer.write(decrypted_pdf)

            return None
