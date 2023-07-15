#!/usr/bin/python3
"""Defines for models/city.py unittests.
Unittest classes:
    TestCity_instantiation
    TestCity_save
    TestCity_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.city import City

global sleep_tm
sleep_tm = 0.05


class TestCity_instantiation(unittest.TestCase):
    """Unittests instantiation City class."""

    def test_no_args_instantiates(self):
        self.assertEqual(City, type(City()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(City(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(City().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().updated_at))

    def test_state_id_is_public_class_attribute(self):
        cityModel = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(cityModel))
        self.assertNotIn("state_id", cityModel.__dict__)

    def test_name_is_public_class_attribute(self):
        cityModel = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(cityModel))
        self.assertNotIn("name", cityModel.__dict__)

    def test_two_cities_unique_ids(self):
        cityModel1 = City()
        cityModel2 = City()
        self.assertNotEqual(cityModel1.id, cityModel2.id)

    def test_two_cities_different_created_at(self):
        cityModel1 = City()
        sleep(sleep_tm)
        cityModel2 = City()
        self.assertLess(cityModel1.created_at, cityModel2.created_at)

    def test_two_cities_different_updated_at(self):
        cityModel1 = City()
        sleep(sleep_tm)
        cityModel2 = City()
        self.assertLess(cityModel1.updated_at, cityModel2.updated_at)

    def test_str_representation(self):
        date_today = datetime.today()
        dateToday_repr = repr(date_today)
        cityModel = City()
        cityModel.id = "123456"
        cityModel.created_at = cityModel.updated_at = date_today
        city_str = cityModel.__str__()
        self.assertIn("[City] (123456)", city_str)
        self.assertIn("'id': '123456'", city_str)
        self.assertIn("'created_at': " + dateToday_repr, city_str)
        self.assertIn("'updated_at': " + dateToday_repr, city_str)

    def test_args_unused(self):
        cityModel = City(None)
        self.assertNotIn(None, cityModel.__dict__.values())

    def test_instantiation_with_kwargs(self):
        date_today = datetime.today()
        dt_iso = date_today.isoformat()
        cityModel = City(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(cityModel.id, "345")
        self.assertEqual(cityModel.created_at, date_today)
        self.assertEqual(cityModel.updated_at, date_today)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class TestCity_save(unittest.TestCase):
    """Unittests for testing save method of the City class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        cityModel = City()
        sleep(sleep_tm)
        fst_updated_at = cityModel.updated_at
        cityModel.save()
        self.assertLess(fst_updated_at, cityModel.updated_at)

    def test_two_saves(self):
        cityModel = City()
        sleep(sleep_tm)
        fst_updated_at = cityModel.updated_at
        cityModel.save()
        scd_updated_at = cityModel.updated_at
        self.assertLess(fst_updated_at, scd_updated_at)
        sleep(sleep_tm)
        cityModel.save()
        self.assertLess(scd_updated_at, cityModel.updated_at)

    def test_save_with_arg(self):
        cityModel = City()
        with self.assertRaises(TypeError):
            cityModel.save(None)

    def test_save_updates_file(self):
        cityModel = City()
        cityModel.save()
        cityId = "City." + cityModel.id
        with open("file.json", "r") as f:
            self.assertIn(cityId, f.read())


class TestCity_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the City class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(City().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        cityModel = City()
        self.assertIn("id", cityModel.to_dict())
        self.assertIn("created_at", cityModel.to_dict())
        self.assertIn("updated_at", cityModel.to_dict())
        self.assertIn("__class__", cityModel.to_dict())

    def test_to_dict_contains_added_attributes(self):
        cityModel = City()
        cityModel.middle_name = "AirBnb"
        cityModel.my_number = 98
        self.assertEqual("AirBnb", cityModel.middle_name)
        self.assertIn("my_number", cityModel.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        cityModel = City()
        cy_dict = cityModel.to_dict()
        self.assertEqual(str, type(cy_dict["id"]))
        self.assertEqual(str, type(cy_dict["created_at"]))
        self.assertEqual(str, type(cy_dict["updated_at"]))

    def test_to_dict_output(self):
        date_today = datetime.today()
        cityModel = City()
        cityModel.id = "123456"
        cityModel.created_at = cityModel.updated_at = date_today
        tdict = {
            'id': '123456',
            '__class__': 'City',
            'created_at': date_today.isoformat(),
            'updated_at': date_today.isoformat(),
        }
        self.assertDictEqual(cityModel.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        cityModel = City()
        self.assertNotEqual(cityModel.to_dict(), cityModel.__dict__)

    def test_to_dict_with_arg(self):
        cityModel = City()
        with self.assertRaises(TypeError):
            cityModel.to_dict(None)


if __name__ == "__main__":
    unittest.main()
