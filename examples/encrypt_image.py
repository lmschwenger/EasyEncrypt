import os

from packages.Keys import Keys
from packages.Security import Security


output_dir = os.path.join('../data', 'output')
input_dir = os.path.join('../data', 'input')

fresh_img_path = os.path.join(input_dir, 'test_image.png')
encrypted_img_path = os.path.join(output_dir, 'img_encrypted.png')
decrypted_img_path = os.path.join(output_dir, 'img_decrypted.png')


key_path = os.path.join(output_dir, 'key.pem')
key = Keys.load_key(key_path)

Security.encrypt_image(key, fresh_img_path, encrypted_img_path)
Security.decrypt_image(key, encrypted_img_path, decrypted_img_path)
