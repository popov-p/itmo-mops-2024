from .rabbitmq import connect_to_rabbitmq
from proto.messages_pb2 import Batch
from pymongo import MongoClient
import time
channel = connect_to_rabbitmq()

mongo_client = MongoClient("mongodb://pavel:popov@mongo:27017/iotdata?authSource=admin")
db = mongo_client.iotdata
data = db.data
instant = db.instant
ongoing = db.ongoing

def callback(ch, method, properties, body):
    try:
        batch = Batch()
        batch.ParseFromString(body)
        message = {
            "device_id": batch.device_id,
            "alpha": batch.alpha,
            "beta": batch.beta,
            "timestamp": batch.timestamp
        }
        if batch.alpha <= 50:
            print(f"Сработало instant rule для ID: {batch.device_id}, alpha: {batch.alpha}")
            instant.insert_one({
                "device_id": batch.device_id,
                "alpha": batch.alpha,
            })
        current_id_stack = ongoing[f"{batch.device_id}_stack"]
        current_id_stack.insert_one(message)

        pipeline = [
            {"$match": {"device_id": batch.device_id}},
            {"$count": "total_count"}
        ]

        result = list(current_id_stack.aggregate(pipeline))

        if result:
            total_count = result[0]['total_count']
            if total_count == 5:
                print("Сработало ongoing rule для ID: {batch.device_id}!")
                ongoing.insert_one({"device_id": batch.device_id,
                                    "timestamp": str(time.time())
                                    })
                db.drop_collection(current_id_stack)
            if current_id_stack.count_documents({}) >= 10:
                db.drop_collection(current_id_stack)

        print(f"Сообщение добавлено в коллекцию data: {message}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Ошибка при обработке сообщения: {e}")


channel.basic_consume(queue='validated_queue', on_message_callback=callback)

def main():
    channel.start_consuming()

if __name__ == "__main__":
    main()