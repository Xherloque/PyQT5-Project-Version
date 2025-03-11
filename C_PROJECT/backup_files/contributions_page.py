from PyQt5 import QtWidgets, QtGui,uic
from PyQt5.QtWidgets import QApplication
import sys

class ContributionsPage(QtWidgets.QWidget):
    def __init__(self,the_stack):
        super().__init__()
        uic.loadUi("C_PROJECT/UI_FILES/contributions_page.ui",self)
        self.the_stack = the_stack
        
        
        

app = QApplication(sys.argv)
window = ContributionsPage(the_stack='')
window.show()
sys.exit(app.exec_())