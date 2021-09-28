# kafka consumer & flask server for displaying the received stream
import datetime
import time
import json
from flask import Flask, Response
from kafka import KafkaConsumer
from pose_estimator import PoseEstimator
import numpy as np
import cv2

with open("kafka_client_config.json") as fp:
    config = json.load(fp)

topic = config['topic']
bootstrap_server_ip = config['bootstrap_server_ip']
port = config['port']
process = config['process']


consumer = KafkaConsumer(
    topic, 
    bootstrap_servers=['{}:{}'.format(bootstrap_server_ip, port)])


# Set the consumer in a Flask App
app = Flask(__name__)

pe = PoseEstimator(
    static_image_mode=False,
    model_complexity=config['model_complexity']
)
process_time = []
@app.route('/video', methods=['GET'])
def video():
    """
    This is the heart of our video display. Notice we set the mimetype to 
    multipart/x-mixed-replace. This tells Flask to replace any old images with 
    new values streaming through the pipeline.
    """
    return Response(
        get_video_stream(), 
        mimetype='multipart/x-mixed-replace; boundary=frame')

def get_video_stream():
    """
    Here is where we recieve streamed images from the Kafka Server and convert 
    them to a Flask-readable format.
    """
    frame_cnt = 0
    for msg in consumer:
        if process and (frame_cnt % config['frame_rate'] == 0):
            start = time.time()
            frame = process_video(msg.value)
            ret, buffer = cv2.imencode('.jpg', frame)
            img_bytes = buffer.tobytes()
            end = time.time()
            print("process_time:", end-start)
        else:
            img_bytes = msg.value
        yield (b'--frame\r\n'
               b'Content-Type: image/jpg\r\n\r\n' + img_bytes + b'\r\n\r\n')
        frame_cnt += 1

def process_video(frame):
    """
    given video frame, perform pose estimation and return annotated frame
    """
    nparr = np.fromstring(frame, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    results = pe.process_image(image)
    annotated_frame = pe.draw_pose_annotation(image, results)
    return annotated_frame

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
