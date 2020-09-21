import cv2
import face_recognition


class DetectFaces:
    def __init__(self, image_path, cascade_path=None):
        self.cascade_path = cascade_path
        self.image_path = image_path

    # read an image from the given path and return the image
    def read_image(self):
        return cv2.imread(self.image_path)

    # read image in gray mode
    def read_image_in_gray(self):
        return cv2.imread(self.image_path, 0)

    # change the image to gray scale and return the resulting image
    def convert_image_to_gray_scale(self):
        return cv2.cvtColor(self.read_image(), cv2.COLOR_BGR2GRAY)

    # detect the faces in the image using Haar Cascade Classifier
    def detect_faces_using_Haar_Cascade_Classifier(self):
        faces = cv2.CascadeClassifier(self.cascade_path).detectMultiScale(
            self.convert_image_to_gray_scale(),
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        return faces

    # detect the faces in an image using face_recognition module
    def face_locations(self):
        try:
            image = face_recognition.load_image_file(self.image_path)
            _face_locations = face_recognition.face_locations(image)
            return _face_locations
        except FileNotFoundError as fnf_exception:
            print(fnf_exception)

    # find face landmarks on each face
    def face_landmarks(self):
        try:
            image = face_recognition.load_image_file(self.image_path)
            _face_landmarks = face_recognition.face_landmarks(image)
            return _face_landmarks

        except FileNotFoundError as fnf_exception:
            print(fnf_exception)

    # detect if there are faces in the image
    def detect_faces_using_face_recognition(self):
        if len(self.face_locations()) != 0:
            return self.face_locations()

    # list of functions implementing different algorithms in classifying images
    def detected_faces_methods_list(self):
        return [self.detect_faces_using_Haar_Cascade_Classifier(),
                self.detect_faces_using_face_recognition()]

    # find the number of faces in an image
    def number_of_faces_found(self, index):
        return len(self.detected_faces_methods_list()[index])

    # detect if there is some face in an image
    def found_faces(self):
        if len(self.face_locations()) != 0 or len(self.detect_faces_using_Haar_Cascade_Classifier()) != 0:
            return True
        else:
            return False

    def print_number_of_faces_detected(self, index):
        print(f'There were {self.number_of_faces_found(index)} faces found!')


