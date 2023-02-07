class NotEnoughCharge(Exception):
    def __init__(self, message="not enough charge!"):
        self.message = message
        super().__init__(self.message)


class CardHasExpired(Exception):
    def __init__(self, message="Card has expired!"):
        self.message = message
        super().__init__(self.message)


class NotEnoughMoney(Exception):
    def __init__(self, message="Not enough money in bank!"):
        self.message = message
        super().__init__(self.message)
