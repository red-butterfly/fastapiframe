from fastapi import APIRouter

from routers.sample.endpoints import test_api

sample_router = APIRouter()
sample_router.include_router(test_api.router, prefix="/test", tags=["sample"])