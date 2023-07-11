import math
import time
import uuid

from starlette_context import context


def gen_new_uuid() -> uuid.UUID:
    """
    Generates a new UUID using the selected algorithm.
    """
    return uuid.uuid4()


def get_timestamp() -> int:
    """
    Returns the current timestamp in seconds.
    """
    return math.floor(time.time())


def get_client() -> str:
    """
    Returns the client IP address.
    """
    forwarded_for = context.data["X-Forwarded-For"]
    return forwarded_for or context.get('client')
