#!/usr/bin/python
import os


def get_image_list():
 path_to_data = "PATH_TO_DATA"

 extensions = ['JPG', 'BMP', 'GIF', 'PNG']

 image_list = []
 for i in os.listdir(path_to_data):
  image_path = os.path.join(path_to_data, i)
  ext = image_path.split('.')[::-1][0].upper()
  if ext in extensions:
   image_list.append(image_path)

 return sorted(image_list)
