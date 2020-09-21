__author__ = "Tafadzwa Brian Motsi"

import mysql.connector


# noinspection SqlNoDataSourceInspection
class DetectedFacesDatabaseOperations:
    def __init__(self, classification_value,  path_to_faces, detection_time):
        self.database = mysql.connector.connect(
            user='tafadzwa',
            password='tafadzwapass',
            host='localhost',
            database='obts'
        )

        self.path_to_faces = path_to_faces
        self.classification_value = classification_value
        self.detection_time = detection_time

    # check if the unknown faces table exists
    def is_unkown_faces_table_existing(self):
        cursor = self.database.cursor()
        cursor.execute("SHOW TABLES LIKE 'unknown_faces'")

        if cursor.fetchone():
            return True
        else:
            return False

    # create the unknown_faces table
    def create_unknown_faces_table(self):
        self.database.cursor().execute("CREATE TABLE unknown_faces(id INT AUTO_INCREMENT PRIMARY KEY, classification VARCHAR(50), faces_path VARCHAR(255), detection_time VARCHAR(50))")

    def insert_image_into_the_database(self):
        try:
            cursor = self.database.cursor()

            add_unknown_face = "INSERT INTO obts.unknown_faces (classification, faces_path, detection_time) VALUES (%s, %s, %s)"

            if len(self.get_unknown_faces_table()) != 0:
                paths_list = [row[2] for row in self.get_unknown_faces_table()]

                if self.path_to_faces not in paths_list:

                    add_unknown_face_value = (self.classification_value, self.path_to_faces, self.detection_time)
                    cursor.execute(add_unknown_face, add_unknown_face_value)
                    self.database.commit()

                    print("Case 1: Record added successfully...")

            else:
                add_unknown_face_value = (self.classification_value, self.path_to_faces, self.detection_time)
                cursor.execute(add_unknown_face, add_unknown_face_value)
                self.database.commit()

                print("Case 2: Record added successfully...")

            cursor.close()

        except mysql.connector.errors.ProgrammingError:
            if not self.is_unkown_faces_table_existing():
                self.create_unknown_faces_table()

            self.insert_image_into_the_database()

    # get data from unknown_faces table
    def get_unknown_faces_table(self):
        cursor = self.database.cursor()
        cursor.execute("SELECT * FROM unknown_faces")

        return cursor.fetchall()


