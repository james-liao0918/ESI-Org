import hashlib
import json

class Consensus:
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def validate_block(self, block_data):
        pass

    def create_block(self, block_data):
        pass

    def calculate_hash(self, block_data):
        return hashlib.sha256(json.dumps(block_data, sort_keys=True).encode('utf-8')).hexdigest()

class PoS(Consensus):
    def __init__(self, blockchain, stakers):
        super().__init__(blockchain)
        self.stakers = stakers

    def validate_block(self, block_data):
        return block_data["validator"] in self.stakers

    def create_block(self, block_data, transactions):
        validator = self.select_validator()
        block_data["validator"] = validator
        block_data["timestamp"] = int(time.time())
        block_data["transactions"] = transactions
        block_data["hash"] = self.calculate_hash(block_data)
        return block_data

    def select_validator(self):
        total_stake = sum(self.stakers.values())
        weighted_stake = {k: v / total_stake for k, v in self.stakers.items()}
        return max(weighted_stake, key=weighted_stake.get)

    def calculate_hash(self, block_data):
        value = f'{block_data["validator"]}{block_data["timestamp"]}{block_data["transactions"]}'.encode()
        return hashlib.sha256(value).hexdigest()

class DPoS(Consensus):
    def __init__(self, blockchain, delegates):
        super().__init__(blockchain)
        self.delegates = delegates

    def validate_block(self, block_data):
        return block_data["delegate"] in self.delegates

    def create_block(self, block_data, transactions):
        delegate = self.select_delegate()
        block_data["delegate"] = delegate
        block_data["timestamp"] = int(time.time())
        block_data["transactions"] = transactions
        block_data["hash"] = self.calculate_hash(block_data)
        return block_data

    def select_delegate(self):
        return random.choice(self.delegates)

    def calculate_hash(self, block_data):
        value = f'{block_data["delegate"]}{block_data["timestamp"]}{block_data["transactions"]}'.encode()
        return hashlib.sha256(value).hexdigest()
    