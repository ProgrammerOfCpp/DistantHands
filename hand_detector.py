import sys
import dlib
import util
import cv2
import consts


class HandDetector:
    def __init__(self, options):
        self.options = options
        self.detector = dlib.fhog_object_detector("assets/hand_detector.svm")

    def predict(self, frame, detector, threshold):
        detections, scores, idx = detector.run(frame, 1, -1)

        best_score = 0
        best_rect = None
        for i, d in enumerate(detections):
            scores[i] -= threshold
            if scores[i] > best_score:
                best_rect = util.from_dlib(d)
                best_rect = util.to_relative(best_rect, frame.shape)
                best_score = scores[i]
        return best_score, best_rect
    
    def detect_hand(self, frame):
        frame = cv2.resize(frame, (self.options[consts.detection_image_width],
                                   self.options[consts.detection_image_height]))
        score, rect = self.predict(frame, self.detector, self.options[consts.detection_threshold])
        return score, rect
