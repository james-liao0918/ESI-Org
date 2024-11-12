import rsa
import time
import json
import logging
import socket
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
import ssl

# Constants
TRANSACTION_EXPIRY_TIME = 300  # 5 minutes expiry time for transactions
NODE_PORT = 12345  # Port specific to this node
NODE_NAME = "EsiNode1"  # Node specific name

# Global Variables
transaction_pool = {}
transaction_timestamps = {}

# Set up logging
logging.basicConfig(level=logging.INFO)

# Step 1: Node Initialization (Generate Keys)
def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_pem, public_pem

# Step 2: Transaction Signing
def sign_transaction(transaction, private_key):
    private_key_obj = serialization.load_pem_private_key(private_key, password=None)
    transaction_hash = hashes.Hash(hashes.SHA256())
    transaction_hash.update(str(transaction).encode('utf-8'))
    transaction_digest = transaction_hash.finalize()
    signature = private_key_obj.sign(
        transaction_digest,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return signature

# Step 3: Transaction Verification
def verify_transaction(transaction, signature, public_key):
    public_key_obj = serialization.load_pem_public_key(public_key)
    transaction_hash = hashes.Hash(hashes.SHA256())
    transaction_hash.update(str(transaction).encode('utf-8'))
    transaction_digest = transaction_hash.finalize()
    try:
        public_key_obj.verify(
            signature,
            transaction_digest,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        logging.error(f"Transaction verification failed: {e}")
        return False

# Step 4: Adding Transactions to the Pool
def add_transaction(transaction, sender_public_key):
    is_valid, message = validate_transaction(transaction)
    if is_valid:
        signature = transaction["signature"]
        if verify_transaction(transaction, signature, sender_public_key):
            transaction_pool[transaction["id"]] = transaction
            transaction_timestamps[transaction["id"]] = time.time()
            logging.info(f"Transaction added: {transaction}")
            broadcast_transaction(transaction)
        else:
            logging.warning("Transaction signature is invalid. Transaction not added to the pool.")
    else:
        logging.warning(f"Invalid transaction: {message}")

# Step 5: Broadcasting Transactions to Other Nodes
def broadcast_transaction(transaction):
    global transaction_pool
    for node_name, port in [("EsiNode1", 12345), ("EsiNode2", 12346), ("EsiNode3", 12347)]:
        if node_name != NODE_NAME:  # Skip broadcasting to itself
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect(('localhost', port))
                    context = create_ssl_context()
                    sock = context.wrap_socket(sock, server_side=False)
                    transaction_message = json.dumps(transaction)
                    sock.sendall(f"New Transaction: {transaction_message}".encode())
                    response = sock.recv(1024)
                    logging.info(f"Transaction broadcast to {node_name}, response: {response.decode()}")
            except Exception as e:
                logging.error(f"Failed to broadcast transaction to {node_name}: {e}")

# SSL context for secure communication
def create_ssl_context():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="node_cert.pem", keyfile="node_key.pem")
    return context

# Step 6: Cleaning Up Expired Transactions
def cleanup_expired_transactions():
    current_time = time.time()
    for txn_id, timestamp in list(transaction_timestamps.items()):
        if current_time - timestamp > TRANSACTION_EXPIRY_TIME:
            del transaction_pool[txn_id]
            del transaction_timestamps[txn_id]
            logging.info(f"Expired transaction {txn_id} removed.")

# Step 7: Validate Transaction Data
def validate_transaction(transaction):
    if transaction["amount"] <= 0:
        return False, "Amount must be greater than zero."
    if "id" not in transaction or not transaction["id"]:
        return False, "Transaction ID is missing or invalid."
    return True, ""

# Step 8: Monitoring Other Nodes
def monitor_nodes(nodes):
    for node_name, port in nodes:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(('localhost', port))
                context = create_ssl_context()
                sock = context.wrap_socket(sock, server_side=False)
                sock.sendall(b"Requesting transaction pool status")
                response = sock.recv(1024)
                logging.info(f"Response from {node_name}: {response.decode()}")
        except Exception as e:
            logging.error(f"Failed to monitor {node_name}: {e}")

# Main Execution Logic for the Node
if __name__ == "__main__":
    private_key, public_key = generate_keys()

    # Sample Transaction
    transaction = {
        "id": "txn_1234",
        "sender": "EsiNode1",
        "receiver": "EsiNode2",
        "amount": 100,
        "signature": sign_transaction(transaction, private_key)
    }

    # Add Transaction to Pool
    add_transaction(transaction, public_key)

    # Main Node Loop
    while True:
        monitor_nodes([("EsiNode1", 12345), ("EsiNode2", 12346), ("EsiNode3", 12347)])
        cleanup_expired_transactions()
        time.sleep(30)
