import os
import json
import time

import pika
from pymongo import MongoClient

from .artifact_analyzer import ArtifactAnalyzer
from .source_analyzer import SourceAnalyzer


class Ritter:
    def start(self):

        config = self.read_config()

        client = MongoClient(config['mongo_uri'])
        self.database = client.get_default_database()

        connection = pika.BlockingConnection(pika.URLParameters(config[
            'rabbit_uri']))
        channel = connection.channel()
        channel.queue_declare(queue='ghostdoc-ritter',
                              durable=True,
                              arguments={'x-max-priority': 10})
        channel.basic_consume(self.mq_callback, queue='ghostdoc-ritter')
        channel.start_consuming()

    def mq_callback(self, ch, method, properties, body):
        msg = str(body, 'UTF-8')
        print("[ ] Received %s" % msg)
        data = json.loads(msg)

        start_time = time.perf_counter()
        if data['type'] == 'artifact_analyzer':
            analyzer = ArtifactAnalyzer(self.database, data['data'])
            analyzer.analyze()
        elif data['type'] == 'source_analyzer':
            analyzer = SourceAnalyzer(self.database, data['data'])
            analyzer.analyze()
        else:
            print('Unknown command type: %s' % data['type'])

        try:
            pass
        except Exception as e:
            print('[e] Failed to process (%s)\n' % e)
        else:
            print('[x] Processed cmd in %ss\n' %
                  (time.perf_counter() - start_time))
        finally:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def read_config(self):
        config = {
            'mongo_uri':
            os.getenv('MONGO_URL', 'mongodb://localhost:3001/meteor'),
            'rabbit_uri':
            os.getenv('RABBITMQ_URL', 'amqp://guest:guest@localhost:5672')
        }
        return config
