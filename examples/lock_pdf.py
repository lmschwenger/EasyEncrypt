import os

from packages.Keys import Keys
from packages.Security import Security


output_dir = os.path.join('../data', 'output')
input_dir = os.path.join('../data', 'input')

pdf_file = os.path.join(input_dir, 'pdf_file.pdf')
locked_pdf_file = os.path.join(output_dir, 'pdf_file_locked.pdf')
Security.lock_pdf(password='Secret Password', pdf_path=pdf_file, output_path=locked_pdf_file)
