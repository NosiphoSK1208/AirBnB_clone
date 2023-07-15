#!/usr/bin/python3
"""Init  for models/user.py unittests.
Unittest classes:
    TestUser_instantiation
    TestUser_save
    TestUser_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.user import User

global sleep_tm
sleep_tm = 0.05

class TestUser_instantiation(unittest.TestCase):
    """Unittests instantiation"""

    def test_no_args_instantiates(self):
        self.assertEqual(User, type(User()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(User(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(User().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(User().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(User().updated_at))

    def test_email_is_public_str(self):
        self.assertEqual(str, type(User.email))

    def test_password_is_public_str(self):
        self.assertEqual(str, type(User.password))

    def test_first_name_is_public_str(self):
        self.assertEqual(str, type(User.first_name))

    def test_last_name_is_public_str(self):
        self.assertEqual(str, type(User.last_name))

    def test_two_users_unique_ids(self):
        userModel1 = User()
        userModel2 = User()
        self.assertNotEqual(userModel1.id, userModel2.id)

    def test_two_users_different_created_at(self):
        userModel1 = User()
        sleep(sleep_tm)
        userModel2 = User()
        self.assertLess(userModel1.created_at, userModel2.created_at)

    def test_two_users_different_updated_at(self):
        userModel1 = User()
        sleep(sleep_tm)
        userModel2 = User()
        self.assertLess(userModel1.updated_at, userModel2.updated_at)

    def test_str_representation(self):
        date_today = datetime.today()
        dateToday_repr = repr(date_today)
        userModel = User()
        userModel.id = "123456"
        userModel.created_at = userModel.updated_at = date_today
        usstr = userModel.__str__()
        self.assertIn("[User] (123456)", usstr)
        self.assertIn("'id': '123456'", usstr)
        self.assertIn("'created_at': " + dateToday_repr, usstr)
        self.assertIn("'updated_at': " + dateToday_repr, usstr)

    def test_args_unused(self):
        userModel = User(None)
        self.assertNotIn(None, userModel.__dict__.values())

    def test_instantiation_with_kwargs(self):
        date_today = datetime.today()
        dateToday_iso = date_today.isoformat()
        userModel = User(id="345", created_at=dateToday_iso, updated_at=dateToday_iso)
        self.assertEqual(userModel.id, "345")
        self.assertEqual(userModel.created_at, date_today)
        self.assertEqual(userModel.updated_at, date_today)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class TestUser_save(unittest.TestCase):
    """Unittests save method"""

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
        userModel = User()
        sleep(sleep_tm)
        fst_updated_at = userModel.updated_at
        userModel.save()
        self.assertLess(fst_updated_at, userModel.updated_at)

    def test_two_saves(self):
        userModel = User()
        sleep(sleep_tm)
        fst_updated_at = userModel.updated_at
        userModel.save()
        scd_updated_at = userModel.updated_at
        self.assertLess(fst_updated_at, scd_updated_at)
        sleep(sleep_tm)
        userModel.save()
        self.assertLess(scd_updated_at, userModel.updated_at)

    def test_save_with_arg(self):
        userModel = User()
        with self.assertRaises(TypeError):
            userModel.save(None)

    def test_save_updates_file(self):
        userModel = User()
        userModel.save()
        usid = "User." + userModel.id
        with open("file.json", "r") as f:
            self.assertIn(usid, f.read())


class TestUser_to_dict(unittest.TestCase):
    """Unittests to_dict method"""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(User().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        userModel = User()
        self.assertIn("id", userModel.to_dict())
        self.assertIn("created_at", userModel.to_dict())
        self.assertIn("updated_at", userModel.to_dict())
        self.assertIn("__class__", userModel.to_dict())

    def test_to_dict_contains_added_attributes(self):
        userModel = User()
        userModel.middle_name = "Airbnb"
        userModel.my_number = 98
        self.assertEqual("Airbnb", userModel.middle_name)
        self.assertIn("my_number", userModel.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        userModel = User()
        user_dictn = userModel.to_dict()
        self.assertEqual(str, type(user_dictn["id"]))
        self.assertEqual(str, type(user_dictn["created_at"]))
        self.assertEqual(str, type(user_dictn["updated_at"]))

    def test_to_dict_output(self):
        date_today = datetime.today()
        userModel = User()
        userModel.id = "123456"
        userModel.created_at = userModel.updated_at = date_today
        tdict = {
            'id': '123456',
            '__class__': 'User',
            'created_at': date_today.isoformat(),
            'updated_at': date_today.isoformat(),
        }
        self.assertDictEqual(userModel.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        userModel = User()
        self.assertNotEqual(userModel.to_dict(), userModel.__dict__)

    def test_to_dict_with_arg(self):
        userModel = User()
        with self.assertRaises(TypeError):
            userModel.to_dict(None)


if __name__ == "__main__":
    unittest.main()