import os
from time import sleep
from typing import List

from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, \
    QMainWindow, QMessageBox, QFileDialog, QGroupBox, QLineEdit, QListWidget, QCheckBox, QListWidgetItem

from app.gui_lamp import RoundLamp
from packages.ErrorHandler import ErrorHandler
from packages.Keys import Keys
from packages.Security import Security


class MainWin(QMainWindow):
    resource_folder = os.path.join(os.path.dirname(__file__), 'resources')
    encrypt = None

    def __init__(self):
        super().__init__()
        self.resize(600, 600)
        # Create a vertical box layout for the main window
        vbox = QVBoxLayout()

        """ 
                Cipher
        """
        cipher_layout = QVBoxLayout()
        # Cipher box
        self.gb_cipher = QGroupBox('Cipher')
        cipherkey_box = QHBoxLayout()

        self.lamp = RoundLamp()
        self.key_edit = QLineEdit()
        self.key_edit.setPlaceholderText('Key input')
        self.key_edit.setReadOnly(True)
        create_key = QPushButton('Create')
        create_key.resize(40, 20)
        create_key.clicked.connect(self.on_generate_key)
        load_key = QPushButton('Load')
        load_key.resize(40, 20)
        load_key.clicked.connect(self.set_key_path)

        settings_layout = QHBoxLayout()

        self.encrypt_button = QPushButton('Encrypt')
        self.encrypt_button.clicked.connect(self.encrypt)
        self.encrypt_button.setIconSize(QtCore.QSize(25, 64))

        self.decrypt_button = QPushButton('Decrypt')
        self.decrypt_button.clicked.connect(self.decrypt)
        self.decrypt_button.setIconSize(QtCore.QSize(20, 64))

        cipherkey_box.addWidget(self.lamp)
        cipherkey_box.addWidget(self.key_edit)
        cipherkey_box.addWidget(create_key)
        cipherkey_box.addWidget(load_key)

        settings_layout.addWidget(self.encrypt_button)
        settings_layout.addWidget(self.decrypt_button)

        cipher_layout.addLayout(cipherkey_box)
        cipher_layout.addLayout(settings_layout)
        self.gb_cipher.setLayout(cipher_layout)
        vbox.addWidget(self.gb_cipher)

        """
            Output Folder
        """

        self.gb_output = QGroupBox('Input and Output')

        dirs = QHBoxLayout()

        input_dir = QVBoxLayout()
        self.input_dir_edit = QLineEdit()
        self.input_dir_edit.setReadOnly(True)
        self.input_dir_edit.setPlaceholderText('Path to input folder')
        self.input_list = QListWidget()

        input_dir_button = QPushButton('Choose input folder')
        input_dir_button.resize(40, 20)
        input_dir_button.clicked.connect(self.set_input_folder)

        # Add the list widget to the layout
        input_dir.addWidget(input_dir_button)
        input_dir.addWidget(self.input_dir_edit)
        input_dir.addWidget(self.input_list)

        output_dir = QVBoxLayout()
        self.output_dir_edit = QLineEdit()
        self.output_dir_edit.setReadOnly(True)
        self.output_dir_edit.setPlaceholderText('Path to folder')
        self.output_list = QListWidget()

        output_dir_button = QPushButton('Choose output folder')
        output_dir_button.resize(40, 20)
        output_dir_button.clicked.connect(self.set_output_folder)

        output_dir.addWidget(output_dir_button)
        output_dir.addWidget(self.output_dir_edit)
        output_dir.addWidget(self.output_list)

        dirs.addLayout(input_dir)
        dirs.addLayout(output_dir)

        self.gb_output.setLayout(dirs)
        vbox.addWidget(self.gb_output)

        """
                Log Box
        """
        self.gb_run = QGroupBox()
        run_layout = QHBoxLayout()
        self.run = QPushButton('Run')
        self.run.setEnabled(False)
        self.run.clicked.connect(self.on_run)

        run_layout.addWidget(self.run)
        self.gb_run.setLayout(run_layout)
        vbox.addWidget(self.gb_run)

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)

    def update_input_dir_list(self):
        self.input_list.clear()
        try:
            files = os.listdir(self.input_dir_edit.text())
            # Add the files to the list widget
            for file in files:
                item = QListWidgetItem()
                checkbox = QCheckBox()
                checkbox.setText(file)
                self.input_list.addItem(item)
                self.input_list.setItemWidget(item, checkbox)
        except FileNotFoundError:
            self.input_list.clear()

    def update_output_dir_list(self):
        self.output_list.clear()
        try:
            files = os.listdir(self.output_dir_edit.text())
            # Add the files to the list widget
            for file in files:
                self.output_list.addItem(file)
        except FileNotFoundError:
            self.output_list.clear()

    def set_output_folder(self):
        url = QFileDialog.getExistingDirectory(self)
        self.output_dir_edit.setText(url)
        self.update_output_dir_list()

    def set_input_folder(self):
        url = QFileDialog.getExistingDirectory(self)
        self.input_dir_edit.setText(url)
        self.update_input_dir_list()

    def set_key_path(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Choose')
        if Keys.load_key(filename) is None:
            self.key_edit.setText('')
            self.lamp.setRed()
        else:
            self.key_edit.setText(filename)
            sleep(0.1)
            self.lamp.setGreen()

    def _encrypt(self):
        self.run.setEnabled(True)
        self.encrypt = True
        self.encrypt_button.setEnabled(False)
        self.decrypt_button.setEnabled(True)

    def decrypt(self):
        self.run.setEnabled(True)
        self.encrypt = False
        self.decrypt_button.setEnabled(False)
        self.encrypt_button.setEnabled(True)

    def on_generate_key(self):
        # Create a QMessageBox object
        popup = QMessageBox(self)

        # Set the message and title
        popup.setText("Your key has been generated! \n Click Save to choose a location. "
                      "\n\n IMPORTANT: Keep the key safely stored! "
                      "It will be used to encryption and decryption of your files!")
        popup.setWindowTitle('Generate Key')

        # Add the two choice buttons
        save_button = popup.addButton('Save', QMessageBox.ButtonRole.AcceptRole)
        popup.addButton('Cancel', QMessageBox.ButtonRole.RejectRole)

        # Show the pop-up window and wait for the user to interact with it
        popup.exec()

        key = Keys.generate_key()
        # If the user clicked the Save button, generate the key
        if popup.clickedButton() == save_button:
            filename, _ = QFileDialog.getSaveFileName(self, 'Save Key', '', 'Key files (*.pem)')
            Keys.save_key(key, filename)
            QMessageBox.information(self, 'Key saved', 'The key has been saved to the file: {}'.format(filename))
            self.key_edit.setText(filename)

        sleep(0.1)
        self.lamp.setGreen()

    def get_chosen_files(self) -> List[str]:
        files = []
        for i in range(self.input_list.count()):
            item = self.input_list.item(i)
            checkbox = self.input_list.itemWidget(item)
            if checkbox.isChecked():
                files.append(checkbox.text())
        return files

    def run_is_valid(self) -> bool:

        if self.key_edit.text() == '':
            ErrorHandler().missing_key_error()
            self.lamp.setRed()
            return False
        elif self.input_dir_edit.text() == '':
            ErrorHandler().input_dir_missing_error()
            return False
        elif self.output_dir_edit.text() == '':
            ErrorHandler().output_dir_missing_error()
            return False

        elif not self.get_chosen_files():
            ErrorHandler().no_files_chosen_error()
            return False
        return True

    def on_run(self):

        if self.run_is_valid():
            chosen_files = self.get_chosen_files()
            key = Keys.load_key(self.key_edit.text())
            if self._encrypt:
                for file in chosen_files:
                    full_path = os.path.join(self.input_dir_edit.text(), file)
                    Security.binary_encrypt(key=key, input_path=full_path, output_dir=self.output_dir_edit.text())

                msg = f"Files have been encrypted!\n\n Find them in {self.output_dir_edit.text()}"

            else:
                for file in chosen_files:
                    full_path = os.path.join(self.input_dir_edit.text(), file)

                    Security.binary_decrypt(key=key, input_path=full_path, output_dir=self.output_dir_edit.text())

                msg = f"Files have been decrypted!\n\n Find them in {self.output_dir_edit.text()}"

            self.update_output_dir_list()
            success_popup = QMessageBox()
            success_popup.setText(msg)
            success_popup.setWindowTitle("Run Complete")
            success_popup.addButton('OK', QMessageBox.ButtonRole.AcceptRole)
            success_popup.exec()
