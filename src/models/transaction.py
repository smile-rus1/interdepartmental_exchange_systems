from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Transaction(BaseModel):
    TransactionType: int
    Data: str
    Hash: str
    Sign: str
    SignerCert: str
    TransactionTime: datetime
    Metadata: Optional[str] = None
    TransactionIn: Optional[str] = None
    TransactionOut: Optional[str] = None
