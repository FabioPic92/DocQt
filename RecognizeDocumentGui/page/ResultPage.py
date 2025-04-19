from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout

from page.AbstractPage import AbstractPage
from page.PageIndex import pageIndex

class ResultPage(AbstractPage):
    def __init__(self, parent, documentData):
        super().__init__()
        self.draw_ui()
        self.Testx = 1

    def draw_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("Result:")
        self.textResult = QLabel("")
        self.textResult.setWordWrap(True)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.textResult)

        self.refresh_button = QPushButton("Reflesh result")
        self.refresh_button.clicked.connect(self.load_result)
        self.layout.addWidget(self.refresh_button)
        pass

    def load_result(self):
        result = getattr(self.parent, "analysis_result", "No result")
        self.text_output.setText(result)

    def update_ui(self):
        pass