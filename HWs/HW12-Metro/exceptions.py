class NotEnoughCharge(Exception):
    def __init__(self, message="not enough charge!"):
        self.message = message
        super().__init__(self.message)


class CardHasExpired(Exception):
    def __init__(self, message="The card has expired"):
        self.message = message
        super().__init__(self.message)
