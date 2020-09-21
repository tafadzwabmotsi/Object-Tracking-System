__author__ = "Tafadzwa Brian Motsi"

import cv2
import numpy as np


# noinspection DuplicatedCode
class ImageProcessing:
    def __init__(self, weights_path, config_path, coco_names_path, image_path):
        self.weights_path = weights_path
        self.config_path = config_path
        self.coco_names_path = coco_names_path
        self.image_path = image_path

        self.network = self.yolov3_network()
        self.image = self.read_image()[0]
        self.labels, self.processed_image = self.label_objects_get_image()

    # read and return the yolov3 network
    def yolov3_network(self):
        return cv2.dnn.readNet(self.weights_path, self.config_path)

    # read the coco names and return a list of names
    def yolov3_objects_names(self):
        with open(self.coco_names_path, 'r') as f:
            coco_names = [line.strip() for line in f.readlines()]
        return coco_names

    # get the yolov3 output layers
    def output_layers(self):
        return [self.network.getLayerNames()[i[0] - 1]
                for i in self.network.getUnconnectedOutLayers()]

    # load image and return the image, height, width, and channels
    def read_image(self):
        image = cv2.imread(self.image_path)
        image = cv2.resize(image, None, fx=1, fy=1)
        height, width, channels = image.shape

        return [image, height, width, channels]

    # find the outputs of the image
    def outputs(self):
        blob = cv2.dnn.blobFromImage(self.image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.network.setInput(blob)
        _outputs = self.network.forward(self.output_layers())

        return _outputs

    # find the class ids, confidences, and boxes of detection
    def class_ids_confidences_boxes(self):
        class_ids = list()
        confidences = list()
        boxes = list()

        for detections in self.outputs():
            for detection in detections:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > 0.5:  # object detected

                    width = self.read_image()[2]
                    height = self.read_image()[1]

                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)

                    _w = int(detection[2] * width)
                    _h = int(detection[3] * height)

                    _x = int(center_x - _w/2)
                    _y = int(center_y - _h/2)

                    boxes.append([_x, _y, _w, _h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        return [class_ids, confidences, boxes]

    # get the number of boxes detected
    def number_of_boxes_detected(self):
        return len(self.class_ids_confidences_boxes()[-1])

    # label the detected objects
    def label_objects_get_image(self):
        ccb = self.class_ids_confidences_boxes()
        boxes = ccb[-1]
        confidences = ccb[1]
        class_ids = ccb[0]

        classes = self.yolov3_objects_names()

        labels = []

        for index in range(self.number_of_boxes_detected()):
            if index in cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4):
                __x__, __y__, __w__, __h__ = boxes[index]
                label = str(classes[int(class_ids[index])])

                if label == 'person':
                    labels.append(label)

                cv2.rectangle(self.image, (__x__, __y__), (__x__ + __w__, __y__ + __h__), (0, 255, 0), 2)
                cv2.putText(self.image, label, (__x__, __y__), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)

        return labels, self.image

    # display image
    def display_image(self):
        cv2.imshow('Image', self.processed_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()





