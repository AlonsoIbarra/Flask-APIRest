import hmac
import hashlib
from os import getenv


def create_signature(data):
    m = hmac.new(
        bytes(getenv('SHARED_PRIVATE_KEY'), 'utf-8'),
        digestmod=hashlib.blake2s
    )
    m.update(bytes(data, 'utf-8'))
    return m.hexdigest()


def verify_signature(data, signature):
    return signature == create_signature(data)
