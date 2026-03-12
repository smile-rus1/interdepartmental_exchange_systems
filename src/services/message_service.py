import json
import uuid
from datetime import datetime

from src.models.message import Message
from src.models.transaction import Transaction
from src.services.crypto import compute_hash, emulate_sign
from src.utils.base64_utils import decode_base64, encode_base64


class MessageService:

    @staticmethod
    def create_receipt(original_tx: Transaction):

        msg_bytes = decode_base64(original_tx.Data)
        msg = json.loads(msg_bytes)

        chain_guid = msg["ChainGuid"]

        receipt_data = {
            "BankGuaranteeHash": msg.get("BankGuaranteeHash")
        }

        receipt_data_bytes = json.dumps(receipt_data).encode()
        receipt_data_b64 = encode_base64(receipt_data_bytes)

        receipt_message = Message(
            Data=receipt_data_b64,
            SenderBranch="SYSTEM_B",
            ReceiverBranch="SYSTEM_A",
            InfoMessageType=215,
            MessageTime=datetime.utcnow(),
            ChainGuid=chain_guid,
            PreviousTransactionHash=original_tx.Hash
        )

        message_bytes = json.dumps(receipt_message.dict()).encode()

        tx = Transaction(
            TransactionType=9,
            Data=encode_base64(message_bytes),
            Hash="",
            Sign="",
            SignerCert=encode_base64(b"SYSTEM_B"),
            TransactionTime=datetime.utcnow()
        )

        tx.Hash = compute_hash(tx.dict())
        tx.Sign = emulate_sign(tx.Hash)

        return tx
