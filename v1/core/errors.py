class KaucherException(Exception):
    pass


class UserAlreadyExists(KaucherException):
    """
    Raised after checking by username and email, if they are already in the database
    """
    pass


class IncorrectPassword(KaucherException):
    pass
