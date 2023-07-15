#!/usr/bin/python3
"""Init models/review.py unittests.
Unittest classes:
    TestReview_instantiation
    TestReview_save
    TestReview_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.review import Review

global sleep_tm
sleep_tm = 0.05


class TestReview_instantiation(unittest.TestCase):
    """Unittests instantiation"""

    def test_no_args_instantiates(self):
        self.assertEqual(Review, type(Review()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Review(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Review().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Review().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Review().updated_at))

    def test_place_id_is_public_class_attribute(self):
        reviewModel = Review()
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(reviewModel))
        self.assertNotIn("place_id", reviewModel.__dict__)

    def test_user_id_is_public_class_attribute(self):
        reviewModel = Review()
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(reviewModel))
        self.assertNotIn("user_id", reviewModel.__dict__)

    def test_text_is_public_class_attribute(self):
        reviewModel = Review()
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(reviewModel))
        self.assertNotIn("text", reviewModel.__dict__)

    def test_two_reviews_unique_ids(self):
        reviewModel1 = Review()
        reviewModel2 = Review()
        self.assertNotEqual(reviewModel1.id, reviewModel2.id)

    def test_two_reviews_different_created_at(self):
        reviewModel1 = Review()
        sleep(sleep_tm)
        reviewModel2 = Review()
        self.assertLess(reviewModel1.created_at, reviewModel2.created_at)

    def test_two_reviews_different_updated_at(self):
        reviewModel1 = Review()
        sleep(sleep_tm)
        reviewModel2 = Review()
        self.assertLess(reviewModel1.updated_at, reviewModel2.updated_at)

    def test_str_representation(self):
        date_today = datetime.today()
        dateToday_repr = repr(date_today)
        reviewModel = Review()
        reviewModel.id = "123456"
        reviewModel.created_at = reviewModel.updated_at = date_today
        review_str = reviewModel.__str__()
        self.assertIn("[Review] (123456)", review_str)
        self.assertIn("'id': '123456'", review_str)
        self.assertIn("'created_at': " + dateToday_repr, review_str)
        self.assertIn("'updated_at': " + dateToday_repr, review_str)

    def test_args_unused(self):
        reviewModel = Review(None)
        self.assertNotIn(None, reviewModel.__dict__.values())

    def test_instantiation_with_kwargs(self):
        date_today = datetime.today()
        today_ios = date_today.isoformat()
        reviewModel = Review(
            id="345", created_at=today_ios, updated_at=today_ios)
        self.assertEqual(reviewModel.id, "345")
        self.assertEqual(reviewModel.created_at, date_today)
        self.assertEqual(reviewModel.updated_at, date_today)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestReview_save(unittest.TestCase):
    """Unittests save method"""

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
        reviewModel = Review()
        sleep(sleep_tm)
        fst_updated_at = reviewModel.updated_at
        reviewModel.save()
        self.assertLess(fst_updated_at, reviewModel.updated_at)

    def test_two_saves(self):
        reviewModel = Review()
        sleep(sleep_tm)
        fst_updated_at = reviewModel.updated_at
        reviewModel.save()
        scd_updated_at = reviewModel.updated_at
        self.assertLess(fst_updated_at, scd_updated_at)
        sleep(sleep_tm)
        reviewModel.save()
        self.assertLess(scd_updated_at, reviewModel.updated_at)

    def test_save_with_arg(self):
        reviewModel = Review()
        with self.assertRaises(TypeError):
            reviewModel.save(None)

    def test_save_updates_file(self):
        reviewModel = Review()
        reviewModel.save()
        rvid = "Review." + reviewModel.id
        with open("obj_file.json", "r") as f:
            self.assertIn(rvid, f.read())


class TestReview_to_dict(unittest.TestCase):
    """Unittests  to_dict method"""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Review().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        reviewModel = Review()
        self.assertIn("id", reviewModel.to_dict())
        self.assertIn("created_at", reviewModel.to_dict())
        self.assertIn("updated_at", reviewModel.to_dict())
        self.assertIn("__class__", reviewModel.to_dict())

    def test_to_dict_contains_added_attributes(self):
        reviewModel = Review()
        reviewModel.middle_name = "Airbanb"
        reviewModel.my_number = 98
        self.assertEqual("Airbanb", reviewModel.middle_name)
        self.assertIn("my_number", reviewModel.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        reviewModel = Review()
        review_dictn = reviewModel.to_dict()
        self.assertEqual(str, type(review_dictn["id"]))
        self.assertEqual(str, type(review_dictn["created_at"]))
        self.assertEqual(str, type(review_dictn["updated_at"]))

    def test_to_dict_output(self):
        date_today = datetime.today()
        reviewModel = Review()
        reviewModel.id = "123456"
        reviewModel.created_at = reviewModel.updated_at = date_today
        tdict = {
            'id': '123456',
            '__class__': 'Review',
            'created_at': date_today.isoformat(),
            'updated_at': date_today.isoformat(),
        }
        self.assertDictEqual(reviewModel.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        reviewModel = Review()
        self.assertNotEqual(reviewModel.to_dict(), reviewModel.__dict__)

    def test_to_dict_with_arg(self):
        reviewModel = Review()
        with self.assertRaises(TypeError):
            reviewModel.to_dict(None)


if __name__ == "__main__":
    unittest.main()
