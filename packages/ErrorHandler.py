from enum import Enum

from PyQt6.QtWidgets import QMessageBox


class ErrorHandler:
    class ErrorMessages(Enum):
        ReadPermissionError = ['Error: EasyEncrypt is not allowed to open the file \n \n'
                               'Try to re-open EasyEncrypt as Administrator', 'Permission Error']
        MissingInputFolder = ['Error: No input folder specified!', 'Missing input folder']
        MissingOutputFolder = ['Error: No output folder specified!', 'Missing output folder']
        MissingKeyError = ['Error: No key chosen. If you do not have one, press create to make a new one!',
                           'Missing Key Error']
        InvalidKeyError = ['Unable to load key. Make sure it is a valid Fernet key, or create a new one.',
                           'Unable to read Key']
        NoFilesChosen = ['Error: No files have been chosen!', 'No Files Chosen']
        InvalidTokenError = ['Error: Unable to decrypt file!', 'InvalidTokenError']
        InvalidPasswordError = ['Error', 'Error']
    @classmethod
    def error_popup(cls, error: Enum) -> None:
        msg, title = error.value
        success_popup = QMessageBox()
        success_popup.setText(msg)
        success_popup.setWindowTitle(title)
        success_popup.addButton('OK', QMessageBox.ButtonRole.AcceptRole)
        success_popup.exec()

    @classmethod
    def missing_key_error(cls) -> None:
        cls.error_popup(cls.ErrorMessages.MissingKeyError)

    @classmethod
    def invalid_key_error(cls) -> None:
        cls.error_popup(cls.ErrorMessages.InvalidKeyError)

    @classmethod
    def input_dir_missing_error(cls) -> None:
        cls.error_popup(cls.ErrorMessages.MissingInputFolder)

    @classmethod
    def output_dir_missing_error(cls) -> None:
        cls.error_popup(cls.ErrorMessages.MissingOutputFolder)

    @classmethod
    def no_files_chosen_error(cls) -> None:
        cls.error_popup(cls.ErrorMessages.NoFilesChosen)

    @classmethod
    def read_permission_error(cls) -> None:
        cls.error_popup(cls.ErrorMessages.ReadPermissionError)

    @classmethod
    def invalid_token_error(cls) -> None:
        cls.error_popup(cls.ErrorMessages.InvalidTokenError)

    @classmethod
    def invalid_password_error(cls) -> None:
        cls.error_popup(cls.ErrorMessages.InvalidPasswordError)
