from PyQt5.QtWidgets import (
    QApplication, QWidget, QListWidget, QStackedWidget, QVBoxLayout,
    QLabel, QCheckBox, QPushButton, QLineEdit, QFormLayout, QComboBox,
    QHBoxLayout, QTextEdit, QListWidgetItem
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5 import uic
import sys

class SettingsUI(QWidget):
    def __init__(self, the_stack):
        super().__init__()
        uic.loadUi("C_PROJECT/UI_FILES/application_settings.ui",self)
        self.the_stack = the_stack
        self.home_btn.clicked.connect(lambda x: self.the_stack.setCurrentIndex(1))
        