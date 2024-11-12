import json
import time
import logging
import socket

# esi-01.py

# Set up logging
logging.basicConfig(level=logging.INFO)

class Blockchain:
    
    def __init__(self, name):
        self.name = name
        self.blocks = []
        self.mempool = []
        self.transaction_pool = {}  # Transaction pool for cross-chain transactions

    # Step 1: Add Transaction to Blockchain Mempool
    def add_transaction(self, transaction):
        if self.validate_transaction(transaction):
            self.mempool.append(transaction)
            logging.info(f"Transaction added to mempool: {transaction}")
        else:
            logging.warning(f"Invalid transaction: {transaction}")

    # Step 2: Validate Transaction (Check signature, balance, etc.)
    def validate_transaction(self, transaction):
        if not self.verify_signature(transaction):
            return False
        
        if not self.check_balance(transaction["sender"], transaction["amount"], transaction["fee"]):
            return False
        
        if self.is_double_spent(transaction["tx_id"]):
            return False
        
        if not self.is_valid_address(transaction["recipient"]):
            return False
        
        if not self.is_valid_fee(transaction["fee"]):
            return False
        
        return True
    
    # Dummy validation methods (for illustration purposes)
    def verify_signature(self, transaction):
        return True  # Signature verification logic goes here

    def check_balance(self, sender, amount, fee):
        return True  # Balance check logic goes here 

    def is_double_spent(self, tx_id):
        return False  # Double spending check goes here

    def is_valid_address(self, address):
        return True  # Address validity check goes here

    def is_valid_fee(self, fee):
        return True  # Fee validity check goes here

    # Step 3: Create Block (Update the blockchain with new transactions)
    def create_block(self):
        block = {
            "block_number": len(self.blocks) + 1,
            "transactions": self.mempool,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
        }
        
        self.blocks.append(block)
        self.mempool = []  # Clear the mempool after block creation
        logging.info(f"Block {block['block_number']} created with {len(block['transactions'])} transactions.")

    # Step 4: Start Block Creation Process (Creates blocks periodically)
    def start_block_creation(self):
        while True:
            if len(self.mempool) > 0:
                self.create_block()
            time.sleep(5)  # Wait for 5 seconds before creating the next block

    # Step 5: Handle Cross-Blockchain Transactions (Receiving transactions from ESI Mainnet)
    def handle_cross_blockchain_transaction(self, transaction):
        # Assume transaction includes cross-chain info like source blockchain, destination blockchain, etc.
        if transaction["source_blockchain"] != self.name:
            self.add_transaction(transaction)
            logging.info(f"Cross-chain transaction received and added to {self.name} mempool.")
        else:
            logging.warning(f"Transaction is from the same blockchain {self.name}, skipping.")

    # Step 6: Monitor Transaction Pool (Monitor for transactions sent to this blockchain)
    def monitor_transaction_pool(self, nodes):
        for node_name, port in nodes:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect(('localhost', port))  # Connect to the node (Mainnet or other sub-blockchain)
                    sock.sendall(b"Requesting transactions")
                    response = sock.recv(1024)
                    transaction = json.loads(response.decode())
                    self.handle_cross_blockchain_transaction(transaction)
            except Exception as e:
                logging.error(f"Failed to monitor {node_name}: {e}")

# Main Function to Start Blockchain (ESI-01)
if __name__ == "__main__":
    # Initialize the Blockchain (ESI-01)
    esi_blockchain = Blockchain("ESI-01")

    # Start the block creation process in a separate thread or process (for periodic block creation)
    import threading
    block_creation_thread = threading.Thread(target=esi_blockchain.start_block_creation)
    block_creation_thread.start()

    # Monitor communication with other blockchains (e.g., EIC-01, EID-01)
    while True:
        esi_blockchain.monitor_transaction_pool([("Mainnet", 8080), ("EIC-01", 12345), ("EID-01", 12346)])
        time.sleep(10)  # Poll every 10 seconds
