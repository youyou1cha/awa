# coding:utf-8

# coding by aaw
# rev json data from promuesq
# send json data to kafka
# send heart for one min one time

from flask import Flask, request,jsonify
from kafka import KafkaProducer
import json
import threading
import time
import toml
from alarmData import heartBeat,alarmData
from datetime import datetime
import logging
import json
from dataclasses import dataclass, asdict

# read config
cfg = toml.load("config.toml")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("log_file.log"),
        logging.StreamHandler()
    ]
)
# person_dict = asdict(person)
# json_str = json.dumps(person_dict)
app = Flask(__name__)

kafka_broker = cfg['kafka']['kafka_broker']  # Kafka broker address
topic = cfg['kafka']['topic']  # Kafka topic to send Prometheus data
heartbeat_topic = cfg['kafka']['heartbeat_topic']  # Kafka topic to send heartbeat data
heartbeat_interval = cfg['kafka']['heartbeat_interval']  # Heartbeat interval in seconds

# producer = KafkaProducer(bootstrap_servers=kafka_broker, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def  send(message:str,topic:str)->None:
    producer = KafkaProducer(bootstrap_servers=kafka_broker)
    producer.send(topic=topic,key= message.encode('utf-8'))
    producer.close()


@app.route('/prometheus', methods=['POST'])
def receive_prometheus_data():
    data = request.get_json()
    # producer.send(topic, data)
    return jsonify("success")

def send_heartbeat():
    while True:
        current_time = datetime.now()
        time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
        heartbeat_data = heartBeat(eventTime=time_str)
        heartbeat_dict = asdict(heartbeat_data)
        heartbeat_json = json.dumps(heartbeat_dict)
        logging.debug(heartbeat_json)
        # producer.send(heartbeat_topic, heartbeat_json.encode('utf-8'))
        send(topic=heartbeat_topic,message=heartbeat_json)
        time.sleep(heartbeat_interval)

if __name__ == '__main__':
    # Start the heartbeat thread
    # heartbeat_thread = threading.Thread(target=send_heartbeat)
    # heartbeat_thread.daemon = True
    # heartbeat_thread.start()
    send_heartbeat()

    # Start the Flask application
    # app.run(host='0.0.0.0', port=5000)
