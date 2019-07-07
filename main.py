import cv2
import json
from cursor_controller import CursorController


class Application:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        with open("options.json", "r") as f:
            self.options = json.load(f)
        self.cursor_controller = CursorController(self.options)

    def __del__(self):
        with open("options.json", "w") as f:
            json.dump(self.options, f)
        print("Application was terminated.")

    def run(self):
        ret, frame = self.cap.read()
        PADDING = 0
        frame = frame[PADDING:frame.shape[0] - PADDING - 1, 0:frame.shape[1] - 1]
        frame = cv2.flip(frame, 1)
        try:
            self.cursor_controller.update(frame)
        except Exception as e:
            print(e)
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if key == 27:
            return False
        return True


def main():
    app = Application()
    while app.run():
        continue


if __name__ == '__main__':
    main()
