import pika, time

device_channels = {}
def create_connection():
    while True:
        try:
            credentials = pika.PlainCredentials('pavel', 'popov')
            parameters = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)
            new_connection = pika.BlockingConnection(parameters)
            print("Подключён к брокеру.")
            return new_connection
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Ошибка при подключении: {e}. Попробуем снова через 1 секунду.")
            time.sleep(2)

rabbitmq_connection = create_connection() #rabbitmq
def create_channel_for_device(connection, device_id):
    channel = connection.channel()
    channel.queue_declare(queue='validated_queue', durable=True)
    device_channels[device_id] = channel
    return channel