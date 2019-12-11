# USAGE
# python scan.py --image images/page.jpg

# import the necessary packages
from pyimagesearch.transform import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2 as cv
import imutils
import sys

def scan_img(img_name, camera_dir, scan_dir):
	
	image = cv.imread(camera_dir+img_name)
	ratio = image.shape[0] / 300.0
	orig = image.copy()
	image = imutils.resize(image, height = 300)
	height, width = image.shape[:2]

	# convert the image to grayscale, blur it, and find edges
	# in the image
	gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
	gray = cv.GaussianBlur(gray, (5, 5), 0)
	edged = cv.Canny(gray, 75, 200)

	# show the original image and the edge detected image
	print("STEP 1: Edge Detection")
	# find the contours in the edged image, keeping only the
	# largest ones, and initialize the screen contour
	cnts = cv.findContours(edged.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	cnts = sorted(cnts, key = cv.contourArea, reverse = True)[:5]

	# loop over the contours
	for c in cnts:
		# approximate the contour
		peri = cv.arcLength(c, True)
		approx = cv.approxPolyDP(c, 0.02 * peri, True)

		# if our approximated contour has four points, then we
		# can assume that we have found our screen
		if len(approx) == 4:
			screenCnt = approx
			error_bool = False
			break

	try:
		screenCnt
	except NameError:
		print('Failed to gather 4-point contours.')
		screenCnt = np.array([[width, 0], [0, 0], [0, height], [width, height]])
		error_bool = True

	# show the contour (outline) of the piece of paper
	print("STEP 2: Find contours of paper")
	try:
		cv.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
		# apply the four point transform to obtain a top-down
		# view of the original image
		warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

		print("STEP 3: Apply perspective transform")
		warped = cv.cvtColor(warped, cv.COLOR_BGR2GRAY)
		
		if error_bool == False:
			# convert the warped image to grayscale, then threshold it
			# to give it that 'black and white' paper effect
			blur = cv.GaussianBlur(warped,(5,5),0)
			ret,T = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
			warped = (warped < T).astype("uint8") * 255


		print("STEP 4: Save scanned results")
		cv.imwrite(scan_dir+img_name,warped)

	except Exception as e:
		print(e)
		return False

	