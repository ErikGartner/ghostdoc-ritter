import pika

def callback(ch, method, properties, body):
    print(" [x] Received %s" % str(body, 'UTF-8'))
    ch.basic_ack(delivery_tag = method.delivery_tag)

def start():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
                   'localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='ghostdoc-ritter', durable=True)
    channel.basic_consume(callback, queue='ghostdoc-ritter')
    channel.start_consuming()
