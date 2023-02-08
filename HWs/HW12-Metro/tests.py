import unittest
from models import *
import pickle


class TestModels(unittest.TestCase):
    def setUp(self) -> None:
        self.obj = Card.new_card(123456, 1, 5000, None)
        Trip.trips[0] = Trip(3000, datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=1))
        Trip.trips[1] = Trip(6000, datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=1))

    def test_new_card(self):
        self.assertIn(123456, Card.cards)
        self.assertEqual(Card.cards, {123456: self.obj})

    def test_one_way_charge_enough(self):
        result = self.obj.one_way(0)
        self.assertEqual(self.obj.card_amount, 2000)
        self.assertTrue(result)

    def test_one_way_charge_not_enough(self):
        result = self.obj.one_way(1)
        self.assertEqual(self.obj.card_amount, 5000)
        self.assertFalse(result)

    def test_credit_charge_enough(self):
        result = self.obj.credit(0)
        self.assertEqual(self.obj.card_amount, 2000)
        self.assertTrue(result)

    def test_credit_charge_not_enough(self):
        result = self.obj.credit(1)
        self.assertEqual(self.obj.card_amount, 5000)
        self.assertFalse(result)

    def test_timed_charge_enough(self):
        result = self.obj.timed(0)
        self.assertEqual(self.obj.card_amount, 2000)
        self.assertTrue(result)


    def test_card_charge(self):
        amount = self.obj.card_charge(4000)
        self.assertEqual(amount, 9000)


if __name__ == '__main__':
    unittest.main()
