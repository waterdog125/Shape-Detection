# USAGE
# python detect_shapes.py --image shapes_and_colors.png

# import the necessary packages
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
ap.add_argument("-r", "--rectangle", action="store_true")
ap.add_argument("-t","--triangle", action="store_true")
ap.add_argument("-p","--pentagon", action="store_true")
ap.add_argument("-c","--circle", action="store_true")
ap.add_argument("-s","--square", action="store_true")
args = vars(ap.parse_args())

# load the image and resize it to a smaller factor so that
# the shapes can be approximaed better
image = cv2.imread(args["image"])
rectangleflag = args["rectangle"]
triangleflag = args["triangle"]
pentaflag = args["pentagon"]
circleflag = args["circle"]
sqflag = args["square"]
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])

# convert the resized image to grayscale, blur it slightly,
# and threshold it
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

# find contours in the thresholded image and initialize the
# shape detector
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
sd = ShapeDetector()

# loop over the contours
if (rectangleflag or triangleflag or pentaflag or circleflag or sqflag):
	if rectangleflag:
		expected = "rectangle"
	elif triangleflag:
		expected = "triangle"
	elif pentaflag:
		expected = "pentagon"
	elif circleflag:
		expected = "circle"
	else:
		expected = "square"

	for c in cnts:
	# compute the center of the contour, then detect the name of the
	# shape using only the contour
		M = cv2.moments(c)
		cX = int((M["m10"] / M["m00"]) * ratio)
		cY = int((M["m01"] / M["m00"]) * ratio)
	


		shape = sd.detect(c,args)

	# multiply the contour (x, y)-coordinates by the resize ratio,
	# then draw the contours and the name of the shape on the image
		c = c.astype("float")
		c *= ratio
		c = c.astype("int")
		if(expected == shape):
			cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
			cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
				0.5, (255, 255, 255), 2)

	# show the output image
		cv2.imshow("Image", image)
		cv2.waitKey(0)

else: 
	print("Please enter shape flag.")
	exit()