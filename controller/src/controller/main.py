from fastapi import FastAPI
from .routes import router
import logging
logging.basicConfig(
    filename='/var/log/controller.log',
    level=logging.INFO,
    format='%(name)s - %(levelname)s - %(message)s',
    filemode='a'
)
app = FastAPI()
app.include_router(router)
