#!/usr/bin/python3
"""Defines models/place.py  unittests.
Unittest classes:
    TestPlace_instantiation
    TestPlace_save
    TestPlace_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.place import Place


global sleep_tm
sleep_tm = 0.05


class TestPlace_instantiation(unittest.TestCase):
    """Unittests instantiation Place class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Place, type(Place()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Place(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Place().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Place().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Place().updated_at))

    def test_city_id_is_public_class_attribute(self):
        placeModel = Place()
        self.assertEqual(str, type(Place.city_id))
        self.assertIn("city_id", dir(placeModel))
        self.assertNotIn("city_id", placeModel.__dict__)

    def test_user_id_is_public_class_attribute(self):
        placeModel = Place()
        self.assertEqual(str, type(Place.user_id))
        self.assertIn("user_id", dir(placeModel))
        self.assertNotIn("user_id", placeModel.__dict__)

    def test_name_is_public_class_attribute(self):
        placeModel = Place()
        self.assertEqual(str, type(Place.name))
        self.assertIn("name", dir(placeModel))
        self.assertNotIn("name", placeModel.__dict__)

    def test_description_is_public_class_attribute(self):
        placeModel = Place()
        self.assertEqual(str, type(Place.description))
        self.assertIn("description", dir(placeModel))
        self.assertNotIn("desctiption", placeModel.__dict__)

    def test_number_rooms_is_public_class_attribute(self):
        placeModel = Place()
        self.assertEqual(int, type(Place.number_rooms))
        self.assertIn("number_rooms", dir(placeModel))
        self.assertNotIn("number_rooms", placeModel.__dict__)

    def test_number_bathrooms_is_public_class_attribute(self):
        placeModel = Place()
        self.assertEqual(int, type(Place.number_bathrooms))
        self.assertIn("number_bathrooms", dir(placeModel))
        self.assertNotIn("number_bathrooms", placeModel.__dict__)

    def test_max_guest_is_public_class_attribute(self):
        placeModel = Place()
        self.assertEqual(int, type(Place.max_guest))
        self.assertIn("max_guest", dir(placeModel))
        self.assertNotIn("max_guest", placeModel.__dict__)

    def test_price_by_night_is_public_class_attribute(self):
        placeModel = Place()
        self.assertEqual(int, type(Place.price_by_night))
        self.assertIn("price_by_night", dir(placeModel))
        self.assertNotIn("price_by_night", placeModel.__dict__)

    def test_latitude_is_public_class_attribute(self):
        placeModel = Place()
        self.assertEqual(float, type(Place.latitude))
        self.assertIn("latitude", dir(placeModel))
        self.assertNotIn("latitude", placeModel.__dict__)

    def test_longitude_is_public_class_attribute(self):
        placeModel = Place()
        self.assertEqual(float, type(Place.longitude))
        self.assertIn("longitude", dir(placeModel))
        self.assertNotIn("longitude", placeModel.__dict__)

    def test_amenity_ids_is_public_class_attribute(self):
        placeModel = Place()
        self.assertEqual(list, type(Place.amenity_ids))
        self.assertIn("amenity_ids", dir(placeModel))
        self.assertNotIn("amenity_ids", placeModel.__dict__)

    def test_two_places_unique_ids(self):
        placeModel1 = Place()
        placeModel2 = Place()
        self.assertNotEqual(placeModel1.id, placeModel2.id)

    def test_two_places_different_created_at(self):
        placeModel1 = Place()
        sleep(sleep_tm)
        placeModel2 = Place()
        self.assertLess(placeModel1.created_at, placeModel2.created_at)

    def test_two_places_different_updated_at(self):
        placeModel1 = Place()
        sleep(sleep_tm)
        placeModel2 = Place()
        self.assertLess(placeModel1.updated_at, placeModel2.updated_at)

    def test_str_representation(self):
        date_today = datetime.today()
        dateToday_repr = repr(date_today)
        placeModel = Place()
        placeModel.id = "123456"
        placeModel.created_at = placeModel.updated_at = date_today
        place_str = placeModel.__str__()
        self.assertIn("[Place] (123456)", place_str)
        self.assertIn("'id': '123456'", place_str)
        self.assertIn("'created_at': " + dateToday_repr, place_str)
        self.assertIn("'updated_at': " + dateToday_repr, place_str)

    def test_args_unused(self):
        placeModel = Place(None)
        self.assertNotIn(None, placeModel.__dict__.values())

    def test_instantiation_with_kwargs(self):
        date_today = datetime.today()
        dt_iso = date_today.isoformat()
        placeModel = Place(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(placeModel.id, "345")
        self.assertEqual(placeModel.created_at, date_today)
        self.assertEqual(placeModel.updated_at, date_today)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)


class TestPlace_save(unittest.TestCase):
    """Save method Unittests Place class."""

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
        placeModel = Place()
        sleep(sleep_tm)
        fst_updated_at = placeModel.updated_at
        placeModel.save()
        self.assertLess(fst_updated_at, placeModel.updated_at)

    def test_two_saves(self):
        placeModel = Place()
        sleep(sleep_tm)
        fst_updated_at = placeModel.updated_at
        placeModel.save()
        scd_updated_at = placeModel.updated_at
        self.assertLess(fst_updated_at, scd_updated_at)
        sleep(sleep_tm)
        placeModel.save()
        self.assertLess(scd_updated_at, placeModel.updated_at)

    def test_save_with_arg(self):
        placeModel = Place()
        with self.assertRaises(TypeError):
            placeModel.save(None)

    def test_save_updates_file(self):
        placeModel = Place()
        placeModel.save()
        plid = "Place." + placeModel.id
        with open("file.json", "r") as f:
            self.assertIn(plid, f.read())


class TestPlace_to_dict(unittest.TestCase):
    """to_dict Unittests Place class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Place().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        placeModel = Place()
        self.assertIn("id", placeModel.to_dict())
        self.assertIn("created_at", placeModel.to_dict())
        self.assertIn("updated_at", placeModel.to_dict())
        self.assertIn("__class__", placeModel.to_dict())

    def test_to_dict_contains_added_attributes(self):
        placeModel = Place()
        placeModel.middle_name = "AirBnb"
        placeModel.my_number = 98
        self.assertEqual("AirBnb", placeModel.middle_name)
        self.assertIn("my_number", placeModel.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        placeModel = Place()
        place_dictn = placeModel.to_dict()
        self.assertEqual(str, type(place_dictn["id"]))
        self.assertEqual(str, type(place_dictn["created_at"]))
        self.assertEqual(str, type(place_dictn["updated_at"]))

    def test_to_dict_output(self):
        date_today = datetime.today()
        placeModel = Place()
        placeModel.id = "123456"
        placeModel.created_at = placeModel.updated_at = date_today
        tdict = {
            'id': '123456',
            '__class__': 'Place',
            'created_at': date_today.isoformat(),
            'updated_at': date_today.isoformat(),
        }
        self.assertDictEqual(placeModel.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        placeModel = Place()
        self.assertNotEqual(placeModel.to_dict(), placeModel.__dict__)

    def test_to_dict_with_arg(self):
        placeModel = Place()
        with self.assertRaises(TypeError):
            placeModel.to_dict(None)


if __name__ == "__main__":
    unittest.main()
