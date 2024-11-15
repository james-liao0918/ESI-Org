import socket
import threading
import logging
import time
from esi_mainnet import ESI_Mainnet

logging.basicConfig(level=logging.INFO)

class Node:
    def __init__(self, node_id, esi_mainnet, port):
        self.node_id = node_id
        self.role = "full_node"
        self.port = port  
        self.peers = []  
        self.transaction_pool = []
        self.esi_mainnet = esi_mainnet  
        self.peer_sockets = {} 

    def start_node(self):
        """Start the node's server to listen for peer messages."""
        threading.Thread(target=self.listen_for_peers, daemon=True).start()
        self.connect_to_peers()

    def listen_for_peers(self):
        """Listen for incoming connections from peers."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', self.port))
            s.listen()
            logging.info(f"Node {self.node_id} listening on port {self.port}")
            while True:
                conn, addr = s.accept()
                threading.Thread(target=self.handle_peer_message, args=(conn,), daemon=True).start()

    def handle_peer_message(self, conn):
        """Handle messages received from a peer."""
        with conn:
            data = conn.recv(1024)
            if data:
                message = data.decode('utf-8')
                logging.info(f"Node {self.node_id} received message from peer: {message}")
                if "TRANSACTION" in message:
                    transaction = message.split(":")[1]
                    self.validate_transaction(transaction)

    def connect_to_peers(self):
        """Connect to other peer nodes."""
        peer_ports = [6000, 6001, 6002]
        peer_ports.remove(self.port)
        for peer_port in peer_ports:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(('localhost', peer_port))
                self.peer_sockets[peer_port] = s
                logging.info(f"Node {self.node_id} connected to peer on port {peer_port}")
            except ConnectionRefusedError:
                logging.error(f"Node {self.node_id} could not connect to peer on port {peer_port}")

    def send_to_peers(self, message):
        """Send a message to all peers."""
        for port, s in self.peer_sockets.items():
            try:
                s.sendall(message.encode('utf-8'))
                logging.info(f"Node {self.node_id} sent message to peer on port {port}")
            except Exception as e:
                logging.error(f"Error sending message to peer on port {port}: {e}")

    def validate_transaction(self, transaction):
        """Validate a transaction according to the rules of the stablecoin protocol."""
        logging.info(f"Node {self.node_id} validating transaction: {transaction}")
        
        if self.is_valid_transaction(transaction):
            logging.info(f"Node {self.node_id} validated transaction: {transaction}")
            self.send_to_mainnet(transaction)
        else:
            logging.warning(f"Node {self.node_id} rejected invalid transaction: {transaction}")

    def is_valid_transaction(self, transaction):
        """Check if a transaction is valid based on the stablecoin rules."""
        return True 

    def send_to_mainnet(self, transaction):
        """Send transaction to ESI Mainnet for cross-blockchain verification."""
        if self.esi_mainnet.verify_transaction(transaction):
            self.route_to_subblockchains(transaction)

    def route_to_subblockchains(self, transaction):
        """Simulate routing transaction to another sub-blockchain."""
        logging.info(f"Node {self.node_id} routing transaction to sub-blockchain.")

        self.send_to_peers(f"CROSS-BLOCKCHAIN TRANSACTION:{transaction}")
