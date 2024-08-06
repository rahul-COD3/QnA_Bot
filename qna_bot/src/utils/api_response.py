class Response:
    def __init__(self, data=None, error_message=None):
        if error_message is not None:
            self.is_success = False
            self.data = error_message
        else:
            self.is_success = True
            self.data = data