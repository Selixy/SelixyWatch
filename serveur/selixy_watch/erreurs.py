class Refus(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code, self.message = code, message


class ErreurImport(Exception):
    pass
