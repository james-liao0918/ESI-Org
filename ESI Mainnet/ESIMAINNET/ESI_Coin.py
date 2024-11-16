class ESICoin:
    def __init__(self):
        self.balances = {}
        self.exempt_accounts = set()
        self.total_supply = 0

    def mint(self, account, amount):
        """Mint new tokens for an account."""
        self.total_supply += amount
        if account in self.balances:
            self.balances[account] += amount
        else:
            self.balances[account] = amount

    def set_exempt_account(self, account):
        """Mark an account as exempt from fees."""
        self.exempt_accounts.add(account)

    def transfer(self, sender, receiver, amount, fee=0):
        """Transfer tokens between accounts with optional fee deduction."""
        if sender not in self.balances or self.balances[sender] < amount:
            raise Exception("Insufficient balance")
        
        if sender not in self.exempt_accounts:
            amount += fee  # Include fee if sender is not exempt

        if self.balances[sender] >= amount:
            self.balances[sender] -= amount
            self.balances[receiver] = self.balances.get(receiver, 0) + (amount - fee)
        else:
            raise Exception("Insufficient balance including fee")
