import sys,os
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog,QApplication, QLineEdit

TEMP_LOG_DETS = {"username":'powder',"password":'1234'}
class LoginPage(QDialog):
    def __init__(self,the_stack):
        super().__init__()
        self.the_stack = the_stack
        # self.the_stack.setMinimumHeight(583)
        # self.the_stack.setMinimumWidth(820)
        # self.the_stack.setGeometry([(0.5,0.5),])
        loadUi("C_PROJECT/UI_FILES/login_page.ui", self)
        self.submit_btn.clicked.connect(self.login_user)
        self.password_text.setEchoMode(QLineEdit.Password)
        
    def login_user(self):
        if self.username_text.text() == TEMP_LOG_DETS["username"] and self.password_text.text() == TEMP_LOG_DETS["password"]: 
            self.the_stack.setCurrentIndex(self.the_stack.currentIndex()+1)
        else:
            self.warning_label.setText("Wrong Details. Essayer Encore...")
        
        
