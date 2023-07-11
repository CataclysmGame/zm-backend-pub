import datetime
from typing import Any, Optional

import sentry_sdk
from fastapi import APIRouter, HTTPException
from loguru import logger
from sqlmodel import Session

from app.core.anticheat import AntiCheat
from app.core.cache import delete_ticket
from app.core.db import engine, ScoreRecord, BannedUser
from app.core.models.score_submission import ScoreSubmission
from app.settings import settings
from app.util import get_timestamp

router = APIRouter(tags=['score'])

anti_cheat = AntiCheat()


@router.get('/highscore/')
async def get_highscore(user: Optional[str] = None, character: Optional[int] = None) -> Any:
    with Session(engine) as session:
        query = session.query(ScoreRecord.user, ScoreRecord.score, ScoreRecord.character)

        if user is not None:
            if character is not None:
                query = query.filter(ScoreRecord.user == user, ScoreRecord.character == character)
            else:
                query = query.filter(ScoreRecord.user == user)
        elif character is not None:
            query = query.filter(ScoreRecord.character == character)

        score = query.order_by(ScoreRecord.score.desc()).first()

        return score


@router.get('/leaderboard/')
async def get_leaderboard(entries: int = 10, character: Optional[int] = None, start_date: Optional[int] = None,
                          end_date: Optional[int] = None) -> Any:
    with Session(engine) as session:

        scores = session.query(
            ScoreRecord.user,
            ScoreRecord.score,
            ScoreRecord.timestamp,
            ScoreRecord.character,
            ScoreRecord.character_skin,
        )

        if character is not None:
            scores = scores.filter(ScoreRecord.character == character)

        if start_date is not None:
            scores = scores.filter(ScoreRecord.timestamp >= start_date)

        if end_date is not None:
            scores = scores.filter(ScoreRecord.timestamp <= end_date)

        return scores.order_by(ScoreRecord.score.desc()).limit(entries).all()


@router.post('/score')
async def submit_score(submission: ScoreSubmission) -> Any:
    logger.debug('Submitting score: {}', submission)

    try:
        # Check if the user is banned
        with Session(engine) as session:
            banned = session.query(BannedUser).filter(BannedUser.user == submission.user).first()
            if banned:
                logger.info('User "{}" is banned', submission.user)
                raise HTTPException(status_code=403, detail='User is banned')

        game_duration = await anti_cheat.validate_submission(submission)
    except Exception as ex:
        sentry_sdk.capture_exception(ex)
        raise ex
    finally:
        # remove used ticket
        await delete_ticket(submission.ticket)
        logger.debug('Ticket deleted: {}', submission.ticket)

    character_skin = submission.character_skin
    if character_skin == 'base':
        character_skin = None

    record = ScoreRecord(
        user=submission.user,
        score=submission.score,
        character=submission.character_id,
        character_skin=character_skin,
        game_duration=game_duration,
        game_version=submission.game_version,
    )

    with Session(engine) as session:
        session.add(record)

        # Remove old records
        today = datetime.datetime.fromtimestamp(
            get_timestamp(),
            tz=datetime.timezone.utc
        )

        tomorrow = today + datetime.timedelta(days=1)

        start_datetime = datetime.datetime.combine(today, datetime.time(hour=14))
        end_datetime = datetime.datetime.combine(tomorrow, datetime.time(hour=14))

        start_date_timestamp = int(start_datetime.timestamp())
        end_date_timestamp = int(end_datetime.timestamp())

        records_count = session.query(ScoreRecord).filter(ScoreRecord.user == submission.user,
                                                          ScoreRecord.character == submission.character_id,
                                                          ScoreRecord.timestamp >= start_date_timestamp,
                                                          ScoreRecord.timestamp <= end_date_timestamp).count()

        logger.debug(
            'User {} with character {} records count today: {}',
            submission.user,
            submission.character_id,
            records_count
        )

        if records_count > settings.MAX_SCORES_PER_CHARACTER:
            rows_to_remove = records_count - settings.MAX_SCORES_PER_CHARACTER

            # Remove the lowest scores of the NFT
            sq = session.query(ScoreRecord.id) \
                .filter(ScoreRecord.user == submission.user,
                        ScoreRecord.character == submission.character_id,
                        ScoreRecord.timestamp >= start_date_timestamp,
                        ScoreRecord.timestamp <= end_date_timestamp) \
                .order_by(ScoreRecord.score.asc()) \
                .limit(rows_to_remove) \
                .subquery()

            session.query(ScoreRecord) \
                .filter(ScoreRecord.id.in_(sq)) \
                .delete(synchronize_session=False)

            logger.info('Deleted {} records of user {} with character {}', rows_to_remove, submission.user,
                        submission.character_id)

        session.commit()
