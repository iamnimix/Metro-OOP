import unittest
from models import *
import pickle


class TestModels(unittest.TestCase):
    def setUp(self) -> None:
        self.card_obj = Card.new_card(123456, 1, 5000, None)
        Trip.trips[0] = Trip(3000, datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=1))
        Trip.trips[1] = Trip(6000, datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=1))
        self.bank_obj = BankAccount(500000)
        self.client_obj = Client.signup('nima', 'abarghooie', self.bank_obj, '0025470558', None)
        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(minutes=1)
        self.trip_obj = Trip.creat_trip(9000, start_time, end_time)

    def test_new_card(self):
        self.assertIn(123456, Card.cards)
        self.assertEqual(Card.cards, {123456: self.card_obj})

    def test_one_way_charge_enough(self):
        result = self.card_obj.one_way(0)
        self.assertEqual(self.card_obj.card_amount, 2000)
        self.assertTrue(result)

    def test_one_way_charge_not_enough(self):
        result = self.card_obj.one_way(1)
        self.assertEqual(self.card_obj.card_amount, 5000)
        self.assertFalse(result)

    def test_credit_charge_enough(self):
        result = self.card_obj.credit(0)
        self.assertEqual(self.card_obj.card_amount, 2000)
        self.assertTrue(result)

    def test_credit_charge_not_enough(self):
        result = self.card_obj.credit(1)
        self.assertEqual(self.card_obj.card_amount, 5000)
        self.assertFalse(result)

    def test_card_charge(self):
        amount = self.card_obj.card_charge(4000)
        self.assertEqual(amount, 9000)

    def test_signup(self):
        self.assertIn('0025470558', Client.clients)
        self.assertEqual(Client.clients, {'0025470558': self.client_obj})

    def test_withdraw_true(self):
        res = self.bank_obj.withdraw(400000)
        self.assertTrue(res)
        self.assertEqual(self.bank_obj.get_balance(), 100000)

    def test_withdraw_false(self):
        res = self.bank_obj.withdraw(500000)
        self.assertFalse(res)
        self.assertEqual(self.bank_obj.get_balance(), 500000)

    def test_deposit(self):
        self.bank_obj.deposit(100000)
        self.assertEqual(self.bank_obj.get_balance(), 600000)


if __name__ == '__main__':
    unittest.main()
