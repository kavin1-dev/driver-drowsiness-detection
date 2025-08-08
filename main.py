import cv2

img = cv2.imread('assetts/spider.jpeg', 0)

cv2.imshow('nanthanda', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
