from models import *
import pickle
import uuid
import datetime
# check


class Admin(Client):
    admins = {}

    def __init__(self, first_name, last_name, bank_acc, ssn, phone_number):
        super().__init__(first_name, last_name, bank_acc, ssn, phone_number)
        self.__id = str(uuid.uuid4())
        self.ssn = ssn
        Admin.admins[self.ssn] = self

    def get_id(self):
        return self.__id

    @classmethod
    def new_admin(cls, first_name, last_name, ssn, bank_acc, phone_number):
        cls(first_name, last_name, ssn, bank_acc, phone_number)
        with open('admins.pickle', 'wb') as admins_info_file:
            pickle.dump(cls.admins, admins_info_file)
        return list(cls.admins.values())[-1]

    @staticmethod
    def trip_registration():
        cost = int(input("cost of trip: "))
        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(minutes=1)
        Trip.creat_trip(cost, start_time, end_time)

    @staticmethod
    def edit_trips():
        num_trip = int(input("Enter number of trip: "))
        Trip.trips.pop(num_trip)
        print("trip deleted!")
