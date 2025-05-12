import uuid

from flask import Flask, request
from flask_cors import CORS

import pika
import os
import woody
import json

app = Flask('api_orders')
cors = CORS(app)

rabbitmq_user = os.getenv('RABBITMQ_DEFAULT_USER')
rabbitmq_pass = os.getenv('RABBITMQ_DEFAULT_PASS')
rabbitmq_host = os.getenv('RABBIT_HOST')

connection = None
channel = None

def get_rabbitmq_channel():
    global connection, channel
    if not connection or connection.is_closed:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', credentials=pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)))
        channel = connection.channel()
        channel.queue_declare(queue='order_queue', durable=True)
    return channel

# ### 3. Order Service
@app.route('/api/orders/do', methods=['GET'])
def create_order():
    # very slow process because some payment validation is slow (maybe make it asynchronous ?)
    # order = request.get_json()
    product = request.args.get('order')
    order_id = str(uuid.uuid4())

    # Send the message through RabbitMQ to a remote worker
    order_message = {
        'order_id': order_id,
        'product': product
    }
    channel = get_rabbitmq_channel()
    channel.basic_publish(
        exchange='',
        routing_key='order_queue',
        body=json.dumps(order_message),
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )

    return f"Your process {order_id} has been created with this product : {product}"

@app.route('/api/orders/', methods=['GET'])
def get_order():
    order_id = request.args.get('order_id')
    status = woody.get_order(order_id)

    return f'order "{order_id}": {status}'

if __name__ == "__main__":
    woody.launch_server(app, host='0.0.0.0', port=5000)
