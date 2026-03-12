from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID


class Message(BaseModel):
    Data: str
    SenderBranch: str
    ReceiverBranch: str
    InfoMessageType: int
    MessageTime: datetime
    ChainGuid: UUID
    PreviousTransactionHash: Optional[str] = None
    Metadata: Optional[str] = None
