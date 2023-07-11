from typing import Any

from fastapi import APIRouter, Request, HTTPException
from loguru import logger

from app.core.cache import set_ticket, get_ticket
from app.core.ticket import generate_ticket
from app.util import get_client

router = APIRouter(tags=['ticket'])


@router.get('/ticket')
async def get_new_ticket(request: Request) -> Any:
    logger.debug('Headers: {}', request.headers)

    ticket = generate_ticket()
    await set_ticket(ticket, get_client())
    logger.debug('Ticket generated: {}', ticket)
    return ticket


@router.get('/ticket/{ticket}')
async def get_game(ticket: str) -> Any:
    game = await get_ticket(ticket)
    if game is None:
        raise HTTPException(status_code=404, detail='Ticket not found')
    return game
