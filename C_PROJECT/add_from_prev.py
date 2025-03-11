from PyQt5 import QtWidgets, QtGui,uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QLineEdit,QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QColor, QFont, QPalette
import sys,os
from database_funcs import (get_member_by_name, get_member_details,
                            get_table_as_object,add_member,
                            get_member_contacts, add_arrear,add_contribution,
                            add_loan)
import sqlite3
from PyQt5.QtWidgets import QMessageBox,QFileDialog
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton




class PopupForm(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add Family Member")
        self.setGeometry(200, 200, 300, 150)

        layout = QVBoxLayout()

        # Label & Input 1
        self.label1 = QLabel("Relation: ")
        self.input1 = QLineEdit()
        layout.addWidget(self.label1)
        layout.addWidget(self.input1)


        self.labelm = QLabel("Full Name: ")
        self.inputm = QLineEdit()
        layout.addWidget(self.labelm)
        layout.addWidget(self.inputm)
        
        # Label & Input 2
        self.label2 = QLabel("Contact:")
        self.input2 = QLineEdit()
        layout.addWidget(self.label2)
        layout.addWidget(self.input2)

        # Buttons
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")

        self.save_button.clicked.connect(self.save_data)
        self.cancel_button.clicked.connect(self.reject)  # Close dialog

        layout.addWidget(self.save_button)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

    def save_data(self):
        """Handle saving data and close the dialog."""
        relation = self.input1.text().strip()
        full_name = self.inputm.text().strip()
        contact = self.input2.text().strip()
        
        if not relation and full_name and contact:
            QMessageBox.critical(self, "Error", "All fields must be filled!")
            return
        else:
            self.accept()  # Close dialog
            return [relation, full_name, contact]
        
        
        



class AddFromPrev(QtWidgets.QWidget):
    #Fire a signal to the members page
    member_added_successfully = pyqtSignal()
         
    def __init__(self,the_stack):
        super().__init__()
        uic.loadUi("C_PROJECT/UI_FILES/add_member.ui",self)
        self.the_stack = the_stack
        self.home_btn.clicked.connect(lambda x: self.the_stack.setCurrentIndex(1))
        self.go_to_members.clicked.connect(lambda x: self.the_stack.setCurrentIndex(2))
        self.add_new_btn.clicked.connect(self.add_family_to_form)
        self.upload_button.clicked.connect(self.open_file_dialog)
        #Save dict:
        self.save_dict = {"family": {}, "profile_image": None}
        
        self.dATEJOINEDDateEdit.setDisplayFormat("dd/MM/yyyy")
        self.dATEOFBIRTHDateEdit.setDisplayFormat("dd/MM/yyyy")
        self.save_member.clicked.connect(self.add_member_to_db)
        
    def add_form_row(self, label_text):
        """Dynamically adds a QLabel and QLineEdit pair to the form layout."""
        label = QLabel(label_text)
        label.setFont(QFont("Arial", 16, QFont.Bold))  # Bold font
        label.setStyleSheet("color: #333; padding: 3px;")  # Dark text, padding
        
        line_edit = QLineEdit()
        line_edit.setObjectName(f"{label_text}LineEdix")
        line_edit.setFont(QFont("Arial", 15))  # Matching font
        line_edit.setStyleSheet(
            """
            QLineEdit {
                border: 2px solid #0078D7;
                border-radius: 5px;
                padding: 5px;
                background-color: #f0f8ff;
                selection-background-color: #0078D7;
            }
            """
        )  # Styled border, background, and selection color
        
        self.family_form.addRow(label, line_edit)  # Add the pair to the form layout
    
    def add_family_to_form(self):
        # A dialog to fill in the details the use add form to put it in form
        dialog = PopupForm()
        if dialog.exec_():  # If the dialog was accepted (Save button clicked)
            relation,fl_name, contact = dialog.save_data()
            self.add_form_row(relation)
            text_field = self.findChild(QLineEdit, f"{relation}LineEdix")
            text_field.setText(f"{fl_name}    -    {contact}")
            self.save_dict["family"][relation] = (fl_name,contact) 
    
    def show_error_message(self):
        """Displays an error message box."""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)  # Error icon
        msg_box.setWindowTitle("Error")
        msg_box.setText("Important details missing!!")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
        
    def open_file_dialog(self):
        start_folder = os.path.join(os.getcwd(), "C_PROJECT/media")# Change this to your preferred default folder

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select a File",
            start_folder,  # The starting directory
            "All Files (*);;Python Files (*.py);;Text Files (*.txt)"  # File filters
        )

        if file_path:  # If a file is selected
            self.save_dict["profile_image"] = file_path # Show file path in label
            # print("Selected file:", file_path)  # Print path for debugging


    def add_member_to_db(self):
        conn = sqlite3.connect("group_management.db")
        cursor = conn.cursor()
        
        
        if self.fULLNAMELineEdit.text() and self.nATIONALIDLineEdit.text() and self.pHONENUMBER1LineEdit.text():
            #The member is atleast addable
            success = add_member(cursor=cursor,name=self.fULLNAMELineEdit.text(),
                       id_number=self.nATIONALIDLineEdit.text(),
                       role=self.pOSITIONROLEComboBox.currentText(),
                       date_joined=self.dATEJOINEDDateEdit.date().toString("yyyy-MM-dd"),
                       contact=[a for a in [self.pHONENUMBER1LineEdit.text(),self.pHONENUMBER2LineEdit.text()] if len(a)>1],
                       family=self.save_dict["family"],
                       address = self.hOMEADDRESSLineEdit.text(),
                       Active = self.sTATUSComboBox.currentText(),
                       date_of_birth = self.dATEOFBIRTHDateEdit.text(),
                       profile_image = self.save_dict["profile_image"],
                       health_details = self.health_details_box.toPlainText())
            

            if success:
                print("Member added successfully!")    
                conn.commit()
                conn.close()
                self.member_added_successfully.emit()
                self.the_stack.setCurrentIndex(2)
                
            # financial_totals
            ttc = 0 if not self.total_contribs.text() else int(self.total_contribs.text())
            ttl = 0 if not self.total_loans.text() else int(self.total_loans.text())
            tta = 0 if not self.total_arrears.text() else int(self.total_arrears.text())
            
            
                
        else:
            self.show_error_message()

        
        
