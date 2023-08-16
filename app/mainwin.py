import os
from time import sleep
from typing import List, Tuple, Optional

from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, \
    QMainWindow, QMessageBox, QFileDialog, QGroupBox, QLineEdit, QListWidget, QCheckBox, QListWidgetItem, QInputDialog,\
    QProgressBar

from app.gui_lamp import RoundLamp
from packages.Encryptor import Encryptor
from packages.ErrorHandler import ErrorHandler
from packages.KeyManager import KeyManager


class MainWin(QMainWindow):
    resource_folder = os.path.join(os.path.dirname(__file__), 'resources')
    encrypt = None
    password = None

    def __init__(self):
        super().__init__()
        self._settings = QtCore.QSettings("OpenOrg", "Easy Encrypt")
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
        self.encrypt_button.clicked.connect(self._encrypt)
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

        self.progress_bar = QProgressBar()

        run_layout.addWidget(self.run)
        run_layout.addWidget(self.progress_bar)
        self.gb_run.setLayout(run_layout)
        vbox.addWidget(self.gb_run)

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)

        if self._key_found():
            reply = QMessageBox.question(
                self,
                "Confirmation",
                "Do you want to use latest settings?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )

            if reply == QMessageBox.StandardButton.Yes:
                self.input_dir_edit.setText(self._settings.value("easy_encrypt_input_path"))
                self.output_dir_edit.setText(self._settings.value("easy_encrypt_output_path"))
                self.key_edit.setText(self._settings.value("easy_encrypt_secret"))
                self.set_key_path()
                self.update_input_dir_list()
                self.update_output_dir_list()
        else:
            self._settings.setValue("easy_encrypt_input_path", None)
            self._settings.setValue("easy_encrypt_output_path", None)

    def _key_found(self) -> bool:
        if not self._settings.contains("easy_encrypt_secret"):
            self._settings.setValue("easy_encrypt_secret", None)
            return False
        print("les go")
        return os.path.exists(self._settings.value("easy_encrypt_secret"))

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
        if url == '':
            return
        self.output_dir_edit.setText(url)
        self.update_output_dir_list()
        self._settings.setValue("easy_encrypt_output_path", url)

    def set_input_folder(self):
        url = QFileDialog.getExistingDirectory(self)
        if url == '':
            return
        self.input_dir_edit.setText(url)

        self.input_dir_edit.setText(self._settings.value("easy_encrypt_input_path"))
        self.update_input_dir_list()
        self._settings.setValue("easy_encrypt_input_path", url)

    def set_key_path(self):

        if self.key_edit.text() == '':
            filename, _ = QFileDialog.getOpenFileName(self, 'Choose')

            if filename == '':
                return
        else:
            filename = self.key_edit.text()

        self.set_password()
        try:
            KeyManager.load_key(self.password, filename)
            sleep(0.1)
            self.lamp.setGreen()
            self._settings.setValue("easy_encrypt_secret", filename)
        except:
            ErrorHandler().invalid_password_error()
            self.key_edit.setText('')
            self.lamp.setRed()

    def _encrypt(self):

        self.run.setEnabled(True)
        self.encrypt = True
        self.encrypt_button.setEnabled(False)
        self.decrypt_button.setEnabled(True)
        self._settings.setValue("easy_encrypt_secret", self.key_edit.text())
        print(self._settings.value("easy_encrypt_secret"))
        self._settings.sync()

    def decrypt(self):
        self.run.setEnabled(True)
        self.encrypt = False
        self.decrypt_button.setEnabled(False)
        self.encrypt_button.setEnabled(True)
        self._settings.setValue("easy_encrypt_secret", self.key_edit.text())
        self._settings.sync()

    @classmethod
    def set_password(cls) -> None:
        dialog = QInputDialog(None)
        dialog.setWindowTitle('Password')
        dialog.setLabelText('Enter your password:')
        dialog.setTextEchoMode(QLineEdit.EchoMode.Password)

        if dialog.exec() == QInputDialog.DialogCode.Accepted:
            cls.password = dialog.textValue()

    def get_save_popup(self) -> Tuple[QMessageBox, QPushButton]:
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
        return popup, save_button

    def on_generate_key(self):
        # Create a QMessageBox object

        self.set_password()
        key = KeyManager.create_key(self.password, salt=os.urandom(12))
        popup, saved = self.get_save_popup()

        # If the user clicked the Save button, generate the key
        if self.password != '':
            filename, _ = QFileDialog.getSaveFileName(self, 'Save Key', '', 'Key files (*.pem)')
            KeyManager.save_key(key, self.password, filename)
            QMessageBox.information(self, f'Key saved', 'The key has been saved to the file: {}'.format(filename))
            self.key_edit.setText(filename)

            sleep(0.1)
            self.lamp.setGreen()
            self.cache.write_line_to_cache(key='key', line=self.key_edit.text())

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

        elif len(self.get_chosen_files()) == 0:
            ErrorHandler().no_files_chosen_error()
            return False
        return True

    def on_run(self):
        success = False
        if self.run_is_valid():
            chosen_files = self.get_chosen_files()
            key = KeyManager.load_key(self.password, self.key_edit.text())

            if self.encrypt:
                for file in chosen_files:
                    full_path = os.path.join(self.input_dir_edit.text(), file)
                    success = Encryptor.binary_encrypt(key=key, input_path=full_path,
                                                       output_dir=self.output_dir_edit.text(), pg_bar=self.progress_bar)

                msg = f"Files have been encrypted!\n\n Find them in {self.output_dir_edit.text()}"

            else:
                for file in chosen_files:
                    full_path = os.path.join(self.input_dir_edit.text(), file)

                    success = Encryptor.binary_decrypt(key=key, input_path=full_path,
                                                       output_dir=self.output_dir_edit.text(), pg_bar=self.progress_bar)

                msg = f"Files have been decrypted!\n\n Find them in {self.output_dir_edit.text()}"
            if success:
                self.cache.write_line_to_cache(key='input_path', line=self.input_dir_edit.text())
                self.cache.write_line_to_cache(key='output_path', line=self.output_dir_edit.text())

                self.update_output_dir_list()
                success_popup = QMessageBox()
                success_popup.setText(msg)
                success_popup.setWindowTitle("Run Complete")
                success_popup.addButton('OK', QMessageBox.ButtonRole.AcceptRole)
                success_popup.exec()
