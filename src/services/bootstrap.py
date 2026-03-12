import json
import uuid
from datetime import datetime, timezone

from src.models.message import Message
from src.models.transaction import Transaction

from src.services.crypto import compute_hash, emulate_sign
from src.storage.sqlite_storage import storage

from src.utils.base64_utils import encode_base64
from src.utils.hash_utils import guarantee_hash


def create_test_transaction():
    """
    Generate on startup app test data
    """

    guarantee_data = {
        "InformationType": 201,
        "InformationTypeString": "Выдача гарантии",
        "Number": "BG-2024-001",
        "IssuedDate": "2024-05-20T10:00:00Z",
        "Guarantor": "ООО 'Финансовая гарантия'",
        "Beneficiary": "Государственное учреждение 'Получатель'",
        "Principal": "ООО 'Должник'",
        "Obligations": [
            {
                "Type": 1,
                "StartDate": "2024-06-01T00:00:00Z",
                "EndDate": "2024-12-01T00:00:00Z",
                "ActDate": "2024-05-15T00:00:00Z",
                "ActNumber": "ПР-2024/05/15-001",
                "Taxs": [
                    {
                        "Number": "1",
                        "NameTax": "Обязательство по контракту №К-2024-01",
                        "Amount": 50000.00,
                        "PennyAmount": 0.00
                    },
                    {
                        "Number": "2",
                        "NameTax": "Гарантийное обеспечение",
                        "Amount": 15000.00,
                        "PennyAmount": 500.00
                    }
                ]
            }
        ],
        "StartDate": "2024-06-01T00:00:00Z",
        "EndDate": "2024-12-15T00:00:00Z",
        "CurrencyCode": "USD",
        "CurrencyName": "Доллар США",
        "Amount": 65000.00,
        "RevokationInfo": "Безотзывная",
        "ClaimRightTransfer": "Не допускается",
        "PaymentPeriod": "5 рабочих дней с момента получения требования",
        "SignerName": "Иванов Иван Иванович",
        "AuthorizedPosition": "Генеральный директор"
    }
    guarantee_data["BankGuaranteeHash"] = guarantee_hash(guarantee_data)

    guarantee_bytes = json.dumps(guarantee_data).encode()
    guarantee_b64 = encode_base64(guarantee_bytes)

    message = Message(
        Data=guarantee_b64,
        SenderBranch="SYSTEM_B",
        ReceiverBranch="SYSTEM_A",
        InfoMessageType=201,
        MessageTime=datetime.now(timezone.utc),
        ChainGuid=uuid.uuid4()
    )

    message_bytes = json.dumps(message.dict(), default=str).encode()

    tx = Transaction(
        TransactionType=201,
        Data=encode_base64(message_bytes),
        Hash="",
        Sign="",
        SignerCert=encode_base64(b"SYSTEM_B"),
        TransactionTime=datetime.now(timezone.utc)
    )

    tx.Hash = compute_hash(tx.dict())
    tx.Sign = emulate_sign(tx.Hash)

    storage.add_transaction(tx)
