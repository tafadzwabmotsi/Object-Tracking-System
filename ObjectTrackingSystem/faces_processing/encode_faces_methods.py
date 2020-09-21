import face_recognition
import imutils

# find face encodings of a face in one image
def one_face_encodings(image_path):
    try:
        image = face_recognition.load_image_file(image_path)
        _face_encodings = face_recognition.face_encodings(image)[0]
        return _face_encodings
    except FileNotFoundError as fnf_exception:
        print(fnf_exception)


# find face encodings on each face
def multiple_face_encodings(image_path):
    try:
        image = face_recognition.load_image_file(image_path)
        _face_encodings = face_recognition.face_encodings(image)
        return _face_encodings
    except FileNotFoundError as fnf_exception:
        print(fnf_exception)