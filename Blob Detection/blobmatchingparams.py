import cv2

params = cv2.SimpleBlobDetector_Params()

#Filter by Color


# Change thresholds
params.minThreshold = 0;
params.maxThreshold = 255;
 
# Filter by Area.
params.filterByArea = True
params.minArea = 50
params.maxArea = 400
# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0
# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0
 
# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0
 
# Create a detector with the parameters
ver = (cv2.__version__).split('.')
if int(ver[0]) < 3 :
    detector = cv2.SimpleBlobDetector(params)
else : 
    detector = cv2.SimpleBlobDetector_create(params)