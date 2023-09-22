class BadPasswordException(Exception):
    def __init__(self, message="Password isn't safe"):
        self.message = message
        super().__init__(self.message)


class BadEmailException(Exception):
    def __init__(self, message="Password isn't safe"):
        self.message = message
        super().__init__(self.message)
