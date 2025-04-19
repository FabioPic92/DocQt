from abc import ABC, abstractmethod

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QTimer
from PyQt5 import QtWidgets

class AbstractMeta(type(QtWidgets.QWidget), type(ABC)):
    pass

class AbstractPage(QtWidgets.QWidget, ABC, metaclass=AbstractMeta):
    update = pyqtSignal()
    destroy = pyqtSignal()
    change_page = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    @pyqtSlot()
    def destroy_slot(self):
        self.destroy.emit()

    @pyqtSlot()
    def update_slot(self):
        self.update.emit()


    @abstractmethod
    def draw_ui(self):
        pass

    @abstractmethod
    def update_ui(self):
        pass

    @pyqtSlot()
    def switch_page(self, index):
        self.change_page.emit(index)
