from os.path import *
from os import listdir
from os import makedirs
import numpy as np
import argparse
import cv2
import time
import random
import math
import dlib

root = dirname(abspath(__file__)) + "\\"
cap = cv2.VideoCapture(0)
detector = dlib.fhog_object_detector(root + "detector_working.svm")
win_det = dlib.image_window()
win_det.set_image(detector)
dlib.hit_enter_to_continue()
	
def main():
	while True:
		ret, frame = cap.read()
		frame = cv2.flip(frame, 1)
		#frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		#frame = cv2.equalizeHist(frame)

		dets, scores, idx = detector.run(frame, 1, -1)
		for i, d in enumerate(dets):
			x1 = d.left()
			y1 = d.top()
			x2 = d.right()
			y2 = d.bottom()
			cv2.rectangle(frame, (x1, y1), (x2, y2), color=(0, 255, 0))
		
		cv2.imshow("Frame", frame)
		
		key = cv2.waitKey(1)
		if key == 27:
			break

main()
