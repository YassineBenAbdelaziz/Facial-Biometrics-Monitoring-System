import dlib
from picamera import PiCamera
import requests
import cv2 as cv
from time import sleep


detector = dlib.get_frontal_face_detector()
url = "http://xxx.xxx.xxx.xxx:5000/upload/"
 

with PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.framerate =10
    sleep(3)

    for i,filename in enumerate(camera.capture_continuous("image.jpeg", format='jpeg', use_video_port=True)):

        img = dlib.load_rgb_image(filename)
        faces = detector(img,1)
        if ( faces ) :
            b , arr = cv.imencode(".jpg",img)
            files = arr.tobytes()
            r = requests.post(url, files={'file':(str(len(faces)),files)})

