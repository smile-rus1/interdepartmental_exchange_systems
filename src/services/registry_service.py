from src.storage.sqlite_storage import storage
from src.services.crypto import compute_hash, emulate_sign


class RegistryService:
    @staticmethod
    def save_transactions(transactions):

        saved = []

        for tx in transactions:

            if not tx.Sign:
                raise ValueError("Transaction signature missing")

            expected_hash = compute_hash(tx.dict())

            if expected_hash != tx.Hash:
                raise ValueError("Invalid transaction hash")

            expected_sign = emulate_sign(tx.Hash)

            if tx.Sign != expected_sign:
                raise ValueError("Invalid signature")

            last_tx = storage.get_last_transaction()

            if last_tx:
                tx.TransactionIn = last_tx.Hash
                last_tx.TransactionOut = tx.Hash

            storage.add_transaction(tx)

            saved.append(tx)

        return saved

    @staticmethod
    def find_transactions(start_date, end_date):

        transactions = storage.get_transactions()
        result = []

        for tx in transactions:
            if start_date <= tx.TransactionTime <= end_date:
                result.append(tx)

        return result
