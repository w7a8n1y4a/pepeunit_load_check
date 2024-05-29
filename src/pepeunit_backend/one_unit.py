import random
import time
from multiprocessing import queues, Process, SimpleQueue, cpu_count
from paho.mqtt import client as mqtt_client

broker = 'emqx.pepemoss.com'
port = 1883
client_id = ''

topics = [
        "one/pepeunit",
        "two/pepeunit",
        "three/pepeunit",
        "four/pepeunit",
        "five/pepeunit",
        "six/pepeunit",
        "seven/pepeunit",
        "acht/pepeunit",
        "neun/pepeunit",
        "zein/pepeunit"
]

def connect_mqtt(client_id):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 1
    while True:
        
        for topic in topics:
            msg = f"messages: {msg_count//100} {msg_count}"
            topic = f'unit.pepemoss.com/output/fb173ae2-80b1-4a5f-9d9d-61aee7b859ec/{topic}'
            result = client.publish(topic, msg)
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")

        msg_count += 1

        time.sleep(0.02)


def run(client_id):
    client = connect_mqtt(client_id)
    client.loop_start()
    publish(client)
    client.loop_stop()


if __name__ == '__main__':
    run(client_id)
