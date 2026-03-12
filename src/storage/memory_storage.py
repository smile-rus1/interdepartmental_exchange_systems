from src.models.transaction import Transaction


class MemoryStorage:

    def __init__(self):
        self.transactions: list[Transaction] = []

    def add_transaction(self, tx: Transaction):
        self.transactions.append(tx)

    def get_transactions(self):
        return self.transactions


storage = MemoryStorage()
