from time import sleep
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

