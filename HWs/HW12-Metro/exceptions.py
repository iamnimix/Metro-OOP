class NotEnoughCharge(Exception):
    def __init__(self, message="not enough charge!"):
        self.message = message
        super().__init__(self.message)


class CardHasExpired(Exception):
<<<<<<< HEAD
    def __init__(self, message="The card has expired"):
=======
    def __init__(self, message="Card has expired!"):
>>>>>>> develop
        self.message = message
        super().__init__(self.message)
