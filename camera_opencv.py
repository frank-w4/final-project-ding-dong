import os
import cv2
from base_camera import BaseCamera
import numpy as np
import os



class Camera(BaseCamera):
    video_source = 0

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()
    
    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        img_count = 0
        """
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            _, img = camera.read()

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()
        """
        fadeCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera')
        
        while True:
            cmd = "rm "
            ret, img = camera.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = fadeCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(20,20)
            )
            for(x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = img[y:y+h, x:x+w]
            print("New Image " + str(img_count))
            yield cv2.imencode('.jpg', img)[1].tobytes()
            path = './tmp/' + str(img_count) + '.jpg'
            if (img_count > 50):
                cmd += './tmp/' + str(img_count-49) + '.jpg'
                returned_value = os.system(cmd)
            cv2.imwrite(path, img, [int(cv2.IMWRITE_PNG_COMPRESSION), 3])
            img_count = img_count + 1
