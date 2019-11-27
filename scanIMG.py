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
	
	# try:

		# construct the argument parser and parse the arguments
		# ap = argparse.ArgumentParser()
		# ap.add_argument("-i", "--image", required = True,
		# 	help = "Path to the image to be scanned")
		# args = vars(ap.parse_args())

		# load the image and compute the ratio of the old height
		# to the new height, clone it, and resize it
		# image = cv.imread(args["image"])
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
	# cv.imshow("Image", image)
	# cv.imshow("Edged", edged)
	# cv.waitKey(0)
	# cv.destroyAllWindows()

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
		# print(screenCnt)
		error_bool = True

	# show the contour (outline) of the piece of paper
	print("STEP 2: Find contours of paper")
	try:
		cv.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
		# cv.imshow("Outline", image)
		# cv.waitKey(0)
		# cv.destroyAllWindows()

		# apply the four point transform to obtain a top-down
		# view of the original image
		warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

		print("STEP 3: Apply perspective transform")
		warped = cv.cvtColor(warped, cv.COLOR_BGR2GRAY)
		# warped_h, warped_w = warped.shape
		# cfactor = 200
		# warped = warped[cfactor:2900, cfactor:2700]
		# alpha = 1.25 # Contrast control (1.0-3.0)
		# beta = 0 # Brightness control (0-100)
		# warped = cv.convertScaleAbs(warped, alpha=alpha, beta=beta)
		
		# cv.imshow("Warped image", imutils.resize(warped, height = 650))
		if error_bool == False:
			# convert the warped image to grayscale, then threshold it
			# to give it that 'black and white' paper effect
			blur = cv.GaussianBlur(warped,(5,5),0)
			ret,T = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
			# T = threshold_local(warped, 11, offset = 10, method = "gaussian")
			warped = (warped < T).astype("uint8") * 255
			# cv.imshow("Warped image w/ Otsu threshold", imutils.resize(warped, height = 650))
			# cv.waitKey(0)

		# show the original and scanned images
		print("STEP 4: Show original and scanned results")
		# cv.imshow("Original", imutils.resize(orig, height = 650))
		# cv.imshow("Scanned", imutils.resize(warped, height = 650))
		# cv.waitKey(0)
		# cv.destroyAllWindows()

		print("STEP 5: Save scanned results")
		cv.imwrite(scan_dir+img_name,warped)
		# print(args["image"][len(args["image"])-args["image"][::-1].find('/')])
		# cv.imwrite(args["image"][:-4]+"_scanned"+args["image"][-4:],warped)

		# print("STEP 6: Confirm image results")
		# if input("Is this a good image result? [Y/N]\n") == 'Y':
		# 	return True
		# else:
		# 	return False

	except Exception as e:
		print(e)
		return False

	