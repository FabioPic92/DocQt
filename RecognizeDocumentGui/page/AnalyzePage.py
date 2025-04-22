import cv2

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QScrollArea, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage

from page.AbstractPage import AbstractPage
from page.PageIndex import pageIndex

class AnalyzePage(AbstractPage):
    def __init__(self, parent, documentData):
        super().__init__()
        
        self.documentData = documentData

        self.draw_ui()

    def draw_ui(self):

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.image = QLabel()
        self.layout.addWidget(self.image)

        self.pixmap = QPixmap()
        self.scroll_area = QScrollArea()

        self.image.setScaledContents(False) 

        self.scroll_area.setWidget(self.image)
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        self.show_result_button = QPushButton("Show Result")
        self.show_result_button.clicked.connect(self.show_result)
        self.layout.addWidget(self.show_result_button)

        self.cancel_analyze_button = QPushButton("Cancel Analyze")
        self.cancel_analyze_button.clicked.connect(self.cancel_analyze)
        self.layout.addWidget(self.cancel_analyze_button)

    def show_result(self):
        self.switch_page(pageIndex["Result"])

    def cancel_analyze(self):
        pass

    def image_to_pixmap(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        
        height, width, channel = rgb_image.shape
        bytes_per_line = channel * width
        
        qimage = QImage(rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        
        return QPixmap.fromImage(qimage)

    def update_ui(self):
        if self.documentData.image_proc is not None:
            pixmap = self.image_to_pixmap(self.documentData.image_proc)
            self.image.setPixmap(pixmap)
        else:
            print("File not found")