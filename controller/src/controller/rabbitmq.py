import pika

device_channels = {}

def create_connection():
    credentials = pika.PlainCredentials('pavel', 'popov')
    parameters = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    return connection

def create_channel_for_device(device_id):
    credentials = pika.PlainCredentials('pavel', 'popov')
    parameters = pika.ConnectionParameters('itmo-mops-2024-rabbitmq-1', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='validated_queue', durable=True)
    device_channels[device_id] = channel
    return channel