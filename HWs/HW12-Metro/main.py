from models import *
from admin import Admin
import pickle
import datetime
from exceptions import *

Trip.trips[0] = Trip(3000, datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=1))

login_type_menu = {
    1: "client login",
    2: "admin login"
}
_menu = {
    1: "signup",
    2: "login",
    3: "exit"
}


def print_menu(menu):
    for item in menu:
        print(f'{item}: {menu[item]}')


while True:
    print_menu(login_type_menu)
    while True:
        login_type = int(input("> "))
        if login_type in [1, 2]:
            break
        else:
            print("Wrong input!")
    op = login_type_menu.get(login_type)

    if op == "client login":

        while True:
            print_menu(_menu)
            use_type = int(input("> "))
            _op = _menu.get(use_type)

            if _op == "signup":
                first_name = input("Enter your first name: ")
                last_name = input("Enter your last name: ")
                while True:
                    try:
                        balance_bank_acc = int(input("Enter your balance bank account: "))
                        break
                    except ValueError:
                        print("You should enter a number not string!")
                        continue
                    new_bank_acc = BankAccount(balance_bank_acc)
                    phone_number = input("Enter your phone number: ")
                    ssn = input("Enter your National Code: ")
                    new_client = Client.signup(first_name, last_name, new_bank_acc, ssn, phone_number)
                    print(f'your ID is: {new_client.get_id()}')
                    break

                while True:
                    print("""
                    CARD TYPE:
                    1.One Way
                    2.Credit
                    3.Timed
                    """)
                    card_type = int(input("Your card type: "))
                    if card_type == 1:
                        while True:
                            try:
                                amount = int(input("Your Card Charge: "))
                            except ValueError:
                                print("You should enter a number not string!")
                                continue
                            new_client.bank_acc.withdraw(amount)
                            Client.update_clients_pickle()
                            Client.buy_card(card_type, amount, None)
                            print("FINISH!")
                            break
                        break

                    elif card_type == 2:
                        while True:
                            try:
                                amount = int(input("Your Card Charge: "))
                                new_client.bank_acc.withdraw(amount)
                                Client.update_clients_pickle()
                                print(f"balance in bank: {new_client.bank_acc.get_balance()}")
                                Client.buy_card(card_type, amount, None)
                                print("YOUR CARD CREATED!")
                                break
                            except ValueError:
                                print("You should enter a number not string!")
                                continue
                        break

                    elif card_type == 3:
                        now = datetime.datetime.now()
                        expiration = now + datetime.timedelta(minutes=1)
                        while True:
                            try:
                                amount = int(input("Your Card Charge: "))
                                break
                            except ValueError:
                                print("You should enter a number not string!")
                                continue
                        new_client.bank_acc.withdraw(amount)
                        Client.update_clients_pickle()
                        print(f"balance in bank: {new_client.bank_acc.get_balance()}")
                        Client.buy_card(card_type, amount, expiration)
                        print("YOUR CARD CREATED!")
                        break

                    else:
                        print("Wrong input!")

            elif _op == "login":
                while True:
                    input_ssn = input("Enter your National Code: ")
                    try:
                        print(f"your ID is: {Client.clients[input_ssn].get_id()}")
                        break
                    except KeyError:
                        print("There is no this national code!")
                        continue

                input_id = input("Enter your id:")
                while True:
                    print("""
                    1.Bank Account
                    2.Using Card & Choice Trip
                    3.exit
                    """)
                    choice = int(input("> "))
                    if choice == 1:
                        if input_ssn in Client.clients:
                            bank = Client.clients[input_ssn].bank_acc
                            print("""
                            1.withdraw
                            2.deposit
                            3.get balance
                            """)
                            inp = int(input("> "))
                            if inp == 1:
                                while True:
                                    try:
                                        withdrawal = int(input("Withdrawal amount > "))
                                        bank.withdraw(withdrawal)
                                        break
                                    except ValueError:
                                        print("You should enter a number not string!")
                                        continue
                            elif inp == 2:
                                while True:
                                    try:
                                        deposit = int(input("Deposit amount > "))
                                        bank.deposit(deposit)
                                    except ValueError:
                                        print("You should enter a number not string!")
                                        continue
                            elif inp == 3:
                                print(f"The remaining amount: {bank.get_balance()}")

                    elif choice == 2:

                        if input_id in Card.cards:
                            card = Card.cards[input_id]
                            if card.card_type == 1:
                                Trip.check_trip()
                                print(f"Trips are: {Trip.trips}")
                                trip = int(input("choice one: "))
                                card.one_way(trip)
                                print(f"Remaining charge: {card.card_amount}")
                                Card.cards.pop(input_id)
                                Card.update_cards_pickle()
                                break

                            elif card.card_type == 2:
                                while True:
                                    bank_acc_client = Client.clients[input_ssn].bank_acc
                                    print("""
                                    1.CHARGE CARD
                                    2.USE CARD
                                    3.EXIT
                                    """)
                                    user_input = int(input('CHOICE ONE: '))
                                    if user_input == 1:
                                        charge = int(input("price charge card: "))
                                        result = bank_acc_client.withdraw(charge)
                                        Client.update_clients_pickle()
                                        print(f"balance in bank: {bank_acc_client.get_balance()}")
                                        if result:
                                            card.card_charge(charge)
                                            Card.update_cards_pickle()
                                            print(f"Remaining charge: {card.card_amount}")
                                        else:
                                            print("card didn't charge!!!!")

                                    elif user_input == 2:
                                        res = Trip.check_trip()
                                        if not res:
                                            Trip.check_trip()
                                        print(f"Trips are: {Trip.trips}")
                                        trip = int(input("choice one: "))
                                        card.credit(trip)
                                        Card.update_cards_pickle()
                                        print(f"Remaining charge: {card.card_amount}")

                                    elif user_input == 3:
                                        break

                            elif card.card_type == 3:
                                while True:
                                    bank_acc_client = Client.clients[input_ssn].bank_acc
                                    print("""
                                    1.CHARGE CARD
                                    2.USE CARD
                                    3.EXIT
                                    """)
                                    user_input = int(input('CHOICE ONE: '))
                                    if user_input == 1:
                                        charge = int(input("price charge card: "))
                                        bank_acc_client.withdraw(charge)
                                        Client.update_clients_pickle()
                                        print(f"balance in bank: {bank_acc_client.get_balance()}")
                                        card.card_charge(charge)
                                        Card.update_cards_pickle()
                                        print(f"Remaining charge: {card.card_amount}")

                                    elif user_input == 2:
                                        res = Trip.check_trip()
                                        if not res:
                                            Trip.check_trip()
                                        print(f"Trips are: {Trip.trips}")
                                        trip = int(input("choice one: "))
                                        card.timed(trip)
                                        Card.update_cards_pickle()
                                        print(f"Remaining charge: {card.card_amount}")

                                    elif user_input == 3:
                                        break
                        else:
                            print("There is no Card with this ID!")

                    elif choice == 3:
                        break
            elif _op == "exit":
                break
            else:
                print("Wrong input!")

    elif op == "admin login":
        while True:
            print_menu(_menu)
            use_type = int(input("> "))
            _op = _menu.get(use_type)

            if _op == "signup":
                first_name = input("Enter your first name: ")
                last_name = input("Enter your last name: ")
                input_ssn = input("Enter your National Code: ")
                new_admin = Admin.new_admin(first_name, last_name, None, input_ssn, None)
                print(f'your ID is: {new_admin.get_id()}')

            elif _op == "login":
                while True:
                    input_ssn = input("Enter your National Code: ")
                    try:
                        print(f"your ID is: {Admin.admins[input_ssn].get_id()}")
                        break
                    except KeyError:
                        print("There is no this national code!")
                        continue
                input_id = input("Enter your id:")
                while True:
                    if input_ssn in Admin.admins:
                        _admin = Admin.admins[input_ssn]

                        print("""
                        1.Trip registration
                        2.Edit trips
                        3.exit
                        """)

                        inp = int(input("> "))
                        if inp == 1:
                            _admin.trip_registration()
                            print("GOOD!")
                        elif inp == 2:
                            _admin.edit_trips()
                            print("GOOD!")
                        elif inp == 3:
                            break

                    else:
                        print("There is no Admin with this SSN!")
                        break

            elif _op == "exit":
                break

            else:
                print("Wrong input!")
