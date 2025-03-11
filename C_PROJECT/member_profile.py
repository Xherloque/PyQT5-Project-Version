from PyQt5 import QtWidgets, QtGui,uic,QtCore
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication, QLabel, QWidget,QLineEdit
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QColor, QFont, QPalette
import sys,os
from database_funcs import get_member_by_name, get_member_details, get_table_as_object, add_member
import sqlite3

class UserProfile(QtWidgets.QWidget):
    def __init__(self,member_name, the_stack):
        super().__init__()
        uic.loadUi("C_PROJECT/UI_FILES/member_profile.ui",self)
        self.the_stack = the_stack
        self.member_name = member_name
        self.scrollArea.setWidgetResizable(True)
        self.home_btn.clicked.connect(lambda x: self.the_stack.setCurrentIndex(1))
        self.back_btn.clicked.connect(lambda x: self.the_stack.setCurrentIndex(2))
        # self.profileLabel = self.profilePicLabel
        self.adjust_UI()
        
    def adjust_UI(self):
        conn = sqlite3.connect("group_management.db")
        cursor = conn.cursor()
        member = get_member_by_name(cursor, self.member_name)
        full_m = get_member_details(cursor,member_id=member.member_id)
        all_meetings = get_table_as_object(cursor,table_name="meetings")
        conn.close()

        # Ensure profile_image is a valid path
        if not member or not member.profile_image:  # If member doesn't exist or has no image
            prof_image = "C_PROJECT/media/profile_default.png"
        elif isinstance(member.profile_image, str) and os.path.exists(member.profile_image):
            prof_image = member.profile_image
        else:
            prof_image = "C_PROJECT/media/profile_default.png"

        # Load and scale the image
        pixmap = QPixmap(prof_image).scaled(
            self.profilePicLabel.size(), 
            QtCore.Qt.KeepAspectRatio, 
            QtCore.Qt.SmoothTransformation
        )

        # Create rounded pixmap
        rounded_pixmap = self.create_rounded_pixmap(pixmap, self.profilePicLabel.width())

        # Update QLabel with rounded image
        self.profilePicLabel.setPixmap(rounded_pixmap)
        #=======================================================
        
        self.title_label.setText(f"{member.name}'s Profile")
        self.full_name_box.setText(member.name)
        y,m,d = member.date_joined.split("-")
        self.date_joined.setDate(QDate(int(y), int(m), int(d)))
        self.date_joined.setDisplayFormat("MMM d, yyyy") 
        self.active_check_box.setText(member.status)
        self.active_check_box.setChecked(True if member.status == "Active" else False)
        self.active_check_box.stateChanged.connect(
            lambda x: self.on_checkbox_state_changed(self.active_check_box.isChecked())
            )
        self.national_id.setText(member.id_number)
        if len(full_m["contacts"]) > 1:
            if "@" not in str(full_m["contacts"][0].contact):
                self.phone_1.setText(full_m["contacts"][0].contact)
            elif "@" not in str(full_m["contacts"][1].contact):
                self.phone_2.setText(full_m["contacts"][1].contact)
            elif "@" in str(full_m["contacts"][0].contact):
                self.email.setText(full_m["contacts"][0].contact)
            elif "@" in str(full_m["contacts"][1].contact):
                self.email.setText(full_m["contacts"][1].contact)
        
        else:
            if "@" not in str(full_m["contacts"][0].contact):
                self.phone_1.setText(full_m["contacts"][0].contact)
            elif "@" in str(full_m["contacts"][0].contact):
                self.email.setText(full_m["contacts"][0].contact)
        self.address.setText(member.address)
        
        Total_Contribuitions = sum([c.amount for c in full_m["contributions"]])       
        Total_Arrears = sum([c.amount for c in full_m["arrears"]])
        Total_Loans = sum([c.amount for c in full_m["loans"]])
        
        self.total_contribs.setText(str(Total_Contribuitions))
        self.total_arrears.setText(str(Total_Arrears))
        self.total_loans.setText(str(Total_Loans))
        
        fam ={j.relation_to_member:(j.name,j.contact) for j in full_m["family"]}
        for fm in fam.keys():
            self.add_form_row(str(fm))
            text_field = self.findChild(QLineEdit, f"{str(fm)}LineEdix")
            text_field.setText(f"{fam[fm][0]}    -    {fam[fm][1]}")
        
        self.attendance.setText(f"Member Attendance: {str(len(full_m["attendance"]))} Out of {len(all_meetings)}")
        self.attendance.setFont(QFont("LM Roman 17", 17))
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
        
        self.formLayout.addRow(label, line_edit)  # Add the pair to the form layout
     
    def on_checkbox_state_changed(self,status):
        if status:
            self.active_check_box.setText("Inactive")
        else:
            self.active_check_box.setText("Active")
            
    def create_rounded_pixmap(self, pixmap, size):
        """Helper function to create a rounded image"""
        rounded = QPixmap(size, size)
        rounded.fill(QtCore.Qt.transparent)  # Transparent background

        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        path = QPainterPath()
        path.addEllipse(0, 0, size, size)  # Draw circular shape

        painter.setClipPath(path)
        painter.drawPixmap(0, 0, size, size, pixmap)  # Draw clipped image
        painter.end()

        return rounded



    def save_edits(self):
        pass