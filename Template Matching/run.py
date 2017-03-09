import functions

image = 'damage.jpg'
template = 'template.jpg'
threshold = 0.8
cropped_images_path = 'cropped'
selected_cropped_images_path = 'cropped_2'
save_coordinates = 'coordinates.txt'
save_filenames = 'filenames.txt'
save_comparison = 'comparison.txt'
save_check = 'check.txt'


functions.template_matching(image,template,cropped_images_path,threshold,save_coordinates)
functions.move_images(image,template,save_coordinates,cropped_images_path,selected_cropped_images_path)
functions.color_difference(template,selected_cropped_images_path,save_filenames,save_comparison,save_check)
