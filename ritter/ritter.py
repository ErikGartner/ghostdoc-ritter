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

        connection = pika.BlockingConnection(pika.ConnectionParameters(
            'localhost'))
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
            'mongo_uri':
            os.getenv('mongo_uri', 'mongodb://localhost:3001/meteor')
        }
        return config
