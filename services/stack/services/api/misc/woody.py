from time import sleep
from werkzeug.serving import run_simple

LONG_WAIT_TIME = 5  # seconds

def make_some_heavy_computation(param=""):
    sleep(LONG_WAIT_TIME)
    return f"Woody -{param}- Woody"

def make_heavy_validation(order):
    make_some_heavy_computation()
    return "Success"

def save_order(order_id, status, product):
    mydb, mycursor = my_connect()
    query = f"INSERT INTO woody.order (order_id, status, product) VALUES ('{order_id}', '{status}', '{product}');"

    mycursor.execute(query)
    mydb.commit()

    mycursor.close()
    mydb.close()

def launch_server(app, host='0.0.0.0', port=5000):
    # voici ce qui rend le serveur si limité ...
    run_simple(host, port, app, use_reloader=True, threaded=False)

