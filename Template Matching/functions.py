import cv2
import numpy as np
import os
import shutil
from colorthief import ColorThief
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

def template_matching(image,template,path,threshold,coordinates):
	print 100*'#'
	print 'starting process'
	print 'starting part 1'
	print 100*'#'
	img_rgb = cv2.imread(image)
	img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
	template = cv2.imread(template,0)
	w, h = template.shape[::-1]

	text_file = open(coordinates, "w")

	res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
	loc = np.where( res >= threshold)

	match_indices = np.arange(res.size)[(res>threshold).flatten()]
	coordinates = zip(np.unravel_index(match_indices,res.shape)[0],np.unravel_index(match_indices,res.shape)[1])

	print 'saving coordinates'

	for i in coordinates:
		text_file.write(str(i))
		text_file.write("\n")


	for pt in zip(*loc[::-1]):
	    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
	    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
	    top_left = max_loc
	    bottom_right = (top_left[0] + w, top_left[1] + h)


	print "Saving image now"

	cv2.imwrite(image+"_"+str(threshold)+"_template_match.jpg",img_rgb)

	print "done with part one"


def move_images(image,template,coordinates_txt,path_in,path_out):
	print 100*'#'
	print 'starting part two'
	print 100*'#'

	img_rgb = cv2.imread(image)
	template = cv2.imread(template,0)
	w, h = template.shape[::-1]

	with open(coordinates_txt) as f:
	    coordinates_fake = f.readlines()

	coordinates_fake = [x.strip() for x in coordinates_fake] 
	coordinates = []
	for i in coordinates_fake:
		i = i[1:-1]
		i = i.split(',')
		i = [int(x) for x in i]
		i = tuple(i)
		coordinates.append(i)

		if not os.path.exists(path_in):
			os.makedirs(path_in)

	 	crop_img = img_rgb[i[0]-w:i[0]+w,i[1]-h:i[1]+h]
	 	cv2.imwrite(path_in+"/"+str(i[0])+'_'+str(i[1])+"_cropped.jpg",crop_img)

	output = []
	for i in coordinates:
		output.append(i)

	for w in range(len(coordinates)):
		if w >= len(output):
			break
		else:
			x = output[w]
			for i in coordinates:
				if abs(x[0] - i[0]) < 10:
					if abs(x[1] - i[1]) < 10:
						if i in output:
							output.remove(i)
			output.append(x)

	if not os.path.exists(path_out):
		os.makedirs(path_out)

	print 'saving images'

	for i in output:
		shutil.move(path_in+'/'+str(i[0])+'_'+str(i[1])+'_cropped.jpg',path_out)

	print 'done with part two'


def expandtuple(a,b,c):
	return a,b,c

def color_difference(template,path,output_filenames,output_comparison,check_txt):
	print 100*'#'
	print 'starting part three'
	print 100*'#'
	color_thief = ColorThief(template)
	palette = color_thief.get_palette(color_count=5, quality=1)
	a,b,c=expandtuple(*min(palette))
	template_rgb = sRGBColor(a,b,c)
	template_lab = convert_color(template_rgb,LabColor)
	filenames = []
	comparison = []
	for filename in os.listdir(path):
		if filename.endswith(".jpg"):
			filenames.append(str(filename))

	print 'comparing color differences'
	text_file_2 = open(check_txt,'w')
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

	print 'saving filenames'
	text_file = open(output_filenames, "w")
	for i in filenames:
		text_file.write(str(i))
		text_file.write("\n")

	print 'saving color comparison'

	text_file_1 = open(output_comparison, "w")
	for i in comparison:
		text_file_1.write(str(i))
		text_file_1.write("\n")

	print 'done with part two'
	print 'done with process'
	print 100*'#'