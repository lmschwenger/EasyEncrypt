import os


class Helper:
    @classmethod
    def default_input_folder(cls) -> str:
        here = os.path.dirname(__file__)
        return os.path.join(here, '..', 'data', 'input')

    @classmethod
    def default_output_folder(cls) -> str:
        here = os.path.dirname(__file__)
        return os.path.join(here, '..', 'data', 'output')
