import hashlib
import json

# consensus.py

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
    def __init__(self, blockchain, difficulty=4):
        super().__init__(blockchain)
        self.difficulty = difficulty  # How many leading zeros in the hash

    def validate_block(self, block_data):
        # Validate if the hash starts with the required number of zeros
        return block_data["hash"][:self.difficulty] == "0" * self.difficulty

    def create_block(self, block_data):
        # Perform mining: find the correct hash with sufficient leading zeros
        block_data["nonce"] = 0
        block_data["hash"] = self.calculate_hash(block_data)
        while not self.validate_block(block_data):
            block_data["nonce"] += 1
            block_data["hash"] = self.calculate_hash(block_data)
        return block_data

class PoS(Consensus):
    def __init__(self, blockchain, stakers):
        super().__init__(blockchain)
        self.stakers = stakers  # Dictionary of stakers and their stakes

    def validate_block(self, block_data):
        # In PoS, we assume the block is valid if it comes from a valid validator
        return block_data["validator"] in self.stakers

    def create_block(self, block_data):
        # Select a validator based on stakes (this is a simple random choice for demonstration)
        validator = self.select_validator()
        block_data["validator"] = validator
        block_data["hash"] = self.calculate_hash(block_data)
        return block_data

    def select_validator(self):
        # Select a validator randomly weighted by their stake
        total_stake = sum(self.stakers.values())
        weighted_stake = {k: v / total_stake for k, v in self.stakers.items()}
        return max(weighted_stake, key=weighted_stake.get)  # Simple selection of the highest stake

class DPoS(Consensus):
    def __init__(self, blockchain, delegates):
        super().__init__(blockchain)
        self.delegates = delegates  # List of active delegates

    def validate_block(self, block_data):
        # In DPoS, the block is valid if it is created by a registered delegate
        return block_data["delegate"] in self.delegates

    def create_block(self, block_data):
        # Pick a delegate to create the block
        delegate = self.select_delegate()
        block_data["delegate"] = delegate
        block_data["hash"] = self.calculate_hash(block_data)
        return block_data

    def select_delegate(self):
        # In a simple implementation, we randomly pick one of the delegates
        import random
        return random.choice(self.delegates)
