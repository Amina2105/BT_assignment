import hashlib
import time

#Block class for individual blocks in the blockchain
class Block:
    def __init__(self, index, previous_hash, timestamp, transactions):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.merkle_root = self.calculate_merkle_root()
        self.nonce = 0
        self.hash = self.calculate_hash()
        
    #Calculate the hash of the block
    def calculate_hash(self):
        data = str(self.index) + str(self.previous_hash) + str(self.timestamp) + str(self.merkle_root) + str(self.nonce)
        return hashlib.sha256(data.encode()).hexdigest()

    #Proof-of-work (mining) to find a hash
    def mine_block(self, difficulty):
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")

    #Calculate the Merkle root of transactions in the block
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

#Define a Blockchain class to manage a chain of blocks
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2

    def create_genesis_block(self):
        return Block(0, "0", int(time.time()), [])

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

def main():
    blockchain = Blockchain()

    while True:
        print("\nBlockchain Console Interface")
        print("1. View Blockchain")
        print("2. Add Transaction")
        print("3. Mine Block")
        print("4. Verify Blockchain")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            print("\nBlockchain:")
            for block in blockchain.chain:
                print(f"Block {block.index}")
                print(f"Hash: {block.hash}")
                print(f"Timestamp: {block.timestamp}")
                print(f"Merkle Root: {block.merkle_root}")
                print("Transactions:")
                for transaction in block.transactions:
                    print(f"  - {transaction}")
                print("")

        elif choice == "2":
            sender = input("Enter sender: ")
            receiver = input("Enter receiver: ")
            amount = input("Enter amount: ")
            new_transaction = f"{sender} -> {receiver}: {amount}"
            blockchain.get_latest_block().transactions.append(new_transaction)
            print("Transaction added to the pending block.")

        elif choice == "3":
            new_block = Block(len(blockchain.chain), blockchain.get_latest_block().hash, int(time.time()), [])
            new_block.mine_block(blockchain.difficulty)
            blockchain.add_block(new_block)
            print("Block mined and added to the blockchain.")

        elif choice == "4":
            is_valid = blockchain.is_chain_valid()
            if is_valid:
                print("The blockchain is valid.")
            else:
                print("The blockchain is NOT valid.")

        elif choice == "5":
            print("Exiting the Blockchain Console Interface.")
            break

if __name__ == "__main__":
    main()
