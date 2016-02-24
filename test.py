
import cv2

#img = cv2.imread("/Users/xuqi/Documents/1.jpg")

cap = cv2.VideoCapture(1)


ret, frame = cap.read()
frame = cv2.imencode('.jpg', frame)[1].tostring()

file_object = open('pystream/pic/test.jpg', 'w')
file_object.write(frame)
file_object.close( )

# img = cv2.imread("test.jpg")
#
# cv2.namedWindow("Image")
#
# cv2.imshow("Image", img)
#
# cv2.waitKey (0)
#
# cv2.destroyAllWindows()