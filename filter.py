import cv2
import numpy as np


class Filter2D:
    def __init__(self):
        self.kf = None
        self.reset()

    def reset(self):
        self.kf = cv2.KalmanFilter(4, 2, 0)
        self.kf.measurementMatrix = np.array([[1, 0, 0, 0],
                                             [0, 1, 0, 0]], np.float32)

        self.kf.transitionMatrix = np.array([[1, 0, 1, 0],
                                            [0, 1, 0, 1],
                                            [0, 0, 1, 0],
                                            [0, 0, 0, 1]], np.float32)

        self.kf.processNoiseCov = np.array([[1, 0, 0, 0],
                                           [0, 1, 0, 0],
                                           [0, 0, 1, 0],
                                           [0, 0, 0, 1]], np.float32) * 0.01

        self.measurement = np.array((2, 1), np.float32)
        self.prediction = np.zeros((2, 1), np.float32)

    def update(self, point):
        measured = np.array([[np.float32(point[0])], [np.float32(point[1])]])
        self.kf.correct(measured)
        prediction = self.kf.predict()
        out = (prediction[0], prediction[1])
        return out
