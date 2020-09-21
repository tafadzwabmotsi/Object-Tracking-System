import cv2


class DisplayVideo:
    def __init__(self, window_name, frame):
        self.window_name = window_name
        self.frame = frame

        self.display_video()

    def display_video(self):
        cv2.imshow(self.window_name, self.frame)
