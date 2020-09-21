import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QColor, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout

from human_tracking.human_tracking import HumanTracking
from image_processing.image_processing import ImageProcessing
from paths.paths import *


class TextLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        QLabel.__init__(self, parent)

    def mousePressEvent(self, ev):
        self.clicked.emit()


class Ui(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(1400, 600)
        self.setWindowTitle('Events')
        self.setWindowIcon(QIcon('web.png'))

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor('#4E6B51'))
        self.setPalette(p)

        h_box = QHBoxLayout()

        image_events_label = TextLabel("Image Events")
        video_events_label = TextLabel("Video Events")

        image_events_label.clicked.connect(self.image_events_label_click_handler)
        video_events_label.clicked.connect(self.video_events_label_click_handler)

        image_events_label.mouseMoveEvent()

        self.add_events_images(h_box, '../images/events_pics/image-events.png', image_events_label)
        self.add_events_images(h_box, '../images/events_pics/video-events.png', video_events_label)

        h_box.setAlignment(Qt.AlignCenter)
        h_box.setSpacing(200)

        self.setLayout(h_box)

        self.show()

    @staticmethod
    def image_events_label_click_handler():
        img_processing = ImageProcessing(yolov3_weights, yolov3_config, yolov3_coco_names, image_processing_people_phones)
        img_processing.display_image()

    @staticmethod
    def video_events_label_click_handler():
        human_tracking = HumanTracking(yolov3_weights, yolov3_config, yolov3_coco_names, image_path_2, video_path)
        human_tracking.track_human()

    @staticmethod
    def add_events_images(h_box, event_image_path, label_text):
        label_image = TextLabel()

        label_text.setAlignment(Qt.AlignCenter)
        label_text.setStyleSheet(
            "background-color :#424743; "
            "padding :15px;"
            "border-radius: 10px"
        )

        label_text.setFont(QFont('Arial', 20))

        pix_map = QPixmap(event_image_path)
        smaller_pix_map = pix_map.scaled(400, 400, Qt.KeepAspectRatio, Qt.FastTransformation)
        label_image.setPixmap(smaller_pix_map)
        label_image.resize(20, 20)

        v_box = QVBoxLayout()
        v_box.addWidget(label_image)
        v_box.addWidget(label_text)
        v_box.setSpacing(10)

        h_box.addLayout(v_box)


# noinspection PyUnusedLocal
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Ui()
    sys.exit(app.exec_())
