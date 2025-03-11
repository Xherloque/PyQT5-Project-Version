from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem,
    QScrollArea,  QTableWidget,QFrame, QTableWidgetItem
)
from PyQt5 import uic
import sys

class GroupFinanceUI(QWidget):
    def __init__(self, the_stack):
        super().__init__()
        self.the_stack = the_stack
        uic.loadUi("C_PROJECT/UI_FILES/group_accounts.ui", self)  # Load the UI file
        self.home_btn.clicked.connect(lambda x: self.the_stack.setCurrentIndex(1))
        

