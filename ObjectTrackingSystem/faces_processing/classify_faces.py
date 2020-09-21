__author__ = "Tafadzwa Brian Motsi"

from detected_faces_database_operations.detected_faces_database_operations import DetectedFacesDatabaseOperations
from faces_processing.encode_faces_methods import *
from faces_processing.detect_faces import DetectFaces
from notifications_handler.emailing_handler import EmailingHandler
import face_recognition
import cv2
import numpy as np
import imghdr
import os
import datetime
from paths.paths import *
import random


# noinspection PyCompatibility,PyUnusedLocal,DuplicatedCode
class ClassifyFaces:
    def __init__(self, known_faces_path, unknown_faces_path):
        self.known_faces_path = known_faces_path
        self.unknown_faces_path = unknown_faces_path

        self.multiple_face_encodings = multiple_face_encodings(self.unknown_faces_path)

        self.detected_faces = DetectFaces(self.unknown_faces_path)
        self.faces_locations = self.detected_faces.face_locations()

    # label faces
    def label_faces(self, img_path, classification_list, time):
        marked = False
        image = cv2.imread(img_path)

        for face_location in self.faces_locations:
            x_1, y_1, x_2, y_2 = face_location
            pt1 = (x_1-30, y_1+20)
            pt2 = (x_2-30, y_2+20)
            color = (255, 255, 0)

            cv2.rectangle(image, pt1, pt2, color, 2)
            for classification in classification_list:
                bool_value, label = classification

                if bool_value:
                    cv2.putText(image, label, (x_1-50, y_2+20), cv2.FONT_HERSHEY_PLAIN, 2, color, 2,  cv2.LINE_AA)

                else:
                    cv2.putText(image, "{0}".format("unknown"), (x_1-50, y_2+20), cv2.FONT_HERSHEY_PLAIN, 2, color, 2,  cv2.LINE_AA)

        image_name = str(img_path).split('/')[-1]

        cv2.putText(image, time, (10, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow("Image window", image)
        cv2.imwrite(str(unknown_faces_detected_path)+str("x{0}".format(image_name)), image)
        cv2.waitKey(0)

    # compare known face and unknown ones in one image
    def compare_known_unknown_faces(self):

        __date__ = datetime.datetime.now()
        hour = str(__date__.hour)
        minute = str(__date__.minute)
        second = str(__date__.second)

        day = str(datetime.date(day=__date__.day, month=__date__.month, year=__date__.year).strftime(
            '%A %d %B %Y'))

        path_to_faces = str(os.path.abspath(str(self.unknown_faces_path).split('/')[-1]))
        detection_time = day + '; ' + hour + ':' + minute + ':' + second

        ext = '/'
        match_faces_list = list()

        for root, directories, files in os.walk(self.known_faces_path, topdown=True):
            for file in files:
                if file.endswith('.jpg') or file.endswith('.png'):
                    path_1 = self.known_faces_path + ext + file

                    for face_encoding in self.multiple_face_encodings:
                        face_comp = face_recognition.compare_faces([one_face_encodings(path_1)], face_encoding)

                        if face_comp == [True] and len(self.multiple_face_encodings) == 1:
                            match_faces_list.append((True, file.split('.')[0]))
                            self.label_faces(self.unknown_faces_path, match_faces_list, detection_time)
                            return match_faces_list

                        elif face_comp == [True]:
                            match_faces_list.append((True,  file.split('.')[0]))
                            self.multiple_face_encodings.remove(face_encoding)

                        else:
                            match_faces_list.append((False, 'Person unknown'))

        marker = False
        for match_face in match_faces_list:
            bool_value, classification_value = match_face

            if bool(bool_value):
                marker = True
                break
            else:
                pass

        if marker:
            pass

        else:

            classification = ''
            length = len(self.multiple_face_encodings)

            if len(self.multiple_face_encodings) == 1:
                classification = classification.join([str(length), ' unknown person'])

            else:
                classification = classification.join([str(length), ' unknown persons'])

            # DetectedFacesDatabaseOperations(classification, path_to_faces, detection_time).insert_image_into_the_database()

            day_of_detection = day
            if int(hour) < 10:
                hour = str(0) + hour

            if int(minute) < 10:
                minute = str(0) + minute

            if int(second) < 10:
                second = str(0) + second

            time_of_detection = hour + ':' + minute + ':' + second

            subject = 'Intruder Found'
            body_content = f'Be notified that there is an intruder found on {day_of_detection} at ' \
                           f'{time_of_detection}. Find the image attached for details'

            # EmailingHandler('obtsdevelopment@gmail.com', self.unknown_faces_path).send_email(subject, body_content)

        self.label_faces(self.unknown_faces_path, match_faces_list, detection_time)

        return match_faces_list
