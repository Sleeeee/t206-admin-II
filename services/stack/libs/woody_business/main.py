from time import sleep

WAITING_TIME = 10


def do_woody_stuff_with_data(data:str) -> str:
    sleep(WAITING_TIME)
    return f"woody woody: {data}"


def run_server_with_woody_needs(app):
    app.run()
