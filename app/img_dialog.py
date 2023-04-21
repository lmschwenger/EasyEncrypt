from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QMainWindow, QMessageBox, \
    QDialog, QFileDialog, QLineEdit

from packages.Security import Security
from packages.Keys import Keys


class ImgDialog(QDialog):

    def __init__(self):
        super().__init__()

        # Create line edits for key input, PDF file path, and output path
        self.key_edit = QLineEdit()
        self.key_edit.setPlaceholderText('Key input')
        self.img_edit = QLineEdit()
        self.img_edit.setPlaceholderText('Image file path')
        self.output_edit = QLineEdit()
        self.output_edit.setPlaceholderText('Output path')

        # Create browse buttons for PDF file path and output path

        self.key_browse_button = QPushButton('Browse')
        self.key_browse_button.clicked.connect(self.browse_key)
        self.img_browse_button = QPushButton('Browse')
        self.img_browse_button.clicked.connect(self.browse_img)
        self.output_browse_button = QPushButton('Browse')
        self.output_browse_button.clicked.connect(self.browse_output)

        # Create OK and Cancel buttons
        self.ok_button = QPushButton('OK')
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.reject)

        # Create a horizontal layout for each line
        key_layout = QHBoxLayout()
        key_layout.addWidget(self.key_edit)
        key_layout.addWidget(self.key_browse_button)
        pdf_layout = QHBoxLayout()
        pdf_layout.addWidget(self.img_edit)
        pdf_layout.addWidget(self.img_browse_button)
        output_layout = QHBoxLayout()
        output_layout.addWidget(self.output_edit)
        output_layout.addWidget(self.output_browse_button)

        # Create a vertical layout for the dialog window
        vbox = QVBoxLayout()
        vbox.addLayout(key_layout)
        vbox.addLayout(pdf_layout)
        vbox.addLayout(output_layout)
        vbox.addWidget(self.ok_button)
        vbox.addWidget(self.cancel_button)

        # Set the layout for the dialog window
        self.setLayout(vbox)

    def browse_img(self):
        # Open a file dialog to select a PDF file
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select Image File', '',
                                                   filter='PNG (*.png);;JPEG (*.jpg *.jpeg)')

        # Update the PDF file path line edit
        self.img_edit.setText(file_path)

    def browse_key(self):
        # Open a file dialog to select a PDF file
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select key File', '', 'PEM Files (*.pem)')

        # Update the PDF file path line edit
        self.key_edit.setText(file_path)

    def browse_output(self):
        # Open a file dialog to select an output path
        output_path, _ = QFileDialog.getSaveFileName(self, 'Select Output Path', '', 'PNG (*.png);; Jpeg (*.jpg)')

        # Update the output path line edit
        self.output_edit.setText(output_path)

    def get_key(self):
        # Return the input key
        return self.key_edit.text()

    def get_pdf_path(self):
        # Return the selected PDF file path
        return self.img_edit.text()

    def get_output_path(self):
        # Return the selected output path
        return self.output_edit.text()

    def on_accept(self, encrypt=True):
        while True:
            result = self.exec()

            if result == 1:
                if self.key_edit.text() == '':
                    QMessageBox.information(self, 'Warning', 'Select an .pem file with a valid key ...')

                elif self.img_edit.text() == '':
                    QMessageBox.information(self, 'Warning', 'Select an image ...')

                elif self.output_edit.text() == '':
                    QMessageBox.information(self, 'Warning', 'Select an output path ...')
                else:
                    key = Keys.load_key(self.key_edit.text())

                    if encrypt:
                        msg = 'Image Sucessfully Encrypted!'
                        Security.encrypt_image(key=key, image_path=self.img_edit.text(),
                                               output_path=self.output_edit.text())
                    else:
                        msg = 'Image Sucessfully Decrypted!'
                        Security.decrypt_image(key=key, image_path=self.img_edit.text(),
                                               output_path=self.output_edit.text())

                    QMessageBox.information(self, msg,
                                            'The image has been saved to the file: {}'.format(self.output_edit.text()))
                    break  # Exit the loop if all values are specified
            elif result == 0:
                break  # Exit the loop if the user cancels the dialog


