from src.proto import messages_pb2
import time
from flask import Flask, Response, request
import os
app = Flask(__name__)

@app.route("/incoming-data", methods=["POST"])
def incoming_data():
    try:
        batch = messages_pb2.Batch()
        batch.ParseFromString(request.data)
        print(f"Получены данные. ID: {batch.device_id}, value: {batch.value}, timestamp: {batch.timestamp}")

        return Response(f"Принято. ID отправителя: {batch.device_id}", status=200)

    except Exception as e:
        return Response(f"Ошибка: {str(e)}", status=500)


@app.route("/")
def hello_world():
    batch = Batch(
    device_id=123,
    value=12.67,
    timestamp = str(time.time())
    )
    return f"{batch.value}asdЫЫЫxXX-777"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)