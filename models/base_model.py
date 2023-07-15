#!/usr/bin/python3
# Authors: Kwenziwa Khanyile & Nosipho Khumalo Date: 2023-07-11
# BaseModel class.
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """The BaseModel class is the foundation of the
    AirBnb_clone project. It provides the basic functionality
      that all other models in the project will inherit.

    Attributes:
        id (str): An UUID for when a new instance is created.
        created_at (datetime): Current date and time the instance is created.
        updated_at (datetime): Current date and time the instance is updated .
    """

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel.
        Args:
            *args (any): Unoccupied.
            **kwargs (dict): value or key pairs of attributes.
        """
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        today_form = "%Y-%m-%dT%H:%M:%S.%f"
        if len(kwargs) != 0:
            for x, y in kwargs.items():
                if x == "created_at" or x == "updated_at":
                    self.__dict__[x] = datetime.strptime(y, today_form)
                else:
                    self.__dict__[x] = y
        else:
            models.storage.new(self)

    def save(self):
        """Modernize updated_at with a now datetime and we save."""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """The dictionary of the BaseModel instance is beimg returned.
        The key/value pair __class__ representing
        the class name of the object are included.
        """
        array_dict_info = self.__dict__.copy()
        array_dict_info["created_at"] = self.created_at.isoformat()
        array_dict_info["updated_at"] = self.updated_at.isoformat()
        array_dict_info["__class__"] = self.__class__.__name__
        return array_dict_info

    def __str__(self):
        """Return the print/str depiction  of the BaseModel instance."""
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)
 
