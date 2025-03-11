from PyQt5 import QtWidgets, QtGui,uic

class ReportsPage(QtWidgets.QWidget):
    def __init__(self,the_stack):
        super().__init__()
        uic.loadUi("C_PROJECT/UI_FILES/reports_page.ui",self)
        self.the_stack = the_stack
        self.home_btn.clicked.connect(lambda x: self.the_stack.setCurrentIndex(1))
        