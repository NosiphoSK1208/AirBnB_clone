#!/usr/bin/python3
"""State unittests for models/base_model.py.
Unittest classes:
    TestBaseModel_instantiation
    TestBaseModel_save
    TestBaseModel_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel

global sleep_tm 
sleep_tm = 0.05
class TestBaseModel_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the BaseModel class."""
    

    def test_no_args_instantiates(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_two_models_unique_ids(self):
        basemodel1 = BaseModel()
        basemodel2 = BaseModel()
        self.assertNotEqual(basemodel1.id, basemodel2.id)

    def test_two_models_different_created_at(self):
        basemodel1 = BaseModel()
        sleep(sleep_tm)
        basemodel2 = BaseModel()
        self.assertLess(basemodel1.created_at, basemodel2.created_at)

    def test_two_models_different_updated_at(self):
        basemodel1 = BaseModel()
        sleep(sleep_tm)
        basemodel2 = BaseModel()
        self.assertLess(basemodel1.updated_at, basemodel2.updated_at)

    def test_str_representation(self):
        date_today = datetime.today()
        crr_repre = repr(date_today)
        basemodel = BaseModel()
        basemodel.id = "202307"
        basemodel.created_at = basemodel.updated_at = date_today
        bmstr = basemodel.__str__()
        self.assertIn("[BaseModel] (202307)", bmstr)
        self.assertIn("'id': '202307'", bmstr)
        self.assertIn("'updated_at': " + crr_repre, bmstr)
        self.assertIn("'created_at': " + crr_repre, bmstr)

    def test_args_unused(self):
        basemodel = BaseModel(None)
        self.assertNotIn(None, basemodel.__dict__.values())

    def test_instantiation_with_kwargs(self):
        date_today = datetime.today()
        date_iso = date_today.isoformat()
        basemodel = BaseModel(id="729", created_at=date_iso, updated_at=date_iso)
        self.assertEqual(basemodel.id, "729")
        self.assertEqual(basemodel.created_at, date_today)
        self.assertEqual(basemodel.updated_at, date_today)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        date_today = datetime.today()
        date_iso = date_today.isoformat()
        basemodel = BaseModel("12", id="729", created_at=date_iso, updated_at=date_iso)
        self.assertEqual(basemodel.id, "729")
        self.assertEqual(basemodel.created_at, date_today)
        self.assertEqual(basemodel.updated_at, date_today)


class TestBaseModel_save(unittest.TestCase):
    """Unittests for testing save method of the BaseModel class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("obj_file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("obj_file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "obj_file.json")
        except IOError:
            pass
    def test_one_save(self):
        basemodel = BaseModel()
        sleep(sleep_tm)
        initial_updated_at = basemodel.updated_at
        basemodel.save()
        self.assertLess(initial_updated_at, basemodel.updated_at)

    def test_two_saves(self):
        basemodel = BaseModel()
        sleep(sleep_tm)
        initial_updated_at = basemodel.updated_at
        basemodel.save()
        second_updated_at = basemodel.updated_at
        self.assertLess(initial_updated_at, second_updated_at)
        sleep(sleep_tm)
        basemodel.save()
        self.assertLess(second_updated_at, basemodel.updated_at)

    def test_save_with_arg(self):
        basemodel = BaseModel()
        with self.assertRaises(TypeError):
            basemodel.save(None)

    def test_save_updates_file(self):
        basemodel = BaseModel()
        basemodel.save()
        bsm_id = "BaseModel." + basemodel.id
        with open("obj_file.json", "r") as f:
            self.assertIn(bsm_id, f.read())


class TestBaseModel_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the BaseModel class."""

    def test_to_dict_type(self):
        basemodel = BaseModel()
        self.assertTrue(dict, type(basemodel.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        basemodel = BaseModel()
        self.assertIn("id", basemodel.to_dict())
        self.assertIn("created_at", basemodel.to_dict())
        self.assertIn("updated_at", basemodel.to_dict())
        self.assertIn("__class__", basemodel.to_dict())

    def test_to_dict_contains_added_attributes(self):
        basemodel = BaseModel()
        basemodel.name = "AirBnb"
        basemodel.my_number = 88
        self.assertIn("name", basemodel.to_dict())
        self.assertIn("my_number", basemodel.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        basemodel = BaseModel()
        bm_dict = basemodel.to_dict()
        self.assertEqual(str, type(bm_dict["created_at"]))
        self.assertEqual(str, type(bm_dict["updated_at"]))

    def test_to_dict_output(self):
        date_today = datetime.today()
        basemodel = BaseModel()
        basemodel.id = "202307"
        basemodel.created_at = basemodel.updated_at = date_today
        tdict = {
            'id': '202307',
            '__class__': 'BaseModel',
            'created_at': date_today.isoformat(),
            'updated_at': date_today.isoformat()
        }
        self.assertDictEqual(basemodel.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        basemodel = BaseModel()
        self.assertNotEqual(basemodel.to_dict(), basemodel.__dict__)

    def test_to_dict_with_arg(self):
        basemodel = BaseModel()
        with self.assertRaises(TypeError):
            basemodel.to_dict(None)


if __name__ == "__main__":
    unittest.main() 
