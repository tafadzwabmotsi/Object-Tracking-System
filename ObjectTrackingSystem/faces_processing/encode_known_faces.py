from .encode_faces_methods import *
import os


class EncodeKnownFaces:
    def __init__(self, path_of_known_faces):
        self.path_of_known_faces = path_of_known_faces

    # encode all the faces within images that we claim to be known
    def encode_known_faces(self):
        encoded_labelled_faces = dict()
        path = self.path_of_known_faces
        ext = '/'

        # traverse through the tree from the given root directory
        for root, directories, files in os.walk(path, topdown=True):
            for file in files:
                if str(file).endswith('.jpg') or str(file).endswith('.png'):
                    encoded_labelled_faces[str(file).split('.')[0]] = one_face_encodings(path+ext+str(file))

        return encoded_labelled_faces

