import logging
import socket
import threading
from ESIMAINNET.esi_mainnet import ESI_Mainnet

logging.basicConfig(level=logging.INFO)

class ESI01MainBlockchain:
    def __init__(self, node_id, esi_mainnet, port):
        self.node_id = node_id
        self.role = "main_blockchain"
        self.port = port  
        self.peer_sockets = {}  
        self.esi_mainnet = esi_mainnet
        
    def start_main_blockchain(self):
        """Start the main blockchain server to listen for incoming transactions."""
        threading.Thread(target=self.listen_for_transactions, daemon=True).start()
        
    def listen_for_transactions(self):
        """Listen for incoming transactions from nodes or other blockchains."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', self.port))
            s.listen()
            logging.info(f"ESI-01 Node {self.node_id} listening for transactions on port {self.port}")
            while True:
                conn, addr = s.accept()
                threading.Thread(target=self.handle_transaction_message, args=(conn,), daemon=True).start()
                
    def handle_transaction_message(self, conn):
        """Handle transaction messages received from other nodes or sub-blockchains."""
        with conn:
            data = conn.recv(1024)
            if data:
                message = data.decode('utf-8')
                logging.info(f"ESI-01 Node {self.node_id} received transaction message: {message}")
                if "TRANSACTION" in message:
                    transaction = message.split(":")[1]
                    self.verify_and_route_transaction(transaction)
                    
    def verify_and_route_transaction(self, transaction):
        """Verify the transaction and route it to the correct sub-blockchain."""
        logging.info(f"ESI-01 Node {self.node_id} verifying transaction: {transaction}")
        
        if self.esi_mainnet.verify_transaction(transaction):
            logging.info(f"Transaction {transaction} verified successfully by ESI Mainnet.")
            self.route_transaction_to_subblockchain(transaction)
        else:
            logging.warning(f"Transaction {transaction} failed verification by ESI Mainnet.")

    def route_transaction_to_subblockchain(self, transaction):
        """Route the verified transaction to the appropriate sub-blockchain."""
        logging.info(f"ESI-01 Node {self.node_id} routing verified transaction to sub-blockchain.")
        sub_blockchain_port = 7000 
        self.send_to_subblockchain(sub_blockchain_port, transaction)
    
    def send_to_subblockchain(self, port, transaction):
        """Send the transaction to a specific sub-blockchain."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('localhost', port))
                s.sendall(f"TRANSACTION:{transaction}".encode('utf-8'))
                logging.info(f"ESI-01 Node {self.node_id} sent transaction to sub-blockchain on port {port}")
        except Exception as e:
            logging.error(f"Error sending transaction to sub-blockchain on port {port}: {e}")
    
if __name__ == "__main__":
    esi_mainnet = ESI_Mainnet() 
    esi_01_node = ESI_01_MainBlockchain(node_id=1, esi_mainnet=esi_mainnet, port=6000)
    esi_01_node.start_main_blockchain()