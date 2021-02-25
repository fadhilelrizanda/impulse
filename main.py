import cv2
import csv
import boto3
import json
import time

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

    print("")
    print(response)
    print("")
    for entry in response["Labels"]:

        if(entry["Name"]):
            if(entry["Name"] == "Truck"):
                print("Truck Detected ! ")
                if(entry["Confidence"] >= 90):
                    print("Truck Confidence Over " +
                          str(entry["Confidence"]) + "% !")
                break
            else:
                print("No truck labels")
        else:
            break
    count = count+1
