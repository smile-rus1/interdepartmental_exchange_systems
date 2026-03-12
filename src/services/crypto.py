import hashlib
import base64
import json


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def compute_hash(obj: dict) -> str:
    temp = dict(obj)

    temp["Hash"] = None
    temp["Sign"] = ""

    json_str = json.dumps(
        temp,
        separators=(",", ":"),
        ensure_ascii=False,
        default=str
    )

    return sha256_hex(json_str.encode())


def emulate_sign(hash_hex: str) -> str:
    hash_bytes = bytes.fromhex(hash_hex)
    return base64.b64encode(hash_bytes).decode()