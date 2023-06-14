# coding:utf-8

# coding by aaw
# rev json data from promuesq
# send json data to kafka
# send heart for one min one time

from flask import Flask, request
from kafka import KafkaProducer
import json
import threading
import time
import toml

cfg = toml.load("config.toml")

app = Flask(__name__)

kafka_broker = 'localhost:9092'  # Kafka broker address
topic = 'prometheus_data'  # Kafka topic to send Prometheus data
heartbeat_topic = 'heartbeat'  # Kafka topic to send heartbeat data
heartbeat_interval = 60  # Heartbeat interval in seconds

producer = KafkaProducer(bootstrap_servers=kafka_broker, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

@app.route('/prometheus', methods=['POST'])
def receive_prometheus_data():
    data = request.get_json()
    producer.send(topic, data)
    return 'OK'

def send_heartbeat():
    while True:
        heartbeat_data = {
            'timestamp': int(time.time()),
            'message': 'Heartbeat'
        }
        producer.send(heartbeat_topic, heartbeat_data)
        time.sleep(heartbeat_interval)

if __name__ == '__main__':
    # Start the heartbeat thread
    heartbeat_thread = threading.Thread(target=send_heartbeat)
    heartbeat_thread.daemon = True
    heartbeat_thread.start()

    # Start the Flask application
    app.run(host='0.0.0.0', port=5000)
