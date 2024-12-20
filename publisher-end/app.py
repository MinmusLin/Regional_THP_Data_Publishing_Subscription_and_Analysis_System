import time
import json
import threading
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)

CORS(app)

data = {}
is_publishing = {}
current_index = {}
publish_threads = {}

def load_data(topic):
    global data
    data_file = f'sensor-data/{topic}.json'
    with open(data_file, 'r') as f:
        data[topic] = json.load(f)

def publish_data(topic):
    global current_index, is_publishing, data
    while True:
        if is_publishing.get(topic, False) and data.get(topic):
            if current_index.get(topic, 0) < len(data[topic]):
                payload = data[topic][current_index.get(topic, 0)]
                try:
                    response = requests.post(f'http://118.89.72.217:3000/pub/{topic}', json=payload)
                    if response.status_code == 200:
                        print(f'Data {current_index.get(topic, 0)} sent successfully for topic {topic}')
                        current_index[topic] += 1
                    else:
                        print(f'Failed to send data {current_index.get(topic, 0)} for topic {topic}: {response.text}')
                except Exception as e:
                    print(f'Error sending data {current_index.get(topic, 0)} for topic {topic}: {e}')
                time.sleep(1)
            else:
                print(f'All data has been published for topic {topic}')
                is_publishing[topic] = False
                current_index[topic] = 0
        else:
            time.sleep(1)

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
    app.run(host='0.0.0.0', port=3000)