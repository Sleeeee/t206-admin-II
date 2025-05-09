from datetime import datetime

from flask import Flask, request
from flask_cors import CORS

import redis

import woody

app = Flask('api_products')
cors = CORS(app)

r = redis.Redis(host='redis', port=6379, db=0)

# ### 2. Product Service ###
@app.route('/api/products', methods=['GET'])
def add_product():
    # product = request.json.get('product', '')
    product = request.args.get('product')
    woody.add_product(str(product))
    return str(product) or "none"

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    return "not yet implemented"


@app.route('/api/products/last', methods=['GET'])
def get_last_product():
    cached_data = r.get("last_product")
    if cached_data:
        last_product = cached_data
    else:
        last_product = woody.get_last_product()  # note: it's a very slow db query
        if last_product is not None:
            r.setex("last_product", 60, last_product)
        else:
            return "No product found"
    return f'db: {datetime.now()} - {last_product}'

if __name__ == "__main__":
    woody.launch_server(app, host='0.0.0.0', port=5000)
