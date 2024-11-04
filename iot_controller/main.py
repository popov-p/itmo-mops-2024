from iot_proto_message import Batch
import time
import pika
from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def hello_world():
    batch = Batch(
    device_id=123,
    value=45.67,
    timestamp = str(time.time())
    )
    return f"{batch.value}ЫЫЫЫ"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)