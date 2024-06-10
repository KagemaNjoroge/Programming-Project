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


# blockchain app


class VoteTransaction:
    def __init__(self, sender, receiver, votes):
        self.sender = sender
        self.receiver = receiver
        self.votes = votes
        self.timestamp = time.time()

    def to_dict(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "votes": self.votes,
            "timestamp": self.timestamp,
        }

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.votes} votes"


class VoteBlockChain(Blockchain):
    def __init__(self):
        super().__init__()
        self.pending_transactions = []

    def create_transaction(self, transaction: VoteTransaction):
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self):
        block_data = [tx.to_dict() for tx in self.pending_transactions]
        new_block = Block(
            index=len(self.chain),
            previous_hash=self.get_latest_block().hash,
            timestamp=int(time.time()),
            data=block_data,
        )
        self.add_block(new_block)
        self.pending_transactions = []
