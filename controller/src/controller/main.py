from fastapi import FastAPI
from .routes import router
import logging
from .report import metrics_reporter

logging.basicConfig(
    filename='/var/log/controller.log',
    level=logging.INFO,
    format='%(name)s - %(levelname)s - %(message)s',
    filemode='a'
)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    print("Запуск фоновой корутины для формирования отчёта.")
    metrics_reporter.connect_to_redis()
    await metrics_reporter.start_background_tasks()

app.include_router(router)
