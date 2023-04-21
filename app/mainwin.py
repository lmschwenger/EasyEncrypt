import os

from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, \
    QMainWindow, QMessageBox, QFileDialog

from app.img_dialog import ImgDialog
from packages.Keys import Keys
from pdf_dialog import PdfDialog


class MainWin(QMainWindow):
    resource_folder = os.path.join(os.path.dirname(__file__), os.pardir, 'resources')
    encrypt = None

    def __init__(self):
        super().__init__()
        self.resize(540, 400)

        # Key Button
        hbox = QHBoxLayout()
        keybutton = QPushButton('Generate Key')
        keybutton.resize(50, 20)
        keybutton.clicked.connect(self.on_generate_key)

        hbox.addWidget(keybutton)

        # Center the button in the horizontal layout
        hbox.setAlignment(keybutton, Qt.AlignmentFlag.AlignHCenter)

        # Create a vertical box layout for the main window
        vbox = QVBoxLayout()

        vbox.addLayout(hbox)
        vbox.addStretch(1)

        # Create a widget to hold the main layout
        widget = QWidget()
        widget.setLayout(vbox)

        """ Add Encrypt/Decrypt options """
        option_layout = QHBoxLayout()
        option_layout.addStretch()
        # create buttons
        self.encrypt_button = QPushButton('Encrypt')
        self.encrypt_button.clicked.connect(self.encrypt)
        self.encrypt_button.setIconSize(QtCore.QSize(25, 64))
        option_layout.addWidget(self.encrypt_button)

        # connect buttons to methods
        self.decrypt_button = QPushButton('Decrypt')
        self.decrypt_button.clicked.connect(self.decrypt)
        self.decrypt_button.setIconSize(QtCore.QSize(20, 64))

        option_layout.addWidget(self.decrypt_button)
        option_layout.addStretch()
        vbox.addLayout(option_layout)

        """ Add The three functional buttons options """
        # Create a horizontal box layout for the buttons
        button_layout = QHBoxLayout()
        # Create a button with a PDF logo
        self.pdf_button = QPushButton()
        self.pdf_button.setIcon(QIcon(os.path.join(self.resource_folder, 'pdf_icon.png')))
        self.pdf_button.setIconSize(QtCore.QSize(64, 64))
        self.pdf_button.clicked.connect(self.on_click_pdf)
        button_layout.addWidget(self.pdf_button)

        # Create a button with a PNG logo
        self.png_button = QPushButton()
        self.png_button.setIcon(QIcon(os.path.join(self.resource_folder, 'img_icon.png')))
        self.png_button.setIconSize(QtCore.QSize(64, 64))
        self.png_button.clicked.connect(self.on_click_img)

        button_layout.addWidget(self.png_button)

        # Create a button with a text-file logo
        self.txt_button = QPushButton()
        self.txt_button.setIcon(QIcon(os.path.join(self.resource_folder, 'file_icon.png')))
        self.txt_button.setIconSize(QtCore.QSize(64, 64))
        # txt_button.clicked.connect(self.on_click_file)
        button_layout.addWidget(self.txt_button)

        self.pdf_button.setEnabled(False)
        self.png_button.setEnabled(False)
        self.txt_button.setEnabled(False)

        vbox.addLayout(button_layout)
        self.setCentralWidget(widget)

    def enable_buttons(self):
        self.pdf_button.setEnabled(True)
        self.png_button.setEnabled(True)
        self.txt_button.setEnabled(True)

    def encrypt(self):
        self.enable_buttons()
        self.encrypt = True
        self.encrypt_button.setEnabled(False)
        self.decrypt_button.setEnabled(True)

    def decrypt(self):
        self.enable_buttons()
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
        response = popup.exec()

        key = Keys.generate_key()
        # If the user clicked the Save button, generate the key
        if popup.clickedButton() == save_button:
            filename, _ = QFileDialog.getSaveFileName(self, 'Save Key', '', 'Key files (*.pem)')
            Keys.save_key(key, filename)
            QMessageBox.information(self, 'Key saved', 'The key has been saved to the file: {}'.format(filename))

    def on_click_pdf(self):
        pdf_dialog = PdfDialog()
        pdf_dialog.on_accept(encrypt=self.encrypt)

    def on_click_img(self):
        img_dialog = ImgDialog()
        img_dialog.on_accept(encrypt=self.encrypt)
