import cv2 as cv
import sys

def applyAdaptiveThreshold(source):
    img = cv.imread(source,0)
    blur = cv.GaussianBlur(img,(5,5),0)
    ret,th_img = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
    cv.imwrite("testimage_thresholded.jpg",th_img)

if __name__ == "__main__":
    img_file = sys.argv[1:][0]
    applyAdaptiveThreshold(img_file)
