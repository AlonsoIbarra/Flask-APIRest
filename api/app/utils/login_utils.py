import hmac
import hashlib
from os import getenv


def create_signature(data):
    """
    Function to encript user password.
    Params:
        data string Any string to encript.
    """
    m = hmac.new(
        bytes(getenv('SHARED_PRIVATE_KEY'), 'utf-8'),
        digestmod=hashlib.blake2s
    )
    m.update(bytes(data, 'utf-8'))
    return m.hexdigest()


def verify_signature(data, signature):
    """
    Function to validate if a signature corresponds to data given.
    Params:
        data      string A string to validate.
        signature string A encripted string.
    """
    return signature == create_signature(data)
