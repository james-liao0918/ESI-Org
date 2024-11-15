import time
import random
import logging

logging.basicConfig(level=logging.INFO)

class ESI_Mainnet:
    def __init__(self):
        self.verified_transactions = []
        self.pending_transactions = []
        self.transaction_status = {}
        self.transaction_fees = []
        self.base_fee = []
        self.gas_fees = [] 

    def verify_transaction(self, transaction):
        """Verifies and logs the transaction status after calculation of fees."""
        time.sleep(1)
        fee = self.calculate_transaction_fee(transaction)
        self.transaction_fees.append(fee)

        gas = self.calculate_gas_fee()  
        self.gas_fees.append(gas) 

        if self.is_valid_transaction(transaction):
            self.verified_transactions.append(transaction)
            self.transaction_status[transaction] = "Verified"
            self.log_transaction(transaction, "Verified")
            return True
        else:
            self.transaction_status[transaction] = "Failed"
            self.log_transaction(transaction, "Failed")
            return False

    def is_valid_transaction(self, transaction):
        """Validates transaction based on simple checks."""
        if len(transaction) < 10:
            return False
        if "invalid" in transaction.lower():
            return False
        return True
    
    def transaction_fee(self):
        """Provides a base fee value."""
        base_fee = 0.0000000012
        self.base_fee.append(base_fee)
        return base_fee

    def calculate_transaction_fee(self, transaction):
        """Calculates transaction fees based on type and amount with a base and security fee for added security."""
        base_fee = 0.0000000012
        try:
            if "sends" in transaction or "receives" in transaction:
                if any(coin in transaction for coin in ["EIC", "EIP", "EID", "EIO", "EIE", "EIO", "EIB", "EIBE"]):
                    amount = float(transaction.split()[transaction.split().index("sends" if "sends" in transaction else "receives") + 1])
                    security_fee = 0.5 * amount
                    return base_fee + security_fee

            elif "withdraws" in transaction or "deposits" in transaction:
                if any(currency in transaction for currency in ["PHP", "USD"]):
                    amount = float(transaction.split()[transaction.split().index("withdraws" if "withdraws" in transaction else "deposits") + 1].replace(",", ""))
                    security_fee = 0.25 * amount
                    return base_fee + security_fee
            
        except (ValueError, IndexError):
            logging.error(f"Failed to extract amount from transaction: {transaction}")
        
        return base_fee
    
    def calculate_gas_fee(self):
        """Calculates the gas fee based on network load."""
        base_gas_fee = self.get_base_gas_fee()
        load_factor = random.choice([1, 2, 3])  
        adjusted_gas_fee = base_gas_fee * load_factor
        return adjusted_gas_fee

    def get_base_gas_fee(self):
        """Returns the base gas fee. This can be adjusted for future scalability."""
        return 0.00001
    
    def log_transaction(self, transaction, status):
        logging.info(f"Transaction: {transaction}, Status: {status}")

    def prioritize_transactions(self):
        self.pending_transactions.sort(key=lambda x: len(x), reverse=True)

    def add_to_pending(self, transaction):
        """Adds a transaction to the pending list."""
        self.pending_transactions.append(transaction)
        self.transaction_status[transaction] = "Pending"

    def resolve_conflict(self, conflicting_transactions):
        """Resolves conflicting transactions based on size."""
        winner = max(conflicting_transactions, key=lambda x: len(x))
        return winner

    def adjust_transaction_fees(self):
        """Adjusts the transaction fees based on network load."""
        load_factor = random.choice([0.5, 1, 1.5])
        base_fee = 0.0000000012 * load_factor
        return base_fee
