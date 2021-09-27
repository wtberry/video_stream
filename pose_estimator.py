# module for pose estimation
# for video implementation
import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose

"""
Requires to install mediapipe: pip install mediapipe
"""
class PoseEstimator(object):
    """
    CLASS
    Take Input image from cv2.Videocaputure(), and run pose estimation using
    google's mediapipe API.
    Return result obj from mp.pose api

    Args:
        - min_detection_confidence:
        - min_tracking_confidence:
        - preprocesing: function to be passed. takes in image
        - flip: whether to flip image horizontally or not, for selfie view.
    """
    
    def __init__(
        self, min_detection_confidence=0.5, min_tracking_confidence=0.5, 
        preprocessing=None, flip=True
        ) -> None:

        self.pose = mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.flip = flip
    
    def process_image(self, image, preprocess=True):
        """
        perform mediapipe pose estimaton on given image frame. 
        Image is flipped horizontally if flip is True for self.Flip is true
        """
        image = cv2.flip(image, 1) if self.flip else image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = self.pose.process(image)
        image.flags.writeable = True
        return results


    def draw_pose_annotation(self, image, results, flip=True):
        """
        draw pose annotation on given image.
        Args:
            - image: opencv bgr image
            - results: result from pose
            - Flip: flip image for selfie view
        return:
            image with the annotation drawn on top
        """
        #image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image = cv2.flip(image, 1) if self.flip else image
        image.flags.writeable = True
        self.mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
        )
        return image