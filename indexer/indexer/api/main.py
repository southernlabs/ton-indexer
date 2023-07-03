import logging

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from indexer.api.api_v1.main import router as router_v1
from indexer.api.api_v2.main import router as router_v2

from indexer.core import exceptions
from indexer.core.settings import Settings


logging.basicConfig(format='%(asctime)s %(module)-15s %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


settings = Settings()
description = ''
app = FastAPI(title="TON Index",
              description=description,
              version='0.1.0',
              root_path=settings.api_root_path,
              docs_url='/')


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse({'error' : str(exc.detail)}, status_code=exc.status_code)


@app.exception_handler(exceptions.DataNotFound)
async def tonlib_wront_result_exception_handler(request, exc):
    return JSONResponse({'error' : str(exc)}, status_code=status.HTTP_404_NOT_FOUND)


@app.exception_handler(exceptions.MultipleDataFound)
async def tonlib_wront_result_exception_handler(request, exc):
    return JSONResponse({'error' : str(exc)}, status_code=status.HTTP_404_NOT_FOUND)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse({'error' : str(exc)}, status_code=status.HTTP_400_BAD_REQUEST)


@app.exception_handler(Exception)
def generic_exception_handler(request, exc):
    return JSONResponse({'error' : str(exc)}, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


@app.on_event("startup")
def startup():
    logger.info('Service started successfully')


app.include_router(router_v2, prefix='/v2', include_in_schema=True, deprecated=False, tags=['v2'])
app.include_router(router_v1, prefix='/v1', include_in_schema=True, deprecated=False, tags=['v1'])
