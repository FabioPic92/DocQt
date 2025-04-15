import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QFileDialog, QPushButton
from PyQt5.QtCore import pyqtSignal, Qt,  pyqtSlot
from PyQt5.QtGui import QPixmap, QImage

from PIL import Image, ExifTags
from pdf2image import convert_from_path

from page.AbstractPage import AbstractPage
from page.PageIndex import pageIndex

class MainPage(AbstractPage):

    def __init__(self, parent, documentData):
        super().__init__()
        self.draw_ui()
        self.documentData = documentData

    def draw_ui(self):

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("No Document Load")
        self.imageLabel = QLabel()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.imageLabel)
        
        self.LoadDocument = QPushButton("Load Document")
        self.LoadDocument.clicked.connect(self.LoadAnalyzeFile)
        self.layout.addWidget(self.LoadDocument)

        self.AddDocument = QPushButton("Add Layout Document")
        self.layout.addWidget(self.AddDocument)

        central_wid = QtWidgets.QWidget()
        self.central_layout = QtWidgets.QGridLayout()
        central_wid.setLayout(self.central_layout)

    def LoadAnalyzeFile(self):
        if self.documentData.image is None:
            self.LoadFile()
        else :
            self.switch_page(pageIndex["Analyze"])

    # Da sistemare
    @pyqtSlot()
    def LoadFile(self):
        self.fileName, _ = QFileDialog.getOpenFileName(self, "Open Document", "", "Image files (*.jpg *.png)")
        if self.fileName:
            if self.fileName.lower().endswith(('.jpg', '.jpeg', '.png','.pdf')):
                self.LoadImage(self.fileName)
        self.update_ui()

    def LoadImage(self, fileName):
        if fileName.lower().endswith(('.jpg', '.jpeg', '.png')):
            image = self.CorrectImageRotation(fileName)
        elif fileName.lower().endswith('.pdf'):
            images = convert_from_path(fileName)
            image = images[0]
        self.label.setText(f"Loaded: {os.path.basename(fileName)}")
        self.documentData.fileName = os.path.basename(self.fileName)
        self.documentData.image = image
        pixmap = self.ImageToPixmap(image).scaled(400, 400, Qt.KeepAspectRatio)
        self.imageLabel.setPixmap(pixmap)

    def ImageToPixmap(self, pilImage):
        if pilImage.mode != "RGB":
            pilImage = pilImage.convert("RGB")
        data = pilImage.tobytes("raw", "RGB")
        qimage = QImage(data, pilImage.width, pilImage.height, QImage.Format_RGB888)
        return QPixmap.fromImage(qimage)

    def CorrectImageRotation(self, imagePath):
        image = Image.open(imagePath)
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break

            exif = image._getexif()
            if exif is not None:
                orientationValue = exif.get(orientation, None)

                if orientationValue == 3:
                    image = image.rotate(180, expand=True)
                elif orientationValue == 6:
                    image = image.rotate(270, expand=True)
                elif orientationValue == 8:
                    image = image.rotate(90, expand=True)
        except (AttributeError, KeyError, IndexError):
            pass
        return image
    
    def AnalyzeImage(self):
        self.Preprocessing()
        self.Analyze()
    
    def Preprocessing(self):
        pass

    def Analyze(self):
        pass

    def update_ui(self):
        if self.documentData.image is None:
            self.label.setText("No Document Load")
            self.imageLabel.clear()
            self.LoadDocument.setText("Load Document")
        else :
            self.label.setText(f"Loaded: {self.documentData.fileName}")
            self.LoadDocument.setText("Analyze")
            self.AddDocument.setText("Load Document")