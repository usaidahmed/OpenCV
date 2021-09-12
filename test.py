import cv2
im = cv2.imread("medOriginal2.jpg", 0)
im1 = cv2.imread("medDefected2.jpg", 0)

diff = cv2.absdiff(im, im1)
ret, thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
thresholded = cv2.erode(thresh, (16,16), iterations = 3)
contours, hierarchy = cv2.findContours(thresholded, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
mask = cv2.cvtColor(im1, cv2.COLOR_GRAY2BGR)

try:
    hierarchy = hierarchy[0]
except:
     hierarchy = []

for contour in contours[:-1]:
    (x, y, w, h) = cv2.boundingRect(contour)
    area = cv2.contourArea(contour)
    if area>10:
        cv2.rectangle(im1, (x, y), (x+w, y+h), (0, 255, 255), 2)

cv2.namedWindow('mask', cv2.WINDOW_NORMAL)
cv2.imshow("mask", diff)
cv2.namedWindow('thresh', cv2.WINDOW_NORMAL)
cv2.imshow("thresh", im1)
cv2.waitKey(0)