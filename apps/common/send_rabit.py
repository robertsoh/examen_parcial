import os
import pika


def send_rabit(mensaje):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=os.environ.get('RABBIT_HOST'),
            virtual_host=os.environ.get('RABBIT_VIRTUAL_HOST'),
            credentials=pika.PlainCredentials(username=os.environ.get('RABBIT_USERNAME'),
                                              password=os.environ.get('RABBIT_PASSWORD'))))
    channel = connection.channel()

    channel.queue_declare(queue='test')

    channel.basic_publish(exchange='',
                          routing_key='test',
                          body=mensaje)
    connection.close()
