from typing import Any

import orjson
from fastapi import APIRouter
from healthcheck import HealthCheck, EnvironmentDump
from sqlmodel import Session, select
from starlette.responses import JSONResponse

from app.settings import settings

router = APIRouter(tags=['health'])
health = HealthCheck()


def _test_db():
    try:
        from app.core.db import engine
        with Session(engine) as session:
            return session.exec(select(1)).one() == 1, None
    except Exception as e:
        return False, str(e)


health.add_check(_test_db)


@router.get('/health')
async def check_health() -> Any:
    """
    Performs application health checks
    """
    content, status_code, headers = health.run()

    return JSONResponse(
        content=orjson.loads(content),
        status_code=status_code,
        headers=headers,
    )


if settings.ENVDUMP_ENABLED:
    env_dump = EnvironmentDump()


    @router.get('/envdump')
    async def environment_dump() -> Any:
        """
        Performs a dump of environment variables
        """
        content, status_code, headers = env_dump.run()

        return JSONResponse(
            content=orjson.loads(content),
            status_code=status_code,
            headers=headers,
        )
