import cv2

vidcap = cv2.VideoCapture('stream.mp4')
fps = int(vidcap.get(cv2.CAP_PROP_FPS))
framecount = 0

while(True):
    # Capture frame-by-frame
    success, image = vidcap.read()
    framecount += 1

    # Check if this is the frame closest to 10 seconds
    if framecount == (fps * 10):
        framecount = 0
        cv2.imshow('image', image)

    # Check end of video
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
