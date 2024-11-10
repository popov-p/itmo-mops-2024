# import pika
#
#
# def connect_to_rabbitmq():
#     credentials = pika.PlainCredentials('pavel', 'popov')
#     parameters = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)
#     connection = pika.BlockingConnection(parameters)
#     channel = connection.channel()
#     channel.queue_declare(queue='validated_queue', durable=True)
#     return channel