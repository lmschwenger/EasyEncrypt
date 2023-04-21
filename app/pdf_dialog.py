from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout, QDialog, QFileDialog, QLineEdit, QMessageBox

from packages.Security import Security


class PdfDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Create line edits for key input, PDF file path, and output path
        self.key_edit = QLineEdit()
        self.key_edit.setPlaceholderText('Choose Password')
        self.pdf_edit = QLineEdit()
        self.pdf_edit.setPlaceholderText('PDF file path')
        self.output_edit = QLineEdit()
        self.output_edit.setPlaceholderText('Output path')

        # Create browse buttons for PDF file path and output path
        self.pdf_browse_button = QPushButton('Browse')
        self.pdf_browse_button.clicked.connect(self.browse_pdf)
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
        pdf_layout = QHBoxLayout()
        pdf_layout.addWidget(self.pdf_edit)
        pdf_layout.addWidget(self.pdf_browse_button)
        output_layout = QHBoxLayout()
        output_layout.addWidget(self.output_edit)
        output_layout.addWidget(self.output_browse_button)

        # Create a vertical layout for the dialog window
        vbox = QVBoxLayout()
        vbox.addLayout(pdf_layout)
        vbox.addLayout(output_layout)
        vbox.addLayout(key_layout)
        vbox.addWidget(self.ok_button)
        vbox.addWidget(self.cancel_button)

        # Set the layout for the dialog window
        self.setLayout(vbox)

    def browse_pdf(self):
        # Open a file dialog to select a PDF file
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select PDF File', '', 'PDF Files (*.pdf)')

        # Update the PDF file path line edit
        self.pdf_edit.setText(file_path)

    def browse_key(self):
        # Open a file dialog to select a PDF file
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select key File', '', 'PEM Files (*.pem)')

        # Update the PDF file path line edit
        self.key_edit.setText(file_path)

    def browse_output(self):
        # Open a file dialog to select an output path
        output_path, _ = QFileDialog.getSaveFileName(self, 'Select Output Path', '', 'PDF Files (*.pdf)')

        # Update the output path line edit
        self.output_edit.setText(output_path)

    def get_key(self):
        # Return the input key
        return self.key_edit.text()

    def get_pdf_path(self):
        # Return the selected PDF file path
        return self.pdf_edit.text()

    def get_output_path(self):
        # Return the selected output path
        return self.output_edit.text()

    def on_accept(self, encrypt: bool):

        while True:
            result = self.exec()

            if result == 1:

                if self.key_edit.text() == '':
                    QMessageBox.information(self, 'Warning', 'No Password given ...')

                elif self.pdf_edit.text() == '':
                    QMessageBox.information(self, 'Warning', 'Select an PDF ...')

                elif self.output_edit.text() == '':
                    QMessageBox.information(self, 'Warning', 'Select an output path ...')

                else:
                    password = self.key_edit.text()
                    if encrypt:
                        msg = "PDF has been locked with password!"
                        Security.lock_pdf(password=password, pdf_path=self.pdf_edit.text(),
                                          output_path=self.output_edit.text())
                        QMessageBox.information(self, msg,
                                                f'The PDF has been saved to the file: {self.output_edit.text()}')
                        break  # Exit the loop if all values are specified

                    else:
                        # TODO: Fix this. It returns wrong password even when the correct is typed in
                        issue = Security.unlock_pdf(password=password, pdf_path=self.pdf_edit.text(),
                                                    output_path=self.output_edit.text())
                        if issue:
                            QMessageBox.information(self, 'Error', issue)
                        else:
                            msg = "PDF has been unlocked!"
                            QMessageBox.information(self, msg,
                                                    f'The PDF has been saved to the file: {self.output_edit.text()}')
            elif result == 0:
                break
