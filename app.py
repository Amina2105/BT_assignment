import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.merkle_root = self.calculate_merkle_root()
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = str(self.index) + str(self.previous_hash) + str(self.timestamp) + str(self.merkle_root) + str(self.nonce)
        return hashlib.sha256(data.encode()).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")

    def calculate_merkle_root(self):
        if len(self.transactions) == 0:
            return "0"
        if len(self.transactions) == 1:
            return self.transactions[0]
        merkle_tree = self.transactions.copy()
        while len(merkle_tree) > 1:
            new_merkle_tree = []
            for i in range(0, len(merkle_tree), 2):
                left = merkle_tree[i]
                right = merkle_tree[i + 1] if i + 1 < len(merkle_tree) else ""
                combined = hashlib.sha256((left + right).encode()).hexdigest()
                new_merkle_tree.append(combined)
            merkle_tree = new_merkle_tree
        return merkle_tree[0]

