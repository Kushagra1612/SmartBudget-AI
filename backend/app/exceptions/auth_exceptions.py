class UserAlreadyExistsError(Exception):
    """Raised when email already exists."""
    pass


class InvalidCredentialsError(Exception):
    """Raised when login credentials are invalid."""
    pass