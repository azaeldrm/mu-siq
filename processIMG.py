import cv2 as cv
import sys

def process_img(img_name, sheet_dir, camera_dir):

    img = cv.imread(camera_dir+img_name,0)
    blur = cv.GaussianBlur(img,(5,5),0)
    ret,th_img = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
    cv.imwrite(sheet_dir+img_name,th_img)
