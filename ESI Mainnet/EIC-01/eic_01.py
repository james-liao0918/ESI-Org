import hashlib
import time
from consensus import Consensus, PoS, PoW, DPoS

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

class EIC01Blockchain:
    def __init__(self):
        self.chain = []
        self.create_gen_block()

    def create_gen_block(self):
        gen_block = Block(0, "0", int(time.time()), "Genesis Block")
        self.chain.append(gen_block)

    def add_block(self, data):
        prev_block = self.chain[-1]
        new_block = Block(len(self.chain), prev_block.hash, int(time.time()), data)
        self.chain.append(new_block)

    def valid(self):
        for i in range(1, len(self.chain)):
            cur_block = self.chain[i]
            prev_block = self.chain[i - 1]
            if cur_block.hash != cur_block.cal_hash():
                return False
            if cur_block.previous_hash != prev_block.hash: 
                return False
        return True
