from blockchain import Blockchain


class User:
    def __init__(self, uuid, balance=0):
        self.uuid = uuid
        self.balance = balance

    def __str__(self):
        return self.uuid

    def to_dict(self):
        return {"uuid": self.name, "balance": self.balance}


class Transaction:
    def __init__(self, sender: User, receiver: User, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.amount}"

    def to_dict(self):
        return {"sender": self.sender, "receiver": self.receiver, "amount": self.amount}

    @staticmethod
    def from_dict(transaction_dict):
        return Transaction(
            transaction_dict["sender"],
            transaction_dict["receiver"],
            transaction_dict["amount"],
        )


class VoteBlockChain:
    def __init__(self) -> None:
        self.chain = Blockchain()
        self.users = []
        self.pending_transactions = []

    def add_user(self, user: User):
        self.users.append(user)

    def validate_if_user_has_enough_to_transfer(self, uuid, amount: int):
        for user in self.users:
            if user.uuid == uuid:
                if user.balance >= amount:
                    return True
                else:
                    return False
        return False

    def add_transaction(self, transaction: Transaction):
        if not self.validate_if_user_has_enough_to_transfer(
            transaction.sender.uuid, transaction.amount
        ):
            return False
        else:
            transaction.sender.balance -= transaction.amount
            transaction.receiver.balance += transaction.amount
            return True

    def get_user_balance(self, uuid):
        for user in self.users:
            if user.uuid == uuid:
                return user.balance
        return None
