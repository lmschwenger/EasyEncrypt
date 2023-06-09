# EasyEncrypt

EasyEncrypt is a simple encryption and decryption tool.

The tool uses the `cryptography` library. Encryption is done by reading any file as binary and encrypt the content with a secret key using `cryptography.fernet.Fernet`
#### NB: 
When encrypting, the original file will still exist untouched by the program!

## Installation

To install the application, clone this repository and run the following command in the root directory:

`pip -e install .`
## Usage

To launch the application, run the following command in the root directory:

`python ./app/freeze/easy_encrypt.py`

## Building

To build the application as a standalone executable, navigate to the `app/freeze` directory and run the following command:

`pyinstaller ./app/freeze/easy_encrypt.spec`

This will generate a standalone executable in the `./dist/` directory.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
