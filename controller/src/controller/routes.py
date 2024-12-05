from ..proto.messages_pb2 import Batch
from .rabbitmq import device_channels, create_channel_for_device, rabbitmq_connection
from fastapi import Request, Response, HTTPException, APIRouter
from .database import db
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from .prometheus import REQUESTS, BATCHES_ACCEPTED, BATCHES_DECLINED
router = APIRouter()

@router.get("/metrics")
def metrics():
    REQUESTS.inc()
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@router.post("/incoming-data")
async def incoming_data(request: Request):
    try:
        REQUESTS.inc()
        body = await request.body()
        batch = Batch()
        batch.ParseFromString(body)
        if batch.alpha < 25:
            BATCHES_DECLINED.inc()
            raise HTTPException(501,"Не принято! Ожидается alpha >= 25")

        if batch.device_id not in device_channels:
            BATCHES_ACCEPTED.inc()
            print("Канала нет, создаем новый.")
            rabbitmq_channel = create_channel_for_device(rabbitmq_connection, batch.device_id)
        else:
            BATCHES_ACCEPTED.inc()
            print("Используем существующий канал.")
            rabbitmq_channel = device_channels[batch.device_id]
        rabbitmq_channel.basic_publish(
            exchange='',
            routing_key='validated_queue',
            body=body
        )

        data = {
            "device_id": batch.device_id,
            "alpha": batch.alpha,
            "beta": batch.beta,
            "timestamp": batch.timestamp
        }

        result = await db.data.insert_one(data)

        return Response(f"Принято. ID отправителя: {batch.device_id}, ID объекта в коллекции: {result.inserted_id}")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500,f"Ошибка: {str(e)}")
