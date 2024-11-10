from .rabbitmq import create_connection
from fastapi import FastAPI
from .routes import router

connection = create_connection() #rabbitmq
app = FastAPI()
app.include_router(router)
