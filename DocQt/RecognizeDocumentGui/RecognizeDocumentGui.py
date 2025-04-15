import sys
import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QPushButton, QFileDialog, QLabel, QStackedWidget, QVBoxLayout
from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal, QObject
from PyQt5.QtGui import QIcon, QPixmap, QImage

from PIL import Image, ExifTags

from page.MainPage import MainPage
from page.AnalyzePage import AnalyzePage
from page.ResultPage import ResultPage

from model.struct import DocumentData
from draw import draw_lines,

class RecognizeDocumentGui(QtWidgets.QMainWindow):
        def __init__(self):
            super().__init__()
            self.title = "Recognize Document GUI"
            self.left = 50
            self.top = 50
            self.width = 640
            self.height = 480
            self.widgets = {}
            self.invind_widgets = {}

            self.documentData = DocumentData()

            self.init_ui()

        def init_ui(self):
            self.setWindowTitle(self.title)
            self.setGeometry(self.left, self.top, self.width, self.height)


            self.stack = QStackedWidget()
            self.setCentralWidget(self.stack)

            self.load_image_page = MainPage(self, self.documentData)
            self.analyze_page = AnalyzePage(self, self.documentData)
            self.result_page = ResultPage(self, self.documentData)

            self.stack.addWidget(self.load_image_page) 
            self.stack.addWidget(self.analyze_page)
            self.stack.addWidget(self.result_page)  

            self.load_image_page.change_page.connect(self.switch_page)

            self.show()

        def switch_page(self, index):
            self.stack.setCurrentIndex(index)
            self.stack.currentWidget().update_ui()

def main(args=None):
    app = QtWidgets.QApplication([])
    mw = RecognizeDocumentGui()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
