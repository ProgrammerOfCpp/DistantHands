import cv2
import util
import consts
import win32api
import win32con
from filter import Filter2D
from hand_tracker import HandTracker


class CursorController:
    def __init__(self, options):
        self.options = options
        self.hand_tracker = HandTracker(self.options)
        self.filter = Filter2D()
        self.hand_prev = None
        self.idle_frames = 0

    def update(self, frame):
        screen = (
            win32api.GetSystemMetrics(1),
            win32api.GetSystemMetrics(0))
        hand_rect = self.hand_tracker.get_hand_rect(frame)
        if hand_rect is not None:
            cv2.rectangle(frame, (int(hand_rect[0]), int(hand_rect[1])), (int(hand_rect[2]), int(hand_rect[3])), (0, 255, 0))
            hand = util.to_relative(hand_rect, frame.shape)
            pos = util.rect_center(hand)
            if self.hand_prev is not None:
                pos_prev = util.rect_center(self.hand_prev)
                delta = [
                    pos[0] - pos_prev[0],
                    pos[1] - pos_prev[1]]
                delta = self.filter.update(delta)
                v0 = util.vec_len(delta)
                if v0 < self.options[consts.vmin]:
                    v = v0*v0/self.options[consts.vmin]
                elif v0 > self.options[consts.vmax]:
                    v = v0*v0/self.options[consts.vmax]
                else:
                    v = v0
                if v < self.options[consts.vidle]:
                    self.idle_frames += 1
                    if self.idle_frames == self.options[consts.idle_frames]:
                        cursor = win32api.GetCursorPos()
                        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, cursor[0], cursor[1], 0, 0)
                        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, cursor[0], cursor[1], 0, 0)
                        self.idle_frames = 0
                else:
                    self.idle_frames = 0
                if v0 > 0:
                    depth_k = self.options[consts.depth_ratio] / (hand[3] - hand[1])
                    sensetivity_x = self.options[consts.sensetivity_x] * depth_k
                    sensetivity_y = self.options[consts.sensetivity_y] * depth_k
                    offset = (
                        float(screen[1]) * delta[0] / v0 * v * sensetivity_x,
                        float(screen[0]) * delta[1] / v0 * v * sensetivity_y
                    )
                    cursor0 = win32api.GetCursorPos()
                    cursor = (
                        cursor0[0] + offset[0],
                        cursor0[1] + offset[1],
                    )
                    win32api.SetCursorPos((int(cursor[0] + 0.5), int(cursor[1] + 0.5)))
                self.hand_prev = hand
            else:
                kx = 1.0
                ky = 1.0
                cursor_rel = [
                    0.5 + (pos[1] - 0.5) * ky,
                    0.5 + (pos[0] - 0.5) * kx
                ]
                cursor = (
                    int(float(screen[1]) * cursor_rel[0] + 0.5),
                    int(float(screen[0]) * cursor_rel[1] + 0.5)
                )
                win32api.SetCursorPos(cursor)
                self.hand_prev = hand
                self.filter.reset()
        else:
            self.hand_prev = None
