from aiocache import Cache

from app.settings import settings
from app.util import get_timestamp

tickets_cache = Cache.from_url(
    settings.CACHE_URL,
)


async def set_ticket(ticket: str, client: str):
    await tickets_cache.set(
        ticket,
        {'ts': get_timestamp(), 'client': client},
        ttl=settings.TICKETS_TTL,
    )


async def delete_ticket(ticket: str):
    await tickets_cache.delete(ticket)


async def ticket_exists(ticket: str) -> bool:
    return await tickets_cache.exists(ticket)


async def get_ticket(ticket: str):
    return await tickets_cache.get(ticket)
