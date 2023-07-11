from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.exceptions.anti_cheat_exception import AntiCheatException


def init_exception_handlers(app: FastAPI):
    app.add_exception_handler(AntiCheatException, anti_cheat_exception_handler)


def anti_cheat_exception_handler(req: Request, exc: AntiCheatException):
    return JSONResponse(
        content=str(exc),
        status_code=status.HTTP_400_BAD_REQUEST,
    )
