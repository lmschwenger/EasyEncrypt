from PyQt6.QtWidgets import QMessageBox


class ErrorHandler:

    error_dict = {
        'MissingInputFolder': ['Error: No input folder specified!', 'Missing input folder'],
        'MissingOutputFolder': ['Error: No output folder specified!', 'Missing output folder'],
        'MissingKeyError': ['Error: No key chosen. If you do not have one, press create to make a new one!',
                            'Missing Key Error'],
        'NoFilesChosen': ['Error: No files have been chosen!', 'No Files Chosen']
    }

    @classmethod
    def error_popup(cls, error: str) -> None:
        msg, title = cls.error_dict[error]
        success_popup = QMessageBox()
        success_popup.setText(msg)
        success_popup.setWindowTitle(title)
        success_popup.addButton('OK', QMessageBox.ButtonRole.AcceptRole)
        success_popup.exec()

    @classmethod
    def key_missing_error(cls) -> None:
        cls.error_popup('MissingKeyError')

    @classmethod
    def input_dir_missing_error(cls) -> None:
        cls.error_popup(error='MissingInputFolder')

    @classmethod
    def output_dir_missing_error(cls) -> None:
        cls.error_popup(error='MissingOutputFolder')

    @classmethod
    def no_files_chosen_error(cls) -> None:
        cls.error_popup(error='NoFilesChosen')
