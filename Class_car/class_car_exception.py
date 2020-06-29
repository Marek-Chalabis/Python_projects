class IllegalCarError(Exception):
    """
    Exception raised for errors in class Car
    """

    def __init__(self, value, message):
        """
            :param value: value which caused the error
            :param message :  explanation of the error
        """
        self.value = value
        self.message = message

    def __str__(self):
        return f"{self.message}\nGIVEN VALUE: {self.value}"

