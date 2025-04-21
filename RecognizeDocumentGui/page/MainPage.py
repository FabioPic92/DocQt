import os
import piexif
import cv2
from qasync import asyncSlot

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QFileDialog, QPushButton
from PyQt5.QtCore import pyqtSignal, Qt,  pyqtSlot
from PyQt5.QtGui import QPixmap, QImage

from PIL import Image, ExifTags, ImageOps

from pdf2image import convert_from_path

from page.AbstractPage import AbstractPage
from page.PageIndex import pageIndex

from model.model import Model
from model.AnalyzeDocument import processing_image

from image.DocumentScanner import scan

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
        self.LoadDocument.clicked.connect(self.load_analyze_file)
        self.layout.addWidget(self.LoadDocument)

        self.AddDocument = QPushButton("Add Layout Document")
        self.layout.addWidget(self.AddDocument)

        central_wid = QtWidgets.QWidget()
        self.central_layout = QtWidgets.QGridLayout()
        central_wid.setLayout(self.central_layout)

    # def load_analyze_file(self):
    #     # self.documentData.filename = '/home/fpicciati/Downloads/20250223_180311.jpg'        
    #     # self.documentData.image = Image.open(self.documentData.filename)
    #     # processing_image(self.documentData)# Test
    #     # self.switch_page(pageIndex["Analyze"])

    #     if self.documentData.image is None:
    #         self.load_file()
    #         self.model = Model('textextractbucket2', self.documentData)
    #         self.model.upload_file()        
    #     else :
    #         self.analyze_image()
    #         print(f"Entra {self.documentData.filename}")
    #         self.switch_page(pageIndex["Analyze"])

    @asyncSlot()
    async def load_analyze_file(self):
        if self.documentData.image is None:
            self.load_file()
            self.model = Model(self.documentData)
            # niente upload S3
        else:
            await self.analyze_image()
            self.switch_page(pageIndex["Analyze"])

    @pyqtSlot()
    def load_file(self):
        self.fileName, _ = QFileDialog.getOpenFileName(self, "Open Document", "", "Image files (*.jpg *.png)")
        if self.fileName:
            if self.fileName.lower().endswith(('.jpg', '.jpeg', '.png','.pdf')):
                self.load_image(self.fileName)
        self.documentData.filename = self.fileName
        self.update_ui()

    def load_image(self, fileName):
        if fileName.lower().endswith(('.jpg', '.jpeg', '.png')):
            image = self.correct_image_orientation(fileName)
        elif fileName.lower().endswith('.pdf'):
            images = convert_from_path(fileName)
            image = images[0]
        self.preprocessing_img = self.preprocessing(image)
        self.label.setText(f"Loaded: {os.path.basename(fileName)}")
        self.documentData.fileName = os.path.basename(self.fileName)
        self.documentData.image = self.preprocessing_img
        
        pixmap = self.image_to_pixmap(self.preprocessing_img).scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.setAlignment(Qt.AlignCenter)  

    # def image_to_pixmap(self, pilImage):
    #     if pilImage.mode != "RGB":
    #         pilImage = pilImage.convert("RGB")
    #     data = pilImage.tobytes("raw", "RGB")
    #     qimage = QImage(data, pilImage.width, pilImage.height, QImage.Format_RGB888)
    #     return QPixmap.fromImage(qimage)
    
    def image_to_pixmap(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        
        height, width, channel = rgb_image.shape
        bytes_per_line = channel * width
        
        qimage = QImage(rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        
        return QPixmap.fromImage(qimage)

    def correct_image_orientation(self, imagePath):
        image = cv2.imread(imagePath)

        try:
            exif_dict = piexif.load(imagePath)
            orientation = exif_dict["0th"].get(piexif.ImageIFD.Orientation, 1)

            if orientation == 3:
                image = cv2.rotate(image, cv2.ROTATE_180)
            elif orientation == 6:
                image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
            elif orientation == 8:
                image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)

        except Exception as e:
            print(f"EXIF non disponibile o errore nella lettura: {e}")

        return image

    @asyncSlot()
    async def analyze_image(self):
        await self.analyze()
        self.switch_page(pageIndex["Analyze"])

    @asyncSlot()
    async def analyze(self):
        await self.model.analyze_document()  # async model method
        self.postProcessing()

    def preprocessing(self, img):
        print("PreProcessing...")
        img_preprocessing = scan(img)
        print("Document Precessed")
        return img_preprocessing

    def postProcessing(self):
        processing_image(self.documentData)

    def update_ui(self):
        if self.documentData.image is None:
            self.label.setText("No Document Load")
            self.imageLabel.clear()
            self.LoadDocument.setText("Load Document")
        else :
            self.label.setText(f"Loaded: {self.documentData.fileName}")
            self.LoadDocument.setText("Analyze")
            self.AddDocument.setText("Load Document")