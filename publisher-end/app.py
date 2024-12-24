import time
import json
import threading
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from datetime import datetime
import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

CORS(app)

MQTT_BROKER = '118.89.72.217'
MQTT_PORT = 8083
MQTT_KEEP_ALIVE = 60
MQTT_USERNAME = 'mqtt_server'
MQTT_PASSWORD = 'mqtt_password'

mqtt_client = mqtt.Client(transport='websockets')
mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

data = {}
is_publishing = {}
current_index = {}
publish_threads = {}

def load_data(topic):
    global data
    data_file = f'sensor-data/{topic}.json'
    with open(data_file, 'r') as f:
        data[topic] = json.load(f)

def format_data(raw_data):
    date_str = list(raw_data.keys())[0][5:10]
    values = [float(value) for value in raw_data.values()]
    average = round(sum(values) / len(values), 2)
    average_str = f'{average:.2f}'
    detail = []
    for timestamp, value in raw_data.items():
        time_str = timestamp[11:16]
        value_str = f'{float(value):.2f}'
        detail.append({'time': time_str, 'value': value_str})
    detail_sorted = sorted(detail, key=lambda x: datetime.strptime(x['time'], '%H:%M'))
    graph = generate_graph(detail_sorted)
    return {
        'date': date_str,
        'average': average_str,
        'detail': detail_sorted,
        'graph': graph
    }

def generate_graph(detail_sorted):
    times = [item['time'] for item in detail_sorted]
    values = [float(item['value']) for item in detail_sorted]
    plt.figure(figsize=(10, 5))
    plt.plot(times, values, marker='o', linestyle='-', color='b')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title('Time vs Value')
    plt.grid(True)
    plt.xticks(rotation=45)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    graph_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    return graph_base64

def publish_data(topic):
    global current_index, is_publishing, data
    while True:
        if is_publishing.get(topic, False) and data.get(topic):
            if current_index.get(topic, 0) < len(data[topic]):
                raw_data = data[topic][current_index.get(topic, 0)]
                formatted_data = format_data(raw_data)
                try:
                    mqtt_client.publish(f'{topic}/data', json.dumps(formatted_data))
                    print(f'Data {current_index.get(topic, 0)} sent successfully for topic {topic}')
                    current_index[topic] += 1
                except Exception as e:
                    print(f'Error sending data {current_index.get(topic, 0)} for topic {topic}: {e}')
                time.sleep(1)
            else:
                print(f'All data has been published for topic {topic}')
                is_publishing[topic] = False
                current_index[topic] = 0
        else:
            time.sleep(1)

def connect_mqtt():
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEP_ALIVE)
        mqtt_client.loop_start()
        print('MQTT client has successfully connected to the MQTT broker')
    except Exception as e:
        print(f'MQTT client connection failed: {e}')

@app.route('/pub/<topic>', methods=['GET'])
def toggle_publish(topic):
    global is_publishing, current_index, publish_threads
    if is_publishing.get(topic, False):
        is_publishing[topic] = False
        return jsonify({'status': 'paused', 'message': 'Data publishing paused for topic ' + topic})
    else:
        if topic not in data:
            load_data(topic)
        is_publishing[topic] = True
        if topic not in current_index:
            current_index[topic] = 0
        if topic not in publish_threads or not publish_threads[topic].is_alive():
            publish_threads[topic] = threading.Thread(target=publish_data, args=(topic,), daemon=True)
            publish_threads[topic].start()
        return jsonify({'status': 'started', 'message': 'Data publishing started for topic ' + topic})

if __name__ == '__main__':
    connect_mqtt()
    app.run(host='0.0.0.0', port=3000)