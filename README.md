# EasyEncrypt

EasyEncrypt is a simple encryption and decryption tool.

The tool uses the `cryptography` library. Encryption is done by reading any file as binary and encrypt the content with a secret key using `cryptography.fernet.Fernet`

## Installation

To install the application, clone this repository and run the following command in the root directory:

`pip -e install .`
## Usage

To launch the application, run the following command in the root directory:

`pyinstaller ./app/freeze/easy_encrypt.spec`

## Building

To build the application as a standalone executable, navigate to the `app/freeze` directory and run the following command:


This will generate a standalone executable in the `app/freeze/dist` directory.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
