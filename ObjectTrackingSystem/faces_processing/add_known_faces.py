__author__ = "Tafadzwa Brian Motsi"

import shutil
import os


class AddKnownFaces:
    def __init__(self, source_path, destination_path):
        self.source_path = source_path
        self.destination_path = destination_path

    def add_new_face(self):
        ext = '/'
        for root, directories, files in os.walk(self.source_path):
            for file in files:
                if file.endswith('.jpg') or file.endswith('.png'):
                    try:
                        shutil.copyfile(self.source_path+ext+file, self.destination_path+ext+file)
                    except IOError as io_error_exception:
                        print(io_error_exception)
