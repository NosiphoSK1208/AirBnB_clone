#!/usr/bin/python3
"""State the User class."""
from models.base_model import BaseModel


class User(BaseModel):
    """User Model presenter.
    Attributes:
        first_name (str): User firstname.
        last_name (str): User lastname.
        email (str): User email address.
        password (str): User password.
    """

    first_name = ""
    last_name = ""
    email = ""
    password = ""
