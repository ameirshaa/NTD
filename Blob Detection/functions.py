import cv2
import numpy as np
import os
import blobmatchingparams
from colorthief import ColorThief
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

def blob_detection(image,width,path):
	print 100*'#'
	print 'starting process'
	print 'starting part 1'
	print 100*'#'
	img = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
	detector = cv2.SimpleBlobDetector_create(blobmatchingparams.params)
	keypoints = detector.detect(img)
	x=[]
	y=[]
	for i in range(len(keypoints)):
		x.append(keypoints[i].pt[0]) #i is the index of the blob you want to get the position
		y.append(keypoints[i].pt[1])

	z = zip(x,y)

	print len(keypoints)

	img_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	if not os.path.exists(path):
		os.makedirs(path)

	print 'saving images'

	for i in z:
		a = i[0]
		b = i[1]
		crop_img = img_with_keypoints[b-width:b+width,a-width:a+width]
		crop_img2 = img[b-width:b+width,a-width:a+width]
		cv2.imwrite(path+'/'+str(a)+'_'+str(b)+"_cropped.jpg",crop_img)
		cv2.imwrite(path+'/'+str(a)+'_'+str(b)+"_cropped2.jpg",crop_img2)

	cv2.imwrite(str(image)+'_blob_detection.jpg',img_with_keypoints)

	print 'finished with part 1'


def expandtuple(a,b,c):
	return a,b,c

def colordifference(reference,path):
	print 100*'#'
	print 'starting part 2'
	print 100*'#'
	color_thief = ColorThief(reference)
	palette = color_thief.get_palette(color_count=5, quality=1)
	a,b,c=expandtuple(*min(palette))
	template_rgb = sRGBColor(a,b,c)
	template_lab = convert_color(template_rgb,LabColor)

	filenames=[]
	for filename in os.listdir(path):
		if filename.endswith("2.jpg"):
			filenames.append(str(filename))

	comparison = []

	text_file_2 = open('check.txt','w')

	print 'computing color differences'

	for i in filenames:
		try:
			color_thief1 = ColorThief(path+'/'+i)
			palette1 = color_thief1.get_palette(color_count=5, quality=1)
			d,e,f=expandtuple(*min(palette1))
			i_rgb = sRGBColor(d,e,f)
			i_lab = convert_color(i_rgb,LabColor)
			delta_e = delta_e_cie2000(template_lab,i_lab)
			comparison.append(delta_e)
			text_file_2.write(str(i))
			text_file_2.write(' , ')
			text_file_2.write(str(delta_e))	
			text_file_2.write('\n')
		except IOError:
			comparison.append(999999)

	print 'finished with paart 2'



