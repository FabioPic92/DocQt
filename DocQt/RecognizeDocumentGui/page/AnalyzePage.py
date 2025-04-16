from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QScrollArea, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage

from page.AbstractPage import AbstractPage
from page.PageIndex import pageIndex

from PIL import Image

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

        self.showResultButtton = QPushButton("Show Result")
        #self.ShowResultButtton.clicked.connect()
        self.layout.addWidget(self.showResultButtton)

        self.cancelAnalyzeButton = QPushButton("Cancel Analyze")
        self.cancelAnalyzeButton.clicked.connect(self.cancel_analyze)
        self.layout.addWidget(self.cancelAnalyzeButton)

    def cancel_analyze(self):
        if self.documentData.image is not None:
            pixmap = self.pil_to_pixmap(self.documentData.image)
            self.image.setPixmap(pixmap)

    def pil_to_pixmap(self, pil_image):
        if pil_image.mode != "RGB":
            pil_image = pil_image.convert("RGB")
        data = pil_image.tobytes("raw", "RGB")
        qimage = QImage(data, pil_image.width, pil_image.height, QImage.Format_RGB888)
        return QPixmap.fromImage(qimage)

    def update_ui(self):
        if self.documentData.image_proc is not None:
            pixmap = self.pil_to_pixmap(self.documentData.image_proc)
            self.image.setPixmap(pixmap)
        else:
            print("File not found")