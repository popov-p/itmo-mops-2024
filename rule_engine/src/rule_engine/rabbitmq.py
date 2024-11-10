from proto.messages_pb2 import Batch
import time
import aiormq, asyncio
from .database import instant, ongoing, db
from .prometheus import  INSTANT_RULES_COUNTER, ONGOING_RULES_COUNTER

async def connect_to_rabbitmq():
    while True:
        try:
            connection = await aiormq.connect("amqp://pavel:popov@rabbitmq/")
            channel = await connection.channel(publisher_confirms=False)
            await channel.basic_consume('validated_queue', on_message)
            print("Подключён к брокеру.")
            return connection, channel
        except aiormq.AMQPConnectionError as e:
            print(f"Ошибка при подключении: {e}. Попробуем снова через 1 секунду.")
            await asyncio.sleep(2)


async def on_message(message: aiormq.abc.DeliveredMessage):
    try:
        batch = Batch()
        batch.ParseFromString(message.body)

        message_data = {
            "device_id": batch.device_id,
            "alpha": batch.alpha,
            "beta": batch.beta,
            "timestamp": batch.timestamp
        }

        if batch.alpha <= 50:
            print(f"Сработало instant rule для ID: {batch.device_id}, alpha: {batch.alpha}")
            INSTANT_RULES_COUNTER.inc()
            await instant.insert_one({
                "device_id": batch.device_id,
                "alpha": batch.alpha,
            })

        current_id_stack = ongoing[f"{batch.device_id}_stack"]
        await current_id_stack.insert_one(message_data)

        pipeline = [
            {"$match": {"device_id": batch.device_id, "beta": {"$gte": 75}}},
            {"$count": "total_count"}
        ]
        result = await current_id_stack.aggregate(pipeline).to_list(length=None)

        if result:
            total_count = result[0]['total_count']
            if total_count >= 5:
                ONGOING_RULES_COUNTER.inc()
                print(f"Сработало ongoing rule для ID: {batch.device_id}!")
                await ongoing.insert_one({
                    "device_id": batch.device_id,
                    "timestamp": str(time.time())
                })

                await db.drop_collection(current_id_stack)


            if await current_id_stack.count_documents({}) >= 10:
                await db.drop_collection(current_id_stack)

        print(f"Сообщение добавлено в коллекцию data: {message_data}.")
        await message.channel.basic_ack(message.delivery_tag)

    except Exception as e:
        print(f"Ошибка при обработке сообщения: {e}.")
        await message.channel.basic_nack(message.delivery_tag)
