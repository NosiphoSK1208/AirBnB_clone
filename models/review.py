#!/usr/bin/python3
"""State the Review class."""
from models.base_model import BaseModel


class Review(BaseModel):
    """Review Model present .
    Attributes:
        place_id (str): Place id from Place Model.
        user_id (str): User id from User Model.
        text (str): A text of the review.
    """

    place_id = ""
    user_id = ""
    text = ""
 