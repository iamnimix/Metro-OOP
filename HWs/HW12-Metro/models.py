import pickle
import uuid
import datetime
from exceptions import *


class Card:
    cards = {}

    #   M1 ==> One Way
    #   M2 ==> Credit
    #   M3 ==> Timed

    def __init__(self, card_type=1, card_amount=3000, date=None):
        self.card_type = card_type
        self.card_amount = card_amount
        self.date = date

    @classmethod
    def new_card(cls, id, card_type, card_amount, date):
        cls.cards[id] = cls(card_type, card_amount, date)
        with open('cards.pickle', 'wb') as cards_info_file:
            pickle.dump(cls.cards, cards_info_file)

    @classmethod
    def update_cards_pickle(cls):
        with open('cards.pickle', 'wb') as cards_info_file:
            pickle.dump(cls.cards, cards_info_file)

    def one_way(self, trip_type):
        try:
            if self.card_amount < Trip.trips[trip_type].cost:
                raise NotEnoughCharge
            self.card_amount -= Trip.trips[trip_type].cost
        except NotEnoughCharge as e:
            print(e)
            return

    def credit(self, trip_type):
        try:
            if self.card_amount < Trip.trips[trip_type].cost:
                raise NotEnoughCharge
            self.card_amount -= Trip.trips[trip_type].cost
        except NotEnoughCharge as e:
            print(e)
            return

    def timed(self, trip_type):
        try:
            if not self.date > datetime.datetime.now():
                raise CardHasExpired
        except CardHasExpired as e:
            print(e)
        try:
            if self.card_amount < Trip.trips[trip_type].cost:
                raise NotEnoughCharge
            self.card_amount -= Trip.trips[trip_type].cost
        except NotEnoughCharge as e:
            print(e)
            return

    def card_charge(self, amount):
        self.card_amount += amount
        return self.card_amount


class Client:
    clients = {}

    def __init__(self, first_name, last_name, bank_acc, ssn, phone_number=None):
        self.first_name = first_name
        self.last_name = last_name
        self.bank_acc = bank_acc
        self.phone_number = phone_number
        self.ssn = ssn
        self.__id = str(uuid.uuid4())
        Client.clients[self.ssn] = self

    def get_id(self):
        return self.__id

    @classmethod
    def signup(cls, first_name, last_name, bank_acc, ssn, phone_number):
        cls(first_name, last_name, bank_acc, ssn, phone_number)
        with open('client.pickle', 'wb') as clients_info_file:
            pickle.dump(cls.clients, clients_info_file)
        return list(cls.clients.values())[-1]

    @classmethod
    def update_clients_pickle(cls):
        with open('client.pickle', 'wb') as clients_info_file:
            pickle.dump(cls.clients, clients_info_file)

    @classmethod
    def buy_card(cls, card_type, card_amount, date):
        Card.new_card(list(cls.clients.values())[-1].__id, card_type, card_amount, date)


class Trip:
    trips = {}
    trip_num = 1

    def __init__(self, cost, start_time, end_time):
        self.cost = cost
        self.start_time = start_time
        self.end_time = end_time
        Trip.trips[self.trip_num] = self
        self.trip_num += 1

    @classmethod
    def creat_trip(cls, cost, start_time, end_time):
        cls(cost, start_time, end_time)

    @classmethod
    def check_trip(cls):
        try:
            for k, v in cls.trips.items():
                if v.end_time < datetime.datetime.now():
                    cls.trips.pop(k)
                return True
        except Exception:
            return False


class BankAccount:
    MIN_BALANCE = 5000

    def __init__(self, initial_balance=MIN_BALANCE):
        self.__balance = initial_balance

    def __check_minimum_balance(self, amount):
        return (self.__balance - amount) >= self.MIN_BALANCE

    def withdraw(self, amount):
        try:
            if self.__check_minimum_balance(amount):
                self.__balance -= amount
                return True
            raise NotEnoughMoney
        except NotEnoughMoney as e:
            print(e)
            return False

    def deposit(self, amount):
        self.__balance += amount

    def get_balance(self):
        return self.__balance
