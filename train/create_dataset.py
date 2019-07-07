from os.path import *
from os import listdir
from os import makedirs
import numpy as np
import argparse
import cv2
import time
import random
import math

root = dirname(abspath(__file__)) + "\\"
categories = ["open","close"]
batch_ratio = 5
	
def main():
	file_index = int(time.time())

	n = 0
	cap = cv2.VideoCapture(0)
	frames_passed = 0
	
	while True:
		ret, frame = cap.read()
		frame = cv2.flip(frame, 1)
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		frame = cv2.equalizeHist(frame)
			
		cv2.imshow("Frame", frame)
		frames_passed += 1
		
		key = cv2.waitKey(1)
		if (key == 27):
			break
		if (key == 49) or (frames_passed == 60):
			cv2.imwrite('images/' + str(file_index) + '.jpg', frame)
			frames_passed = 0
			
			file_index += 1
main()
