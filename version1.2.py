import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, transactions, timestamp):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_content = f"{self.index}{self.previous_hash}{self.transactions}{self.timestamp}{self.nonce}"
        return hashlib.sha256(block_content.encode()).hexdigest()

    def mine_block(self, difficulty):
        # Process of mining for hash, starting from zero (difficulty)
        target = "1" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block {self.index} is 'mined' with hash: {self.hash}")

class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.pending_transactions = []
        self.mining_reward = 100

    def create_genesis_block(self):
        return Block(0, "0", "Genesis Block", time.time())

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
                print(f"Хешът на блока {current_block.index} е невалиден!")
                return False

            if current_block.previous_hash != previous_block.hash:
                print(f"Хеш връзката между блок {previous_block.index} и блок {current_block.index} е невалидна!")
                return False
        return True

    def create_transaction(self, sender, recipient, amount):
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_address):
        block = Block(len(self.chain), self.get_latest_block().hash, self.pending_transactions, time.time())
        block.mine_block(self.difficulty)

        print(f"Transactions done. Miner {miner_address} get a price.")
        self.chain.append(block)

        # miner award
        self.pending_transactions = [{"sender": "System", "recipient": miner_address, "amount": self.mining_reward}]

    def show_chain(self):
        for block in self.chain:
            print(f"Index: {block.index}")
            print(f"Last Hash: {block.previous_hash}")
            print(f"Now Hash: {block.hash}")
            print(f"Transaction: {block.transactions}")
            print("-" * 30)

# Creating blockchain and transactions
my_blockchain = Blockchain(difficulty=2)
my_blockchain.create_transaction("Alice", "Bob", 50)
my_blockchain.create_transaction("Bob", "Charlie", 25)

# Mining transactions
my_blockchain.mine_pending_transactions("NasLion")

# Blockchain status
my_blockchain.show_chain()

# Checking blockchain status
print(f"Is the blockchain valid? {my_blockchain.is_chain_valid()}")
