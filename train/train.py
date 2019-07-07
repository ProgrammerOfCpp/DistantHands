import os
import sys
import glob
from os.path import *

import dlib

DETECTOR_FILENAME = "detector_working.svm"
TRAINING_FILENAME = "train.xml"

root = dirname(abspath(__file__)) + "\\"
faces_folder = root + ""

options = dlib.simple_object_detector_training_options()
options.detection_window_size = 2000
options.add_left_right_image_flips = True
options.C = 5
options.num_threads = 4
options.be_verbose = True


training_xml_path = os.path.join(faces_folder, TRAINING_FILENAME)
dlib.train_simple_object_detector(training_xml_path, DETECTOR_FILENAME, options)

detector = dlib.simple_object_detector(DETECTOR_FILENAME)
win_det = dlib.image_window()
win_det.set_image(detector)
dlib.hit_enter_to_continue()