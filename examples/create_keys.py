import os

from packages.Keys import generate_key, save_key, load_key

output_dir = os.path.join('../data', 'output')
input_dir = os.path.join('../data', 'input')


key = generate_key()
save_key(key, os.path.join(output_dir, 'key.pem'))
