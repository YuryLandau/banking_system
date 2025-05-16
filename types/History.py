
from datetime import datetime, timezone, timedelta

class History:
    def __init__(self):
        self._transactions = []

    @property
    def transactions(self):
        return self.transactions
    
    def add_transaction(self, transaction):
        self._transactions.append({
            "operation_index": len(self._transactions) + 1,
            "operation_date": datetime.now(timezone.utc),
            "operation_type": transaction.__class__.__name__,
            "value": transaction.value
        })