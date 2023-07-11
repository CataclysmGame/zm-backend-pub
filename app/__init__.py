import sentry_sdk
from fastapi import FastAPI
from loguru import logger
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette_context import middleware, plugins
from starlette_exporter import PrometheusMiddleware, handle_metrics

from app.api.routes import main_router
from app.exceptions import init_exception_handlers
from app.log import setup_logging
from app.settings import settings, log_settings


# def before_sentry_send(event, hint):
#     logger.info('Sending event to Sentry...')


class ClientPlugin(plugins.Plugin):
    key = 'client'

    async def process_request(self, request):
        client = request.client.host
        return client


def create_app() -> FastAPI:
    setup_logging()

    log_settings()

    description = '''
    '''

    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=description,
        terms_of_service='',
        contact={  # TODO: Insert correct information
            'name': 'NFT Factory SRL',
            'url': 'https://www.nft-factory.club/',
            'email': 'ciao@nft-factory.club',
        },
        license_info=None,
    )

    app.add_middleware(
        middleware.RawContextMiddleware,
        plugins=(
            plugins.ForwardedForPlugin(),
            plugins.RequestIdPlugin(),
            plugins.CorrelationIdPlugin(),
            ClientPlugin(),
        )
    )

    if settings.SENTRY_DSN is not None:
        logger.info('Initializing Sentry...')
        sentry_sdk.init(
            settings.SENTRY_DSN,
            debug=settings.DEBUG,
            sample_rate=settings.SENTRY_SAMPLE_RATE,
            max_breadcrumbs=settings.SENTRY_MAX_BREADCRUMBS,
            # before_send=before_sentry_send,
        )
        app.add_middleware(SentryAsgiMiddleware)

    if settings.PROMETHEUS_ENABLED:
        app.add_middleware(
            PrometheusMiddleware,
            app_name=settings.PROJECT_NAME,
            group_paths=True,
            buckets=[0.1, 0.25, 0.50],
        )
        app.add_route(settings.PROMETHEUS_METRICS_ENDPOINT, handle_metrics)

    if settings.CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ORIGINS,
            allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
            allow_methods=settings.CORS_ALLOW_METHODS,
            allow_headers=settings.CORS_ALLOW_HEADERS,
        )

    app.include_router(main_router)

    init_exception_handlers(app)

    @app.on_event('startup')
    async def on_app_startup():
        from app.core.db import create_db_and_tables
        create_db_and_tables()
        logger.info(startup_banner)
        logger.info('App started')

    @app.on_event('shutdown')
    async def on_app_shutdown():
        logger.info('App shut down')

    return app


app = create_app()

startup_banner = '''
      ............................................................................................................................     
   ^??7!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!7J7.  
  YY.                                                                                                                              ^P! 
 7P                                                                         :^JP^                                                   :B:
 J5                                                                        ~?:PB?                                                   .G^
 ?5                                                               .^!55    7!.5BY                                                   .G^
 ?5                                                         ..    Y^~BG:   ?^.5BP.                                                  .G^
 ?5                                                      :!!P5   .J.~GB~   J:.5BG:                                                  .G^
 ?5                                                 .:   J^:GG.  ~?.~GB?  .J:.5BB~                                                  .G^
 ?5                                              ^!7BP  .J::GB:  7!.~GB5  :J..5BB?                                                  .G^
 ?5                                              Y^~GG. .J.:GB~  J^.~BBG: ^7..5BBY                                                  .G^
 ?5                                              Y.~BB^ ^J:~GBJ:^Y!~7J?5P?5J^^5BBP.                                                 .G^
 ?5                                            .^Y~7557~!!~~~^^::......?BBBBBGGBBG~.                                                .G^
 ?5                                          .J~^::............^~!~:...?BBBBBBBBBBBGPY?!:                                           .G^
 ?5                                          .J..:~77~.:J5PP7.JBBBB?...?BBBBBBBBBBBBBBBBG.                                          .G^
 ?5                                          .J..YBPPG^!BY7Y5:5G~^YJ...?BBBBBBBBBBBBBBBBP.                                          .G^
 ?5                                          .J..5J  Y~!P  :5:5Y  !Y...?BBBBBBBBBBBBBBBBP.                                          .G^
 ?5                                          .J..YY.:5^~P!:??.?P!!Y!...?BBBBBBBBBBBBBBBBP.                                          .G^
 ?5                                          .J..:!!!^.:^!~~:.:^~^:....?BBBBBBBBBBBBBBBBP.                                          .G^
 ?5                                          .J.:?!^^~?^^^?!^:!?:::??:.?BBBBBBBBBBBBBBBBP.                                          .G^
 ?5                                          :Y~75:  .?   7:  :7   7!!~JBBBBBBBBBBBBBBBBG.                                          .G^
 ?5                                          .JJ^7~::~?:::?~::~?:::?~:75PPPPPPPPPPPPPPPPY.                                          .G^
 ?5                                                                                                                                 .G^
 ?5                                                                                                                                 .G^
 ?5        :P5  P7    .5PYYY7     ?5PP5J.          :55YYY!    .5PYYPJ    .YP5YY?.    755P5Y.    !P5Y5P^    ~P5Y5P~    :P7 :57       .G^
 ?5        ^GB5 BJ    .GP^..       .5G:            ^BY:.      .GP^~B5    .PP:         .5G^      ?B!.JB~    !BJ:?B7    ^BY.~BJ       .G^
 ?5        ^GPPBBJ    .PGY7         5P.            ^GGY!      .GGY5B5    .PP.          YG:      ?B^ 7B~    !BGGPJ.    :YPGP57       .G^
 J5        ^BJ GBJ    .G5.          5G.            ^BJ        :G5.:G5    .PG~.:.       YG:      ?B7:YB~    !B55G~       ^BY         .G^
 ?P        .J~ ^J~    .?!           7?.            .J~        .?! .?7     7JJJJ7       !J.      ~JJJJJ:    ^J^ 7J^      .J~         .B:
 :G~                                                                                                                                J5 
  .JJ~:..........................................................................................................................:!Y7  
    .^!!777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777!~: 
'''
