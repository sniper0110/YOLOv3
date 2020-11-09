import cv2
import os
import shutil
import numpy as np
import tensorflow as tf
import core.utils as utils
from core.config import cfg
from core.yolov3 import YOLOv3, decode


if __name__=='__main__':

    INPUT_SIZE   = cfg.TEST.INPUT_SIZE
    NUM_CLASS    = len(utils.read_class_names(cfg.YOLO.CLASSES))

    # Build Model
    input_layer  = tf.keras.layers.Input([INPUT_SIZE, INPUT_SIZE, 3])
    feature_maps = YOLOv3(input_layer)

    bbox_tensors = []
    for i, fm in enumerate(feature_maps):
        bbox_tensor = decode(fm, i)
        bbox_tensors.append(bbox_tensor)

    model = tf.keras.Model(input_layer, bbox_tensors)
    model.load_weights("./yolov3")

    model.save('SavedModel/YOLOv3_model')