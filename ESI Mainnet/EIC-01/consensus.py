import hashlib
import json
import time
import random

class Consensus:
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def validate_block(self, block_data):
        pass

    def create_block(self, block_data):
        pass

    def calculate_hash(self, block_data):
        return hashlib.sha256(json.dumps(block_data, sort_keys=True).encode('utf-8')).hexdigest()

class PoW(Consensus):
    def __init__(self, blockchain, difficulty=4, block_reward=10):
        super().__init__(blockchain)
        self.difficulty = difficulty
        self.block_reward = block_reward

    def validate_block(self, block_data):
        return block_data["hash"][:self.difficulty] == "0" * self.difficulty

    def create_block(self, block_data, transactions):
        block_data["nonce"] = 0
        block_data["timestamp"] = int(time.time())
        block_data["transactions"] = transactions
        total_fees = sum([tx["fee"] for tx in transactions])
        block_data["reward"] = self.block_reward + total_fees
        block_data["hash"] = self.calculate_hash(block_data)
        
        while not self.validate_block(block_data):
            block_data["nonce"] += 1
            block_data["hash"] = self.calculate_hash(block_data)
        
        return block_data

    def calculate_hash(self, block_data):
        value = f'{block_data["nonce"]}{block_data["timestamp"]}{block_data["transactions"]}'.encode()
        return hashlib.sha256(value).hexdigest()

class PoS(Consensus):
    def __init__(self, blockchain, stakers):
        super().__init__(blockchain)
        self.stakers = stakers

    def validate_block(self, block_data):
        return block_data["validator"] in self.stakers

    def create_block(self, block_data):
        validator = self.select_validator()
        block_data["validator"] = validator
        block_data["hash"] = self.calculate_hash(block_data)
        return block_data

    def select_validator(self):
        total_stake = sum(self.stakers.values())
        validators = list(self.stakers.items())
        chosen_validator = random.choices(validators, weights=self.stakers.values())[0][0]
        return chosen_validator

    def calculate_hash(self, block_data):
        value = f'{block_data["validator"]}{block_data["timestamp"]}{block_data["previous_hash"]}'.encode()
        return hashlib.sha256(value).hexdigest()

class DPoS(Consensus):
    def __init__(self, blockchain, delegates):
        super().__init__(blockchain)
        self.delegates = delegates

    def validate_block(self, block_data):
        return block_data["delegate"] in self.delegates

    def create_block(self, block_data):
        delegate = self.select_delegate()
        block_data["delegate"] = delegate
        block_data["hash"] = self.calculate_hash(block_data)
        return block_data

    def select_delegate(self):
        return random.choice(self.delegates)
