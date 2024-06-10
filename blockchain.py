import hashlib
import json
import time


class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4

    def create_genesis_block(self):
        return Block(0, "0", int(time.time()), "Genesis Block")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block: Block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()

        # Mine the block
        self.mine_block(new_block)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                print(f"Block {i} has been tampered with. Hash is invalid.")
                return False

            if current_block.previous_hash != previous_block.hash:
                print(f"Block {i} has been tampered with. Previous hash is invalid.")
                return False
        return True

    def mine_block(self, block: Block):
        while block.hash[: self.difficulty] != "0" * self.difficulty:
            block.nonce += 1
            block.hash = block.calculate_hash()


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
