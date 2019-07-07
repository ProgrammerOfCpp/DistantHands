import dlib
import math
import numpy as np
import cv2


def to_dlib(rect):
    new_rect = dlib.rectangle(
        int(rect[0]),
        int(rect[1]),
        int(rect[2]),
        int(rect[3]))
    return new_rect


def from_dlib(rect):
    new_rect = [
        float(rect.left()),
        float(rect.top()),
        float(rect.right()),
        float(rect.bottom())]
    return new_rect


def to_relative(rect, shape):
    new_rect = [
        rect[0] / shape[1],
        rect[1] / shape[0],
        rect[2] / shape[1],
        rect[3] / shape[0]]
    return new_rect


def from_relative(rect, shape):
    new_rect = [
        rect[0] * shape[1],
        rect[1] * shape[0],
        rect[2] * shape[1],
        rect[3] * shape[0]]
    return new_rect


def submat(frame, rect):
    mat = frame[int(rect[1]):int(rect[3]), int(rect[0]):int(rect[2])]
    return mat


def fit_rect(rect, shape):
    new_rect = [
        max(0, rect[0]),
        max(0, rect[1]),
        min(shape[1], rect[2]),
        min(shape[0], rect[3])]
    return new_rect


def to_square(rect, minimize=True):
    x = rect[0]
    y = rect[1]
    w = rect[2]-x
    h = rect[3]-y

    d = abs(w-h)

    if minimize:
        if w > h:
            w = h
            x += d/2
        else:
            h = w
            y += d/2
    else:
        if w > h:
            h = w
            y -= d/2
        else:
            w = h
            x -= d/2

    new_rect = [x, y, x+w, y+h]
    return new_rect


def scale(rect, scale_factor):
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y

    nw = w * scale_factor
    nh = h * scale_factor
    nx = x + (w - nw) / 2
    ny = y + (h - nh) / 2

    new_rect = [nx, ny, nw+nx, ny+nh]
    return new_rect


def add_rect(rect1, rect2):
    rect = [rect1[0] + rect2[0],
            rect1[1] + rect2[1],
            rect1[2] + rect2[0],
            rect1[3] + rect2[1]]
    return rect


def rect_center(rect):
    center = [float(rect[0]+rect[2])/2, float(rect[1]+rect[3])/2]
    return center


def vec_len(vec):
    return math.sqrt(vec[0]*vec[0] + vec[1]*vec[1])


def difference(img1, img2, color_mode=False):
    if color_mode:
        def get_dominant_color(img):
            color = []
            for c in img.shape[2]:
                avg = np.mean(img[:, :, c])
                color.append(avg)
            return color

        c1 = get_dominant_color(img1)
        c2 = get_dominant_color(img2)
        diff = 0
        for c in range(0, 3):
            diff += abs(c2[c] - c1[c])
        diff /= img1.size
        return diff
    else:
        res = cv2.matchTemplate(img1, img2, cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        return min_val
		

def are_different_locations(rect1, rect2):
    if rect1 is None or rect2 is None:
        return False
    side1 = min(rect1[2] - rect1[0], rect1[3] - rect1[1])
    side2 = min(rect2[2] - rect2[0], rect2[3] - rect2[1])
    if side1 > side2:
        side1, side2 = side2, side1
    if side2 / side1 > 2:
        return True
    c1 = rect_center(rect1)
    c2 = rect_center(rect2)
    dist = vec_len([c2[0]-c1[0], c2[1]-c1[1]])
    if dist / side2 > 0.5:
        return True
    return False
