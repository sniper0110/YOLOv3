import cv2
import os
import shutil
import numpy as np
import tensorflow as tf
from core.config import cfg
import core.utils as utils
import argparse


if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--path_to_image', help='Path to the image that you want to use for inference')
    parser.add_argument('--confidence_score', type=float, default=0.7)
    parser.add_argument('--iou', type=float, default=0.5)
    args = parser.parse_args()

    INPUT_SIZE = cfg.TEST.INPUT_SIZE
    SCORE_THRESHOLD = args.confidence_score
    IOU_THRESHOLD = args.iou

    path_to_image  = args.path_to_image
    model = tf.keras.models.load_model('SavedModel/YOLOv3_model')

    image = cv2.imread(path_to_image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_size = image.shape[:2]
    image_data = utils.image_preporcess(np.copy(image), [INPUT_SIZE, INPUT_SIZE])
    image_data = image_data[np.newaxis, ...].astype(np.float32) # (1, width, height, 3)

    pred_bbox = model.predict(image_data)
    pred_bbox = [tf.reshape(x, (-1, tf.shape(x)[-1])) for x in pred_bbox]
    pred_bbox = tf.concat(pred_bbox, axis=0)
    bboxes = utils.postprocess_boxes(pred_bbox, image_size, INPUT_SIZE, SCORE_THRESHOLD)
    bboxes = utils.nms(bboxes, IOU_THRESHOLD, method='nms')

    image_with_detections = utils.draw_bbox(image, bboxes)
    image_with_detections = cv2.cvtColor(image_with_detections, cv2.COLOR_RGB2BGR)
    print('image_size = ', image_size)

    # If image size is too big then resize the image for display purposes
    display_shape = (image_size[1], image_size[0])
    if image_size[0] > 1500 or image_size[1] > 1500:
        display_shape = (int(image_size[1]/4), int(image_size[0]/4))

    image_with_detections = cv2.resize(image_with_detections, display_shape)

    cv2.imshow('detections', image_with_detections)
    cv2.waitKey(0)

    #model.summary()