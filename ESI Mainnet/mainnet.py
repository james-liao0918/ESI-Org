import datetime

class Blockchain:
    
    def __init__(self, name, block_time_interval):
        self.name = name
        self.block_time_interval = block_time_interval
        self.blocks = []
        self.transactions = []
        
    def add_transactions(self, transaction):
        self.transactions.append(transactions)
        print(f"transaction added to {self.name}")
        
    def create_block(self):
        current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if len(self.blocks) == 0:
            previous_hash = None
        else:
            previous_hash = self.blocks[-1]["hash"]
        
        block = {
            "index": len(self.blocks) + 1,
            "timestamp": current_timestamp,
            "previous_hash": previous_hash,
        }
        
        block["hash"] = self.generate_block_hash(block)
        self.blocks.append(block)
        self.transactions = []
        print(f"Block {block['index']} created for {self.name} at {current_timestamp}")
    
    def generate_block_hash(self, block):
        return f"hash_{block["index"]}"
    
    def start_block_creation(self):
        print(f"Starting block creation for {self.name} every {self.block_time_interval} seconds")
        self.create_block()
        
class ESI_Mainnet:
    
    def __init__(self):
        self.blockchains = []
        
    def add_blockchain(self, blockchain):
        self.blockchains.append(blockchain)
        print(f"blockchain {blockchain.name} added to ESI Mainnet")
        
    def start_network(self):
        print("Starting the ESI Mainnet")
        for blockchain in self.blockchains:
            blockchain.start_block_creation()

    def list_blockchains(self):
        print("Blockchains under the ESI Mainnet:")
        for blockchain in self.blockchains:
            print(f"- {blockchain.name}")

ESI_Mainnet = ESI_Mainnet()

ESI_01 = Blockchain("ESI-01", block_time_interval=2)
EIC_01 = Blockchain("EIC-01", block_time_interval=4)
EIP_01 = Blockchain("EIP-01", block_time_interval=6)
EID_01 = Blockchain("EID-01", block_time_interval=8)
EIO_01 = Blockchain("EIO-01", block_time_interval=10)
EIE_01 = Blockchain("EIE-01", block_time_interval=12)
EIB_01 = Blockchain("EIB-01", block_time_interval=14)
EIBE_01 = Blockchain("EIBE-01", block_time_interval=16)

ESI_Mainnet.add_blockchain(ESI_01)
ESI_Mainnet.add_blockchain(EIC_01)
ESI_Mainnet.add_blockchain(EIP_01)
ESI_Mainnet.add_blockchain(EID_01)
ESI_Mainnet.add_blockchain(EIO_01)
ESI_Mainnet.add_blockchain(EIE_01)
ESI_Mainnet.add_blockchain(EIB_01)
ESI_Mainnet.add_blockchain(EIBE_01)

ESI_Mainnet.list_blockchains()
ESI_Mainnet.start_network()
