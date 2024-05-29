import random
import time
from multiprocessing import queues, Process, SimpleQueue, cpu_count
from paho.mqtt import client as mqtt_client


broker = 'emqx.pepemoss.com'
port = 1883

def connect_mqtt(client_id):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    
    client_id = f'publish-{random.randint(0, 1000)}'
    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 1
    while True:
        msg = f"messages: {msg_count}"
        topic = "unit.pepemoss.com/output/fb173ae2-80b1-4a5f-9d9d-61aee7b859ec/one/pepeunit"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]

        msg_count+=1
        if msg_count % 10000 == 0:

            print(time.perf_counter())


def run(client_id):
    client = connect_mqtt(client_id)
    client.loop_start()
    publish(client)
    client.loop_stop()


def worker(jobs, results) -> None:
    while path := jobs.get():
        results.put(run(path))
    results.put(None)


def start_jobs(procs, jobs, results, images_path):
    for item in images_path:
        jobs.put(item)
    for _ in range(procs):
        proc = Process(target=worker, args=(jobs, results))
        proc.start()
        jobs.put(0)


def get_uuid_images(images_path, results):
    uuid_images = []
    procs_done = 0
    while procs_done < len(images_path):
        uuid = results.get()

        if uuid == None:
            pass
        else:
            procs_done += 1
            uuid_images.append(uuid)

    return uuid_images


def gen_dataset() -> list[str]:
    
    client_ids = [
        '<token>' for item in range(0, 36)]

    jobs = SimpleQueue()
    results = SimpleQueue()

    start_jobs(1, jobs, results, client_ids)

    return get_uuid_images(client_ids, results)

if __name__ == '__main__':                                                                                              
    gen_dataset()
