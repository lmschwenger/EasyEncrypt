import os

from packages.Keys import Keys
from packages.Security import Security


output_dir = os.path.join('../data', 'output')
input_dir = os.path.join('../data', 'input')

fresh_img_path = os.path.join(input_dir, 'python_file.py')
encrypted_img_path = os.path.join(output_dir, 'python_file_encrypted.py')
decrypted_img_path = os.path.join(output_dir, 'python_file_decrypted.py')


key_path = os.path.join(output_dir, 'key.pem')
key = Keys.load_key(key_path)

Security.binary_encrypt(key, fresh_img_path, encrypted_img_path)
Security.binary_decrypt(key, encrypted_img_path, decrypted_img_path)
