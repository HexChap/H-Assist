import re

from tortoise.validators import Validator, ValidationError


__all__ = [
    "EmailValidator"
]

EMAIL_PATTERN = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"


class EmailValidator(Validator):
    """
    Validator to check if a given value is email.
    """

    def __init__(self):
        self.email_regex = re.compile(EMAIL_PATTERN, re.U)

    def __call__(self, value: str):
        if not self.email_regex.match(value):
            raise ValidationError(f"Value '{value}' isn't email.")
