
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, TypedDict

class TransactionDict(TypedDict):
    operation_index: int
    operation_date: datetime
    operation_type: str
    value: float

class History:
    def __init__(self):
        self._transactions: List[TransactionDict] = []

    @property
    def transactions(self) -> List[TransactionDict]:
        return self._transactions
    
    def add_transaction(self, transaction):
        self._transactions.append({
            "operation_index": len(self._transactions) + 1,
            "operation_date": datetime.now(timezone.utc),
            "operation_type": transaction.__class__.__name__,
            "value": transaction.value
        })