from datetime import datetime
from pydantic import BaseModel

from .transaction import Transaction


class SearchRequest(BaseModel):
    StartDate: datetime
    EndDate: datetime
    Limit: int
    Offset: int


class TransactionsData(BaseModel):
    Transactions: list[Transaction]
    Count: int
