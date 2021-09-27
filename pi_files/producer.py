# producer script for video stream
import sys
import time
import cv2
from kafka import KafkaProducer
import json

with open("kafka_config.json") as fp:
    config = json.load(fp)

topic = config['topic']
bootstrap_server_ip = config['bootstrap_server_ip']




def publish_video(video_file):
    """
    Publish given video file to a specified Kafka topic.
    Kafka Server is expected to be running on the localhost. Not partitioned.

    :param video_file: path to video file <string>
    """
    # Start up producer
    producer = KafkaProducer(bootstrap_servers='{}:9092'.format(bootstrap_server_ip))

    # Open file
    video = cv2.VideoCapture(video_file)

    print('publishing video...')

    while(video.isOpened()):
        success, frame = video.read()

        # Ensure file was read successfully
        if not success:
            print("bad read!")
            break

        # Convert image to png
        ret, buffer = cv2.imencode('.jpg', frame)

        # Convert to bytes and send to kafka
        producer.send(topic, buffer.tobytes())

        time.sleep(0.2)
    video.release()
    print('publish complete')


def publish_camera():
    """
    Publish camera video stream to specified Kafka topic.
    Kafka Server is expected to be running on the localhost. Not partitioned.
    """

    # Start up producer
    producer = KafkaProducer(bootstrap_servers='{}:9092'.format(bootstrap_server_ip))


    camera = cv2.VideoCapture(0)
    frame_cnt = 0
    try:
        while(True):
            success, frame = camera.read()
            if frame_cnt % config['frame_rate'] == 0:
                ret, buffer = cv2.imencode('.jpg', frame)
                producer.send(topic, buffer.tobytes())
            frame_cnt += 1

            # Choppier stream, reduced load on processor
            #time.sleep(0.5)

    except Exception as e:
        print("\nExiting.", e)
        sys.exit(1)


    camera.release()


if __name__ == '__main__':
    """
    Producer will publish to Kafka Server a video file given as a system arg.
    Otherwise it will default by streaming webcam feed.
    """
    if(len(sys.argv) > 1):
        video_path = sys.argv[1]
        publish_video(video_path)
    else:
        print("publishing feed!")
        publish_camera()
