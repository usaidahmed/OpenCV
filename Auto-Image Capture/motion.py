import cv2
import imutils
import time
import datetime

# frame from video is none 
first_frame = None

camera = cv2.VideoCapture(0)

# loop into frames of the video
while True:
    # grab the current frame 
    (grabbed, frame) = camera.read()
    text = "undetected"

    # is no frame grabbed the is end of video 
    if not grabbed:
        break

    # resize the frame 
    frame = imutils.resize(frame, width=640)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # is first frame is none , make gray 
    if first_frame is None:
        first_frame = gray
        continue


    # compute difference from current frame and first frame 
    frameDelta = cv2.absdiff(first_frame, gray)
    first_frame = gray
    thresh = cv2.threshold(frameDelta, 1, 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes
    # then find contours on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                 cv2.CHAIN_APPROX_SIMPLE)

    # loop contours 
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < 10000:
            continue

        # compute the bounding box for the contour
        # draw it on the frame,
        # and update the text
        #(x, y, w, h) = cv2.boundingRect(c)
        #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 0)
        roi = frame
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y_%H-%M-%S')
        # if the detection is on sized then save the image 
        #if (w > h ) and (y + h) > 50 and (y + h) < 550:
        cv2.imwrite(st+"opencv.jpg", roi)
        # set text to show on gui 
        text = "detected"
    
    # draw the text and timestamp on the frame
    cv2.putText(frame, "Detect: {}".format(text), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    #show frame , thresh and frame_Delta
    cv2.imshow("Security Feed", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    key = cv2.waitKey(1) &  0xFF

    # break from loop with q key 
    if key == ord("q"):
        break

# close camera and windows 
camera.release()
cv2.destroyAllWindows()