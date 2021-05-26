class AuthenticationException(Exception):
    def __init__(self, text):
        self.text = text


class NoChildrenException(Exception):
    def __init__(self, text):
        self.text = text


class NoSuccessException(Exception):
    def __init__(self, text):
        self.text = text
