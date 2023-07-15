#!/usr/bin/python3
"""Init models/state.py unittests.
Unittest classes:
    TestState_instantiation
    TestState_save
    TestState_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State

global sleep_tm
sleep_tm = 0.05


class TestState_instantiation(unittest.TestCase):
    """Unittests  instantiation"""

    def test_no_args_instantiates(self):
        self.assertEqual(State, type(State()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(State(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(State().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().updated_at))

    def test_name_is_public_class_attribute(self):
        stateModel = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(stateModel))
        self.assertNotIn("name", stateModel.__dict__)

    def test_two_states_unique_ids(self):
        stateModel1 = State()
        stateModel2 = State()
        self.assertNotEqual(stateModel1.id, stateModel2.id)

    def test_two_states_different_created_at(self):
        stateModel1 = State()
        sleep(sleep_tm)
        stateModel2 = State()
        self.assertLess(stateModel1.created_at, stateModel2.created_at)

    def test_two_states_different_updated_at(self):
        stateModel1 = State()
        sleep(sleep_tm)
        stateModel2 = State()
        self.assertLess(stateModel1.updated_at, stateModel2.updated_at)

    def test_str_representation(self):
        today_date = datetime.today()
        todayDate_repr = repr(today_date)
        stateModel = State()
        stateModel.id = "123456"
        stateModel.created_at = stateModel.updated_at = today_date
        stateModel_str = stateModel.__str__()
        self.assertIn("[State] (123456)", stateModel_str)
        self.assertIn("'id': '123456'", stateModel_str)
        self.assertIn("'created_at': " + todayDate_repr, stateModel_str)
        self.assertIn("'updated_at': " + todayDate_repr, stateModel_str)

    def test_args_unused(self):
        stateModel = State(None)
        self.assertNotIn(None, stateModel.__dict__.values())

    def test_instantiation_with_kwargs(self):
        today_date = datetime.today()
        today_iso = today_date.isoformat()
        stateModel = State(id="345", created_at=today_iso,
                           updated_at=today_iso)
        self.assertEqual(stateModel.id, "345")
        self.assertEqual(stateModel.created_at, today_date)
        self.assertEqual(stateModel.updated_at, today_date)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestState_save(unittest.TestCase):
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
        stateModel = State()
        sleep(sleep_tm)
        fst_updated_at = stateModel.updated_at
        stateModel.save()
        self.assertLess(fst_updated_at, stateModel.updated_at)

    def test_two_saves(self):
        stateModel = State()
        sleep(sleep_tm)
        fst_updated_at = stateModel.updated_at
        stateModel.save()
        scd_updated_at = stateModel.updated_at
        self.assertLess(fst_updated_at, scd_updated_at)
        sleep(sleep_tm)
        stateModel.save()
        self.assertLess(scd_updated_at, stateModel.updated_at)

    def test_save_with_arg(self):
        stateModel = State()
        with self.assertRaises(TypeError):
            stateModel.save(None)

    def test_save_updates_file(self):
        stateModel = State()
        stateModel.save()
        state_id = "State." + stateModel.id
        with open("file.json", "r") as f:
            self.assertIn(state_id, f.read())


class TestState_to_dict(unittest.TestCase):
    """Unittests to_dict method"""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(State().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        stateModel = State()
        self.assertIn("id", stateModel.to_dict())
        self.assertIn("created_at", stateModel.to_dict())
        self.assertIn("updated_at", stateModel.to_dict())
        self.assertIn("__class__", stateModel.to_dict())

    def test_to_dict_contains_added_attributes(self):
        stateModel = State()
        stateModel.middle_name = "Airbanb"
        stateModel.my_number = 98
        self.assertEqual("Airbanb", stateModel.middle_name)
        self.assertIn("my_number", stateModel.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        stateModel = State()
        state_dictn = stateModel.to_dict()
        self.assertEqual(str, type(state_dictn["id"]))
        self.assertEqual(str, type(state_dictn["created_at"]))
        self.assertEqual(str, type(state_dictn["updated_at"]))

    def test_to_dict_output(self):
        today_date = datetime.today()
        stateModel = State()
        stateModel.id = "123456"
        stateModel.created_at = stateModel.updated_at = today_date
        tdict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': today_date.isoformat(),
            'updated_at': today_date.isoformat(),
        }
        self.assertDictEqual(stateModel.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        stateModel = State()
        self.assertNotEqual(stateModel.to_dict(), stateModel.__dict__)

    def test_to_dict_with_arg(self):
        stateModel = State()
        with self.assertRaises(TypeError):
            stateModel.to_dict(None)


if __name__ == "__main__":
    unittest.main()
