# Voici les différentes fonctions que l'api de Woody pourrait utiliser
#
# Il y a beacoup de "sleep", et de ralentissement qui ont pour but de simuler une grosse charge et/ou
# pour simuler des requètes qui seraient (dans un cas réel) plus lourde..
#
# Ce fichier ne peut pas être modifié (du moins pas pour "fixer" les limitations qu'il introduit ;)
# ( ce fichier sera, à terme dans une lib externe pour rendre plus clair la séparation)


from werkzeug.serving import run_simple
from mysql.connector import connect, Error
from time import sleep

LONG_WAIT_TIME = 5  # seconds
SHORT_WAIT_TIME = 5


def my_connect():
    # note, c'est une mauvaise idée de recréer la connection à chaque requète
    # (c'est surtt pour une question de performance)
    # Mais ici, ce n'est pas la performance qu'on cherche ;)

    try:
        mydb = connect(host='db', user='root', password='pass', database='woody', port=3306)
        mycursor = mydb.cursor()
    except Error as e:
        print(e)
        return None, None
    return mydb, mycursor


def get_last_product():
    mydb, mycursor = my_connect()

    mycursor.execute("LOCK TABLES product READ;")

    mycursor.execute("SELECT name, sleep(15) FROM product ORDER BY id DESC LIMIT 1;")

    last_product = mycursor.fetchone()

    mycursor.execute("select count(*) from product;")
    product_count = mycursor.fetchone()

    # sleep(SHORT_WAIT_TIME)

    mycursor.execute("UNLOCK TABLES;")
    mycursor.close()
    mydb.close()

    if last_product is None or product_count is None:
        return "No product found"

    return f'{product_count[0]} products (last={last_product[0]})'


def make_some_heavy_computation(param=""):
    sleep(LONG_WAIT_TIME)
    return f"Woody -{param}- Woody"


def make_heavy_validation(order):
    make_some_heavy_computation()
    return "Success"


def add_product(product):
    mydb, mycursor = my_connect()
    query = f"INSERT INTO woody.product ( name) VALUES ('{product}');"

    mycursor.execute(query)
    mydb.commit()
    mycursor.close()
    mydb.close()


def launch_server(app, host='0.0.0.0', port=5000):
    # voici ce qui rend le serveur si limité ...
    run_simple(host, port, app, use_reloader=True, threaded=False)


def save_order(order_id, status, product):
    mydb, mycursor = my_connect()
    query = f"INSERT INTO woody.order (order_id, status, product) VALUES ('{order_id}', '{status}', '{product}');"

    mycursor.execute(query)
    mydb.commit()

    mycursor.close()
    mydb.close()


def get_order(order_id):
    mydb, mycursor = my_connect()
    query = f"SELECT status FROM woody.order WHERE order_id='{order_id}';"

    mycursor.execute(query)

    order_status = mycursor.fetchone()

    mycursor.close()
    mydb.close()
    return order_status