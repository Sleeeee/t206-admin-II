import uuid

from flask import Flask, request
from flask_cors import CORS

import woody

app = Flask('api_orders')
cors = CORS(app)

# ### 3. Order Service
@app.route('/api/orders/do', methods=['GET'])
def create_order():
    # very slow process because some payment validation is slow (maybe make it asynchronous ?)
    # order = request.get_json()
    product = request.args.get('order')
    order_id = str(uuid.uuid4())

    # TODO TP10: this next line is long, intensive and can be done asynchronously ... maybe use a message broker ?
    process_order(order_id, product)
    return f"Your process {order_id} has been created with this product : {product}"

@app.route('/api/orders/', methods=['GET'])
def get_order():
    order_id = request.args.get('order_id')
    status = woody.get_order(order_id)

    return f'order "{order_id}": {status}'

# #### 4. internal Services
def process_order(order_id, order):
    # ...
    # ... do many check and stuff
    status = woody.make_heavy_validation(order)

    woody.save_order(order_id, status, order)

if __name__ == "__main__":
    woody.launch_server(app, host='0.0.0.0', port=5000)
