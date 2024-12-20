from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import threading
import json
import time
import queue
import paho.mqtt.client as mqtt

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
                yield f'{message}\n'
            except GeneratorExit:
                mqtt_client.unsubscribe(mqtt_topic)
                break
    return Response(stream_with_context(event_stream(topic_queues[mqtt_topic])), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, threaded=True)