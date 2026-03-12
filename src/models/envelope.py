from pydantic import BaseModel


class SignedApiData(BaseModel):
    Data: str
    Sign: str
    SignerCert: str
