import pika
import woody
import os
import json
import time

rabbitmq_user = os.getenv('RABBITMQ_DEFAULT_USER')
rabbitmq_pass = os.getenv('RABBITMQ_DEFAULT_PASS')
rabbitmq_host = os.getenv('RABBITMQ_HOST')

def get_rabbitmq_channel():
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
    retry_count = 0
    max_retries = 500
    while retry_count < max_retries:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=rabbitmq_host,
                    credentials=credentials,
                    connection_attempts=3,
                    retry_delay=5
                )
            )
            channel = connection.channel()
            channel.queue_declare(queue='task_queue', durable=True)
            return channel
        except Exception as e:
            retry_count += 1
            print(f"Failed to connect to RabbitMQ (attempt {retry_count}/{max_retries}): {e}")
            if retry_count >= max_retries:
                raise
            time.sleep(5)

# #### 4. internal Services
def process_order(order_id, order):
    # ...
    # ... do many check and stuff
    status = woody.make_heavy_validation(order)

    woody.save_order(order_id, status, order)

def callback(ch, method, properties, body):
    order_message = json.loads(body)
    order_id = order_message['order_id']
    order_product = order_message['product']
    print(f'Received order {order_id} for product {order_product}')
    process_order(order_id, order_product)

    print('Task completed!')
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_worker():
    channel = get_rabbitmq_channel()
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue', on_message_callback=callback)

    print('Worker initialized. Waiting for tasks to be consumed')
    channel.start_consuming()

if __name__ == '__main__':
    start_worker()
