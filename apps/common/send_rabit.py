#!/usr/bin/env python
import pika


def send_rabit():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='chimpanzee.rmq.cloudamqp.com',
            virtual_host='ftzmpaoj',
            credentials=pika.PlainCredentials(username='ftzmpaoj', password='pEYJ7Q6W5G36I4o-UWbrSNYctawNNZ6L')))
    channel = connection.channel()

    channel.queue_declare(queue='test')

    channel.basic_publish(exchange='',
                          routing_key='test',
                          body='Hello World!')
    print(" [x] Sent 'Hello World!'")
    connection.close()
