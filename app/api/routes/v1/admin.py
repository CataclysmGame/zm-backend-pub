from typing import Any

from fastapi import APIRouter
from loguru import logger
from sqlmodel import Session

from app.core.db import engine, ScoreRecord, BannedUser
from app.core.models.ban_request import BanRequest

router = APIRouter(prefix='/admin', tags=['admin'])


@router.post('/ban')
async def ban_user(ban_req: BanRequest) -> Any:
    with Session(engine) as session:
        if ban_req.permanent or ban_req.delete_scores:
            session.query(ScoreRecord).filter_by(user=ban_req.user).delete()
            logger.info('Deleted User "{}" scores', ban_req.user)

        session.add(BannedUser(
            user=ban_req.user,
            reason=ban_req.reason,
            duration=None if ban_req.permanent else ban_req.duration,
        ))

        session.commit()

    logger.info('User "{}" banned', ban_req.user)


@router.get('/bans')
async def get_bans(page: int, per_page: int) -> Any:
    with Session(engine) as session:
        bans = session.query(BannedUser).order_by(BannedUser.user.desc()).offset((page - 1) * per_page).limit(per_page).all()
        return bans
