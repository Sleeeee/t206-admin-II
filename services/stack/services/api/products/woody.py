from werkzeug.serving import run_simple
from mysql.connector import connect, Error

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

def add_product(product):
    mydb, mycursor = my_connect()
    query = f"INSERT INTO woody.product ( name) VALUES ('{product}');"

    mycursor.execute(query)
    mydb.commit()
    mycursor.close()
    mydb.close()

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

def launch_server(app, host='0.0.0.0', port=5000):
    # voici ce qui rend le serveur si limité ...
    run_simple(host, port, app, use_reloader=True, threaded=False)

