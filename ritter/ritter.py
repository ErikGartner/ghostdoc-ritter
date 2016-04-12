import os
import json

import pika
from pymongo import MongoClient

from .artifact_analyzer import ArtifactAnalyzer


class Ritter:
    def start(self):

        config = self.read_config()

        client = MongoClient(config['mongo_uri'])
        self.database = client.get_default_database()

        connection = pika.BlockingConnection(pika.URLParameters(config['rabbit_uri']))
        channel = connection.channel()
        channel.queue_declare(queue='ghostdoc-ritter', durable=True)
        channel.basic_consume(self.mq_callback, queue='ghostdoc-ritter')
        channel.start_consuming()

    def mq_callback(self, ch, method, properties, body):
        msg = str(body, 'UTF-8')
        print(" [x] Received %s" % msg)
        data = json.loads(msg)

        if data['type'] == 'artifact_analyzer':
            artifact_analyzer = ArtifactAnalyzer(self.database, data['data'])
            artifact_analyzer.analyze()
        else:
            print('Unknown command type: %s' % data['type'])

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def read_config(self):
        config = {
            'MONGO_URL':
            os.getenv('mongo_uri', 'mongodb://localhost:3001/meteor'),
            'RABBITMQ_URL':
            os.getenv('rabbit_uri', 'amqp://guest:guest@localhost:5672')
        }
        return config
