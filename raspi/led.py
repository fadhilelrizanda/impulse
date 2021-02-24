import RPi.GPIO as GPIO
from time  import sleep


 
import cv2
import csv
import boto3
import json
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(5,GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(3,GPIO.OUT, initial = GPIO.LOW)

with open('cred.csv', 'r') as input:
    next(input)
    reader = csv.reader(input)
    for line in reader:
        access_key_id = line[2]
        secret_key_id = line[3]
        token = line[5]

print(access_key_id)
print(secret_key_id)
print(token)

count = 0
timesleep = 5
label_truck = 0
vidcap = cv2.VideoCapture('stream.mp4')

fps = int(vidcap.get(cv2.CAP_PROP_FPS))
framecount = 0
while (True):

    print("count : " + str(count))
    print("time : " + str(timesleep))

    while(True):
        # Capture frame-by-frame
        success, image = vidcap.read()
        framecount += 1

        # Check if this is the frame closest to 5 seconds
        if success:
            if framecount == (fps * 5):
                framecount = 0
                # save frame as JPEG file
                cv2.imwrite("frame%d.jpg" % count, image)
                print('Read a new frame: ', success)
                break
        else:
            exit()

    photo = 'frame'+str(count)+'.jpg'
    client = boto3.client(
        'rekognition',
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_key_id,
        aws_session_token=token,
        region_name='us-east-1'
    )
    with open(photo, 'rb') as source_image:
        source_byte = source_image.read()

    response = client.detect_labels(
        Image={'Bytes': source_byte}, MaxLabels=10, MinConfidence=80)

    for entry in response["Labels"]:

        if(entry["Name"]):
            if(entry["Name"] == "Truck"):
                print("Truck Detected ! ")
                if(entry["Confidence"] >= 90):
                    print("Truck Confidence Over " +
                          str(entry["Confidence"]) + "% !")
                    label_truck = 1
                break
            else:
                print("No truck labels")
                label_truck = 0
        else:
            break
    
    if(label_truck==1):
        GPIO.output(5, GPIO.HIGH)
        GPIO.output(3, GPIO.LOW)
    else:
        GPIO.output(3, GPIO.HIGH)
        GPIO.output(5,GPIO.LOW)
        
    count = count+1
    print("Label Truck :" +str(label_truck))
