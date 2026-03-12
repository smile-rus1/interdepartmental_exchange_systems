import hashlib
import json


def guarantee_hash(guarantee: dict) -> str:
    """
    Generate hash for doc
    """

    temp = dict(guarantee)

    if "BankGuaranteeHash" in temp:
        temp["BankGuaranteeHash"] = ""

    json_str = json.dumps(
        temp,
        ensure_ascii=False,
        separators=(",", ":")
    )

    return hashlib.sha256(
        json_str.encode()
    ).hexdigest().upper()
