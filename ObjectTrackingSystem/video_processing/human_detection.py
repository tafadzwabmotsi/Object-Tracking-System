__author__ = "Tafadzwa Brian Motsi"

import cv2
import numpy as np
import time
import datetime
import xlsxwriter

from human_tracking_analyzer.human_tracking_analyzer import HumanTrackingAnalyzer


# noinspection DuplicatedCode
def get_date_time():
    __date__ = datetime.datetime.now()
    hour = str(__date__.hour)
    minute = str(__date__.minute)
    second = str(__date__.second)

    day = str(datetime.date(day=__date__.day, month=__date__.month, year=__date__.year).strftime('%A %d %B %Y'))

    return day, hour, minute, second


# noinspection DuplicatedCode
class HumanDetection:
    def __init__(self, weights_path, config_path, coco_names_path, video_path):
        self.weights_path = weights_path
        self.config_path = config_path
        self.coco_names_path = coco_names_path
        self.video_path = video_path

        # load the network
        self.network = cv2.dnn.readNet(self.weights_path, self.config_path)

        # analyze human walking, create workbook
        self.workbook = xlsxwriter.Workbook('../analysis_output/analysis.xlsx')
        self.worksheet = self.workbook.add_worksheet('Analysis')

        self.numbers_of_people_detected_list = []
        self.times_of_detection_list = []

    def get_classes_names_colors_output_layers(self):
        try:
            classes = ['person']
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

        while True:
            ret, frame = capture.read()
            frame_id += 1

            self.draw_boxes_on_detected_objects(frame)

            elapsed_time = time.time() - starting_time
            fps = frame_id / elapsed_time
            cv2.putText(frame, "Frames/second: " + str(round(fps, 2)),
                        (10, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 4, (255, 0, 0), 4)

            cv2.imshow("Frame", frame)

            if cv2.waitKey(0) & 0xFF == ord('q'):
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

                if confidence > 0.8:
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

        self.numbers_of_people_detected_list.append(len(indexes))
        self.times_of_detection_list.append(get_date_time())

        # print(self.numbers_of_people_detected_list)

        # detection_time = get_date_time()[0] + ' @ ' + get_date_time()[1] + ':' + get_date_time()[2] + ':' + get_date_time()[3]

        # print("System detected ", len(indexes), " people on ", detection_time)
        # HumanTrackingAnalyzer('System detected ', len(indexes), ' people on ', detection_time, self.worksheet)

        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = 'person'
                confidence = confidences[i]
                color = (255, 255, 255)

                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label + " " + str(round(confidence, 2)),
                            (x, y + 30), cv2.FONT_HERSHEY_PLAIN, 3, color, 3)

    # get the numbers of people detected through the entire video
    def get_numbers_of_people_detected(self):
        return self.numbers_of_people_detected_list

    # get the times of detection
    def get_times_of_detection(self):
        return self.times_of_detection_list
