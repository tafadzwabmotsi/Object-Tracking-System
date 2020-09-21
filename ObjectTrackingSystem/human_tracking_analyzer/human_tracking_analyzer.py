# noinspection SpellCheckingInspection
class HumanTrackingAnalyzer:
    def __init__(
            self,
            system_title,
            number_of_people_detected,
            people_title,
            detection_date_and_time,
            worksheet):

        self.system_title = system_title
        self.number_of_people_detected = number_of_people_detected
        self.people_title = people_title
        self.detection_date_and_time = detection_date_and_time
        self.worksheet = worksheet

    def create_analysis_file(self, row_index):
        self.worksheet.write(row_index, 0, self.system_title)
        self.worksheet.write(row_index, 1, self.number_of_people_detected)
        self.worksheet.write(row_index, 2, self.people_title)
        self.worksheet.write(row_index, 3, self.detection_date_and_time)