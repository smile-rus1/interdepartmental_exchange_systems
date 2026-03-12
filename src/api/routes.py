import json
from fastapi import APIRouter, HTTPException

from src.models.envelope import SignedApiData
from src.models.search import SearchRequest, TransactionsData
from src.services.message_service import MessageService
from src.services.registry_service import RegistryService
from src.utils.base64_utils import decode_base64, encode_base64

router = APIRouter()


@router.get("/api/health")
def health():
    return "OK"


@router.post("/api/messages/outgoing")
def outgoing(envelope: SignedApiData):

    try:

        data = decode_base64(envelope.Data)

        req = SearchRequest.parse_raw(data)

        txs = RegistryService.find_transactions(
            req.StartDate,
            req.EndDate
        )

        paginated = txs[req.Offset:req.Offset + req.Limit]

        result = TransactionsData(
            Transactions=paginated,
            Count=len(txs)
        )

        result_bytes = json.dumps(
            result.dict(),
            default=str
        ).encode()

        response = SignedApiData(
            Data=encode_base64(result_bytes),
            Sign="",
            SignerCert=encode_base64(b"SYSTEM_B")
        )

        return response

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/api/messages/incoming")
def incoming(envelope: SignedApiData):

    try:

        data = decode_base64(envelope.Data)

        tx_data = TransactionsData.parse_raw(data)

        receipts = []

        for tx in tx_data.Transactions:

            RegistryService.save_transactions([tx])

            receipt = MessageService.create_receipt(tx)

            receipts.append(receipt)

        result = TransactionsData(
            Transactions=receipts,
            Count=len(receipts)
        )

        result_bytes = json.dumps(
            result.dict(),
            default=str
        ).encode()

        response = SignedApiData(
            Data=encode_base64(result_bytes),
            Sign="",
            SignerCert=encode_base64(b"SYSTEM_B")
        )

        return response

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("/debug/search")
def debug():
    """
    For generate Base64 (temporarily)
    """
    import base64, json

    data = {
        "StartDate": "2024-01-01T00:00:00Z",
        "EndDate": "2025-01-01T00:00:00Z",
        "Limit": 10,
        "Offset": 0
    }

    return base64.b64encode(json.dumps(data).encode()).decode()
