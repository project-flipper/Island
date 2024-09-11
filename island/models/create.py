
import re
import email_validator
from pydantic import BaseModel, field_validator

from island.core.config import HAS_LETTERS_REGEX, MAX_PASSWORD_LENGTH, MAX_USERNAME_LENGTH, MIN_PASSWORD_LENGTH, MIN_USERNAME_LENGTH, ONLY_NUMBERS_REGEX, VALID_USERNAME_REGEX
from island.core.i18n import _


class CreateUser(BaseModel):
    name: str
    color: int
    password: str
    email: str
    token: str

    @field_validator("name")
    @classmethod
    def username_check(cls, value: str):
        value = value.strip()

        if len(value) < MIN_USERNAME_LENGTH:
            raise ValueError(_("error.username.short"))
        elif len(value) > MAX_USERNAME_LENGTH:
            raise ValueError(_("error.username.long"))
        elif not VALID_USERNAME_REGEX.match(value):
            raise ValueError(_("error.username.invalid"))
        elif ONLY_NUMBERS_REGEX.match(value):
            raise ValueError(_("error.username.invalid"))
        elif not HAS_LETTERS_REGEX.match(value):
            raise ValueError(_("error.username.invalid"))

        return value

    @field_validator("password")
    @classmethod
    def password_strength_check(cls, value: str):
        if len(value) < MIN_PASSWORD_LENGTH:
            raise ValueError(_("error.password.short"))
        elif len(value) > MAX_PASSWORD_LENGTH:
            raise ValueError(_("error.password.long"))

        return value

    @field_validator("email")
    @classmethod
    def email_valid(cls, value: str):
        value = value.strip()

        try:
            email_validator.validate_email(value)
        except email_validator.EmailNotValidError as e:
            raise ValueError(_("error.email.invalid")) from e

        return value

class Create(BaseModel):
    user_id: str | None
    validation_errors: dict[str, str]
