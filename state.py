#!/usr/bin/python3
"""State the State class."""
from models.base_model import BaseModel


class State(BaseModel):
    """State Model presenter.
    Attributes:
        name (str): State name.
    """

    name = ""