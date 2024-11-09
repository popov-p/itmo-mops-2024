from .rabbitmq import connect_to_rabbitmq
from ..proto.messages_pb2 import Batch
from flask import Flask,  Response, request
from flask_pymongo import PyMongo
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://pavel:popov@mongo:27017/iotdata?authSource=admin"

mongo = PyMongo(app)

rabbitmq_channel = connect_to_rabbitmq()

@app.route("/incoming-data", methods=["POST"])
def incoming_data():
    try:
        batch = Batch()
        batch.ParseFromString(request.data)
        if batch.alpha < 25:
            return Response( "Не принято! Ожидается alpha >= 25", status=501)

        rabbitmq_channel.basic_publish(
            exchange='',
            routing_key='validated_queue',
            body=request.data
        )

        data = {
            "device_id": batch.device_id,
            "alpha": batch.alpha,
            "beta": batch.beta,
            "timestamp": batch.timestamp
        }

        mongo.db.data.insert_one(data)

        return Response(f"Принято. ID отправителя: {batch.device_id}", status=200)

    except Exception as e:
        return Response(f"Ошибка: {str(e)}", status=500)



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)