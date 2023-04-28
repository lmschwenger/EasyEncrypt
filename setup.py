from setuptools import setup, find_packages

setup(
    name='EasyEncrypt',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        "cryptography",
        "PyQt6"
        # Add any package dependencies here
    ],
    entry_points={
        # Add any command-line scripts here
    }
)
