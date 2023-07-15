#!/usr/bin/python3
"""Init for models/amenity.py unittests.
Unittest classes:
    TestAmenity_instantiation
    TestAmenity_save
    TestAmenity_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity

global sleep_tm
sleep_tm = 0.05


class TestAmenity_instantiation(unittest.TestCase):
    """instantiation Unittests Amenity class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Amenity().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_name_is_public_class_attribute(self):
        amt_model = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", amt_model.__dict__)

    def test_two_amenities_unique_ids(self):
        amt_model1 = Amenity()
        amt_model2 = Amenity()
        self.assertNotEqual(amt_model1.id, amt_model2.id)

    def test_two_amenities_different_created_at(self):
        amt_model1 = Amenity()
        sleep(sleep_tm)
        amt_model2 = Amenity()
        self.assertLess(amt_model1.created_at, amt_model2.created_at)

    def test_two_amenities_different_updated_at(self):
        amt_model1 = Amenity()
        sleep(sleep_tm)
        amt_model2 = Amenity()
        self.assertLess(amt_model1.updated_at, amt_model2.updated_at)

    def test_str_representation(self):
        date_today = datetime.today()
        crr_repre = repr(date_today)
        amt_model = Amenity()
        amt_model.id = "123456"
        amt_model.created_at = amt_model.updated_at = date_today
        amt_model_str = amt_model.__str__()
        self.assertIn("[Amenity] (123456)", amt_model_str)
        self.assertIn("'id': '123456'", amt_model_str)
        self.assertIn("'created_at': " + crr_repre, amt_model_str)
        self.assertIn("'updated_at': " + crr_repre, amt_model_str)

    def test_args_unused(self):
        amt_model = Amenity(None)
        self.assertNotIn(None, amt_model.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """instantiation with kwargs test method"""
        date_today = datetime.today()
        dt_iso = date_today.isoformat()
        amt_model = Amenity(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(amt_model.id, "345")
        self.assertEqual(amt_model.created_at, date_today)
        self.assertEqual(amt_model.updated_at, date_today)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)


class TestAmenity_save(unittest.TestCase):
    """Save method Unittests of Amenity class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("obj_file.json", "tmp")
        except IOError:
            pass

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
        amt_model = Amenity()
        sleep(sleep_tm)
        fst_updated_at = amt_model.updated_at
        amt_model.save()
        self.assertLess(fst_updated_at, amt_model.updated_at)

    def test_two_saves(self):
        amt_model = Amenity()
        sleep(sleep_tm)
        fst_updated_at = amt_model.updated_at
        amt_model.save()
        scd_updated_at = amt_model.updated_at
        self.assertLess(fst_updated_at, scd_updated_at)
        sleep(sleep_tm)
        amt_model.save()
        self.assertLess(scd_updated_at, amt_model.updated_at)

    def test_save_with_arg(self):
        amt_model = Amenity()
        with self.assertRaises(TypeError):
            amt_model.save(None)

    def test_save_updates_file(self):
        amt_model = Amenity()
        amt_model.save()
        amid = "Amenity." + amt_model.id
        with open("obj_file.json", "r") as f:
            self.assertIn(amid, f.read())


class TestAmenity_to_dict(unittest.TestCase):
    """to_dict Unittests  Amenity class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Amenity().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        amt_model = Amenity()
        self.assertIn("id", amt_model.to_dict())
        self.assertIn("created_at", amt_model.to_dict())
        self.assertIn("updated_at", amt_model.to_dict())
        self.assertIn("__class__", amt_model.to_dict())

    def test_to_dict_contains_added_attributes(self):
        amt_model = Amenity()
        amt_model.middle_name = "AirBnb"
        amt_model.my_number = 98
        self.assertEqual("AirBnb", amt_model.middle_name)
        self.assertIn("my_number", amt_model.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        amt_model = Amenity()
        amt_dictn = amt_model.to_dict()
        self.assertEqual(str, type(amt_dictn["id"]))
        self.assertEqual(str, type(amt_dictn["created_at"]))
        self.assertEqual(str, type(amt_dictn["updated_at"]))

    def test_to_dict_output(self):
        date_today = datetime.today()
        amt_model = Amenity()
        amt_model.id = "123456"
        amt_model.created_at = amt_model.updated_at = date_today
        td_dict = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': date_today.isoformat(),
            'updated_at': date_today.isoformat(),
        }
        self.assertDictEqual(amt_model.to_dict(), td_dict)

    def test_contrast_to_dict_dunder_dict(self):
        amt_model = Amenity()
        self.assertNotEqual(amt_model.to_dict(), amt_model.__dict__)

    def test_to_dict_with_arg(self):
        amt_model = Amenity()
        with self.assertRaises(TypeError):
            amt_model.to_dict(None)


if __name__ == "__main__":
    unittest.main()
