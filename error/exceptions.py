# error/exceptions.py
class ValidationError(Exception):
    """General validation error."""
    pass


class WrongFileTypeError(Exception):
    """Raised when a file is of the wrong type."""
    pass


class UserNotFoundError(Exception):
    """Raised when a user is not found."""
    pass


class UnauthorizedError(Exception):
    """Raised when a user is not authorized to perform an action."""
    pass


class WrongAccessCodeException(Exception):
    """Raised when an access code is wrong."""
    pass


class DuplicateEmailError(Exception):
    """Raised when attempting to create a user with an email that already exists."""
    pass


class ImageProcessingError(Exception):
    """Raised when an error occurs during image processing."""
    pass


class RoomNotFoundError(Exception):
    """Raised when a room is not found."""
    pass


class UnAvailableModelError(Exception):
    """Raised when a model is not available."""
    pass


class ChatNotFoundError(Exception):
    """Raised when a chat is not found."""
    pass
