import time
import hashlib
import json
from consensus import consensus, PoS, DPoS

class Block:
    def __init__(self, index, previous_hash, timestamp, data):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = self.cal_hash()

    def cal_hash(self):
        value = f'{self.index}{self.previous_hash}{self.timestamp}{self.data}'.encode() 
        return hashlib.sha256(value).hexdigest()
    
class EIP01Blockchain:
    def __init__(self, consensus_mechanism):
        self.chain = []
        self.consensus = consensus_mechanism
        self.create_gen_block()

    def create_gen_block(self):
        gen_block = {
            "index": 0,
            "previous_hash": "0",
            "timestamp": int(time.time()),
            "transactions": "Genesis Block",
            "hash": self.consensus.calculate_hash({"index": 0, "previous_hash": "0", "timestamp": int(time.time()), "transactions": "Genesis Block"})
        }
        self.chain.append(gen_block)

    def add_block(self, transactions):
        prev_block = self.chain[-1]
        block_data = {
            "index": len(self.chain),
            "previous_hash": prev_block["hash"],
            "timestamp": int(time.time()),
            "transactions": transactions
        }
        new_block = self.consensus.create_block(block_data, transactions)
        self.chain.append(new_block)

    def valid(self):
        for i in range(1, len(self.chain)):
            cur_block = self.chain[i]
            prev_block = self.chain[i - 1]
            if cur_block["hash"] != self.consensus.calculate_hash(cur_block):
                return False
            if cur_block["previous_hash"] != prev_block["hash"]:
                return False
        return True
