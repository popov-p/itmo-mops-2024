from proto.messages_pb2 import Batch
import time
import aiormq
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://pavel:popov@mongo:27017/iotdata?authSource=admin"
client = AsyncIOMotorClient(MONGO_URI)
db = client.iotdata
data = db.data
instant = db.instant
ongoing = db.ongoing

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
            await instant.insert_one({
                "device_id": batch.device_id,
                "alpha": batch.alpha,
            })

        current_id_stack = ongoing[f"{batch.device_id}_stack"]
        await current_id_stack.insert_one(message_data)

        pipeline = [
            {"$match": {"device_id": batch.device_id}},
            {"$count": "total_count"}
        ]
        result = await current_id_stack.aggregate(pipeline).to_list(length=None)

        if result:
            total_count = result[0]['total_count']
            if total_count == 5:
                print(f"Сработало ongoing rule для ID: {batch.device_id}!")
                await ongoing.insert_one({
                    "device_id": batch.device_id,
                    "timestamp": str(time.time())
                })

                await db.drop_collection(current_id_stack)


            if await current_id_stack.count_documents({}) >= 10:
                await db.drop_collection(current_id_stack)

        # Acknowledge the message
        print(f"Сообщение добавлено в коллекцию data: {message_data}")
        await message.channel.basic_ack(message.delivery_tag)

    except Exception as e:
        print(f"Ошибка при обработке сообщения: {e}")
        await message.channel.basic_nack(message.delivery_tag)


async def main():
    connection = await aiormq.connect("amqp://pavel:popov@rabbitmq/")

    channel = await connection.channel()

    await channel.queue_declare('validated_queue', durable=True)
    await channel.basic_consume('validated_queue', on_message)

    try:
        await asyncio.Future()
    finally:
        await channel.close()
        await connection.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())