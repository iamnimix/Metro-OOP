import unittest
from models import *
import pickle


class TestModels(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_new_card(self):
        obj = Card.new_card(123456, 1, 5000, None)
        self.assertIn(123456, Card.cards)
        self.assertEqual(Card.cards, {123456: obj})


if __name__ == '__main__':
    unittest.main()
