#!/usr/bin/python3
"""Init the FileStorage class."""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Represent an abstracted storage engine.
    Attributes:
        __file_direction (str):  obj_file to save objects to.
        __objs (dict): A dic of instantiated objects.
    """
    __file_direction = "file.json"
    __objs = {}

    def all(self):
        """Return the dic __objs."""
        return FileStorage.__objs

    def new(self, obj):
        oc_name = obj.__class__.__name__
        FileStorage.__objs["{}.{}".format(oc_name, obj.id)] = obj

    def save(self):
        o_dict = FileStorage.__objs
        dicti_js = {obj: o_dict[obj].to_dict() for obj in o_dict.keys()}
        with open(FileStorage.__file_direction, "w") as f:
            json.dump(dicti_js, f)

    def reload(self):
        try:
            with open(FileStorage.__file_direction) as f:
                dicti_js = json.load(f)
                for o in dicti_js.values():
                    cls_name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(cls_name)(**o))
        except FileNotFoundError:
            return

