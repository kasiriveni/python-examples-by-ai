"""
OOP basics - classes, objects, methods.
"""

class BankAccount:
    """A simple bank account class."""

    # Class variable
    interest_rate = 0.02

    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance  # convention: protected
        self._transactions = []

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount
        self._transactions.append(f"+{amount}")
        return self

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
        self._transactions.append(f"-{amount}")
        return self

    def apply_interest(self):
        interest = self._balance * self.interest_rate
        self.deposit(interest)
        return self

    @classmethod
    def from_string(cls, account_string):
        owner, balance = account_string.split(":")
        return cls(owner, float(balance))

    @staticmethod
    def validate_amount(amount):
        return isinstance(amount, (int, float)) and amount > 0

    def __str__(self):
        return f"Account({self.owner}, ${self._balance:.2f})"

    def __repr__(self):
        return f"BankAccount('{self.owner}', {self._balance})"

    def __len__(self):
        return len(self._transactions)


if __name__ == "__main__":
    # Create account
    acc = BankAccount("Alice", 1000)
    print(acc)

    # Method chaining
    acc.deposit(500).withdraw(200).apply_interest()
    print(f"After operations: {acc}")
    print(f"Transactions: {len(acc)}")

    # Class method
    acc2 = BankAccount.from_string("Bob:5000")
    print(f"From string: {acc2}")

    # Static method
    print(f"Valid amount (100): {BankAccount.validate_amount(100)}")
    print(f"Valid amount (-5): {BankAccount.validate_amount(-5)}")

    # Class variable
    print(f"Interest rate: {BankAccount.interest_rate}")
    BankAccount.interest_rate = 0.03
    print(f"New rate: {acc.interest_rate}")
