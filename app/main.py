import os

from fastapi import FastAPI
from starlette.requests import Request

# load env
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from core import config
app = FastAPI(title=config.PROJECT_NAME, openapi_url="/api/v1/openapi.json")

# init log
from utils.logger import initLoggerBySize
if not os.path.exists(config.LOGFILE_PATH):
    try:
        os.makedirs(config.LOGFILE_PATH)
    except FileExistsError as e:
        print('file exist')

initLoggerBySize(
    config.PROJECT_NAME, 
    os.path.join(config.LOGFILE_PATH, config.PROJECT_NAME), 
    config.LOG_LEVEL
)

# CORS
origins = []

# Set all CORS enabled origins
if config.BACKEND_CORS_ORIGINS:
    origins_raw = config.BACKEND_CORS_ORIGINS.split(",")
    for origin in origins_raw:
        use_origin = origin.strip()
        origins.append(use_origin)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),


# rewrite HTTP Error
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import PlainTextResponse

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


# add routers
from routers.sample import sample_router

router_list = [
    (sample_router, ''),
]
for router in router_list:
    app.include_router(router[0], prefix=router[1])

# app.include_router(api_router, prefix=config.API_V1_STR)

