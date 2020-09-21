__author__ = "Tafadzwa Brian Motsi"

import cv2
import numpy as np
import time


class ObjectDetection:
    def __init__(self, weights_path, config_path, coco_names_path, video_path):
        self.weights_path = weights_path
        self.config_path = config_path
        self.coco_names_path = coco_names_path
        self.video_path = video_path

        # load the network
        self.network = cv2.dnn.readNet(self.weights_path, self.config_path)

    def get_classes_names_colors_output_layers(self):
        try:
            with open(self.coco_names_path, 'r') as f:
                classes = [line.strip() for line in f.readlines()]

            layer_names = self.network.getLayerNames()
            output_layers = [layer_names[i[0] - 1] for i in self.network.getUnconnectedOutLayers()]
            colors = np.random.uniform(0, 255, size=(len(classes), 3))

            return classes, layer_names, colors, output_layers

        except ...:
            return None

    def object_detection_objects_using_yolo(self):
        capture = cv2.VideoCapture(self.video_path if self.video_path else 0)

        starting_time = time.time()
        frame_id = 0

        while capture.isOpened():
            ret, frame = capture.read()
            frame_id += 1

            self.draw_boxes_on_detected_objects(frame)

            elapsed_time = time.time() - starting_time
            fps = frame_id / elapsed_time
            cv2.putText(frame, "FPS: " + str(round(fps, 2)),
                        (10, 50), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 3)

            cv2.imshow("Image", frame)
            key = cv2.waitKey(1)
            if key == 27:
                break

        capture.release()
        cv2.destroyAllWindows()

    def detect_objects(self, frame):
        self.network.setInput(cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False))
        return self.network.forward(self.get_classes_names_colors_output_layers()[-1])

    def get_class_ids_confidences_boxes(self, frame):
        height, width, channels = frame.shape

        class_ids = list()
        confidences = list()
        boxes = list()

        outs = self.detect_objects(frame)
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > 0.1:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        return class_ids, confidences, boxes

    def draw_boxes_on_detected_objects(self, frame):

        class_ids, confidences, boxes = self.get_class_ids_confidences_boxes(frame)
        classes, _, colors, _ = self.get_classes_names_colors_output_layers()

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.8, 0.3)

        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                confidence = confidences[i]
                color = colors[class_ids[i]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label + " " + str(round(confidence, 2)),
                            (x, y + 30), cv2.FONT_HERSHEY_PLAIN, 3, color, 3)
