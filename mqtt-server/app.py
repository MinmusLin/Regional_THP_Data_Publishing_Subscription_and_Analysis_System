from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import threading
import json
import time
import queue
import paho.mqtt.client as mqtt
from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

CORS(app)

MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_KEEP_ALIVE_INTERVAL = 60

mqtt_client = mqtt.Client()

topic_queues = {}

def on_connect(client, userdata, flags, rc):
    pass

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode('utf-8')
    if topic in topic_queues:
        topic_queues[topic].put(payload)

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEP_ALIVE_INTERVAL)
mqtt_client.loop_start()

@app.route('/pub/<topic>', methods=['POST'])
def publish_topic(topic):
    try:
        data = request.get_json()
        mqtt_client.publish(f'{topic}/data', json.dumps(data))
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/sub/<topic>', methods=['GET'])
def subscribe_topic(topic):
    mqtt_topic = f'{topic}/data'
    mqtt_client.subscribe(mqtt_topic)
    if mqtt_topic not in topic_queues:
        topic_queues[mqtt_topic] = queue.Queue()

    def event_stream(q):
        while True:
            try:
                message = q.get()
                data = json.loads(message)
                sorted_items = sorted(data.items(), key=lambda x: datetime.strptime(x[0], '%Y-%m-%dT%H:%M:%S'))
                times = [datetime.strptime(k, '%Y-%m-%dT%H:%M:%S').strftime('%H:%M') for k, v in sorted_items]
                temperatures = [float(v) for k, v in sorted_items]
                average = round(sum(temperatures) / len(temperatures), 2)
                average_str = f'{average:.2f}'
                plt.figure(figsize=(10, 5))
                plt.plot(times, temperatures, marker='o')
                plt.xlabel('Time')
                plt.ylabel('Y')
                plt.xticks(rotation=45)
                plt.tight_layout()
                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                plt.close()
                buf.seek(0)
                image_base64 = base64.b64encode(buf.read()).decode('utf-8')
                response_data = {
                    'date': sorted_items[0][0][:10],
                    'average': average_str,
                    'detail': image_base64
                }
                yield f'data: {json.dumps(response_data)}\n\n'
            except GeneratorExit:
                mqtt_client.unsubscribe(mqtt_topic)
                break
            except Exception as e:
                error_data = {
                    'date': 'null',
                    'average': 'null',
                    'detail': e
                }
                yield f'data: {json.dumps(error_data)}\n\n'

    return Response(stream_with_context(event_stream(topic_queues[mqtt_topic])), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, threaded=True)