import functions

image = 'Seite1.jpg'
reference = 'template.jpg'
width = 20
path = 'cropped'

functions.blob_detection(image, width,path)
functions.colordifference(reference,path)