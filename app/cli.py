import typer
import uvicorn

from app.settings import settings

cli = typer.Typer(name='ZMServer CLI')

APP_MODULE_STR: str = 'app:app'


@cli.command()
def run(
        port: int = settings.API_PORT,
        host: str = settings.API_HOST,
        log_level: str = settings.LOG_LEVEL,
        reload: bool = settings.API_RELOAD,
        proxy_headers: bool = False,
):
    uvicorn.run(
        APP_MODULE_STR,
        host=host,
        port=port,
        log_level=log_level,
        reload=reload,
        proxy_headers=proxy_headers,
    )
