import os

from dotenv import load_dotenv

from dataclasses import dataclass


@dataclass
class WebConfig:
    host: str
    port: int


@dataclass
class Config:
    web: WebConfig


def config_loader():
    load_dotenv()

    return Config(
        web=WebConfig(
            host=os.getenv("HOST"),
            port=int(os.getenv("PORT"))
        )
    )


config = config_loader()
