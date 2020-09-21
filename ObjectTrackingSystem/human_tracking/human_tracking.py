from __future__ import absolute_import, division, print_function, unicode_literals

__author__ = "Tafadzwa Brian Motsi"

import cv2
from image_processing.image_processing import ImageProcessing as ImgP
from video_processing.human_detection import HumanDetection
import datetime


# noinspection DuplicatedCode
class HumanTracking:
    def __init__(
            self,
            yolov3_weights,
            yolov3_config,
            yolov3_coco_names,
            image_path,
            video_path,
            yolo_tiny_videos_model_path=None,
            video_output_path=None,
    ):

        # get processed image with detected objects
        self.processed_image = ImgP(yolov3_weights, yolov3_config, yolov3_coco_names, image_path)
        self.human_detection = HumanDetection(yolov3_weights, yolov3_config, yolov3_coco_names, video_path)

        # get the labels from yolov3 coco names
        self.labels = self.processed_image.labels

        # get the video path
        self.video_path = video_path

        # get the yolo tiny videos model path
        self.yolo_tiny_videos_model_path = yolo_tiny_videos_model_path

        # get the video output path
        self.video_output_path = video_output_path

    @staticmethod
    # draw rectangle around an object
    def draw_rectangle_around_object(image, xy_coordinate_1, xy_coordinate_2, rbg_color, thickness):
        x_1, y_1 = xy_coordinate_1
        x_2, y_2 = xy_coordinate_2

        red, blue, green = rbg_color

        cv2.rectangle(
            img=image,
            pt1=(x_1, y_1),
            pt2=(x_2, y_2),
            color=(red, blue, green),
            thickness=thickness
        )

    # track human in a video
    def track_human(self):
        if 'person' in self.labels:
            try:
                self.human_detection.object_detection_objects_using_yolo()
            except Exception as e:
                pass
