import os
import pandas as pd
from copy import copy
import numpy as np
import shutil
import argparse

def parse_my_csv(path_to_csv_file):
    """
    This function reads all the annotations from the csv file and then create a dictionary
    that stores these annotations.
    The dictionary will have as a key the name of the image and as a value a list of detections.

    params:
    path_to_csv_file : the path to where your pascal annotations (should be a csv file).
    """

    df = pd.read_csv(path_to_csv_file)
    data = {}

    for i in range(len(df.index)):
        
        xmin = int(df.iloc[i]['xmin'])
        ymin = int(df.iloc[i]['ymin'])
        xmax = int(df.iloc[i]['xmax'])
        ymax = int(df.iloc[i]['ymax'])

        if df.iloc[i]['class'] == 'mask':
            object_class = 0
        else:
            object_class = 1


        if df.iloc[i]['filename'] in data.keys():
            data[df.iloc[i]['filename']].append([xmin, ymin, xmax, ymax, object_class])
        else:
            data.update({df.iloc[i]['filename'] : [[xmin, ymin, xmax, ymax, object_class]]})


    # data = {'image_name' : [[det1], [det2], ..]}
    # det1 = xmin, ymin, xmax, ymax, object_class
    return data



def modify_data(data, path_to_images, path_to_output):
    """
    This function transforms annotations from pascal format to yolo format.
    It also removes any spaces in the images names and create new images that
    have names without spaces. This is done to make things consistent with 
    the way the training and evaluation code handle reading data.

    params:
    data: a dictionary that has as a key the name of the image and as value a list of 
    detections (xmin, ymin, xmax, ymax, class).
    path_to_images: the path to where your images are stored.
    path_to_output : the path to where the generated yolo annotations and also the images
    without any spaces in their names.
    """

    path_to_save_annotations = os.path.join(path_to_output, 'annotations.txt')
    with open(path_to_save_annotations, 'a+') as f:
        

        for img_name, detections in data.items():

            # Copy and rename image
            path_to_input_img = os.path.join(path_to_images, img_name)

            name_without_spaces = img_name.replace(' ', '')
            path_to_output_img = os.path.join(path_to_output, name_without_spaces)

            shutil.copy(path_to_input_img, path_to_output_img)

            # save detections in the new annotations file
            f.write(f'{path_to_output_img} ')
            for detection in detections:
                xmin, ymin, xmax, ymax, c = detection
                f.write(f'{xmin},{ymin},{xmax},{ymax},{c} ')

            f.write('\n')

    print('Done saving annotations!')



if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--path_to_images', help="path to where your images are stored")
    parser.add_argument('--path_to_csv_annotations', help='full path to where your csv annotations file is.')
    parser.add_argument('--path_to_save_output', help='path to where the output images and annotation file will be saved')

    args = parser.parse_args()

    path_to_images = args.path_to_images 
    path_csv_file = args.path_to_csv_annotations 

    data = parse_my_csv(path_csv_file)

    output_path = args.path_to_save_output 
    if not os.path.isdir(output_path):
        os.makedirs(output_path)

    modify_data(data, path_to_images, output_path)


