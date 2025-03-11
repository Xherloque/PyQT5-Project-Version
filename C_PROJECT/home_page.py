import sys,os
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog,QApplication,QMainWindow
from tkinter import Tk
from add_members_to_db import test_data
from add_from_prev import AddFromPrev
from register_member import RegisterMember
from reports_page import ReportsPage
from contributions_page import ContributionsPage
from loans_page import LoansDebtsPage
from arrears_page import ArrearsPage
from app_settings import SettingsUI
from messages_notifications import MessagesUI
from tasks_reminders import TaskManager
from accounts import GroupFinanceUI
from meetings_page import MeetingRecordsUI
from record_new import RecordMeetingScreen
from members_page import MembersPage
from database_funcs import get_table_as_object
import sqlite3

root = Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

    
class HomePage(QMainWindow):
    def __init__(self,the_stack):
        super().__init__()
        self.the_stack = the_stack
        self.the_stack.setFixedHeight(screen_height)
        self.the_stack.setFixedWidth(screen_width)
        
        loadUi("C_PROJECT/UI_FILES/home_page.ui", self)
        self.members_page_btn.clicked.connect(lambda x: self.go_to("members"))
        self.members_count.setText(f"Total Members {self.get_member_count()}")
        self.add_from_prev.clicked.connect(lambda x: self.go_to("add_from_prev"))
        self.register_member.clicked.connect(lambda x: self.go_to("register_member"))
        self.all_reports.clicked.connect(lambda x: self.go_to("reports_page"))
        self.contrib_btn.clicked.connect(lambda x: self.go_to("contrib_page"))
        self.loans_btn.clicked.connect(lambda x: self.go_to("loans_page"))
        self.arrears_btn.clicked.connect(lambda x: self.go_to("arrears_page"))
        self.settings_btn.clicked.connect(lambda x: self.go_to("settings_page"))
        self.messages_btn.clicked.connect(lambda x: self.go_to("messages_page"))
        self.tasks_btn.clicked.connect(lambda x: self.go_to("tasks_page"))
        self.accounts_btn.clicked.connect(lambda x: self.go_to("accounts_page"))
        self.meetings_btn.clicked.connect(lambda x: self.go_to("meetings_page"))
        self.actionRecordMeeting_btn.triggered.connect(lambda x: self.go_to("record_meeting_page"))
    
    def get_member_count(self):
        conn = sqlite3.connect("group_management.db")
        cursor = conn.cursor()
        members = get_table_as_object(cursor, "members")
        conn.close()
        print(f"Updating the count down to {len(members)}....")
        self.members_count.setText(f"Total Members {len(members)}")
        return len(members)
    
    def go_to(self,page):
        if page == "members":
            self.the_stack.setCurrentIndex(2)
        elif page == "add_from_prev":
            self.the_stack.setCurrentIndex(4)
        elif page == "register_member":
            self.the_stack.setCurrentIndex(3)

        elif page == "reports_page":
            nm = ReportsPage(the_stack=self.the_stack)
            self.the_stack.addWidget(nm)
            self.the_stack.setCurrentIndex(self.the_stack.count() - 1)
            
        elif page == "contrib_page":
            nm = ContributionsPage(the_stack=self.the_stack)
            self.the_stack.addWidget(nm)
            self.the_stack.setCurrentIndex(self.the_stack.count() - 1)
        
        elif page == "loans_page":
            nm = LoansDebtsPage(the_stack=self.the_stack)
            self.the_stack.addWidget(nm)
            self.the_stack.setCurrentIndex(self.the_stack.count() - 1)
        
        elif page == "arrears_page":
            nm = ArrearsPage(the_stack=self.the_stack)
            self.the_stack.addWidget(nm)
            self.the_stack.setCurrentIndex(self.the_stack.count() - 1)
        
        elif page == "settings_page":
            nm = SettingsUI(the_stack=self.the_stack)
            self.the_stack.addWidget(nm)
            self.the_stack.setCurrentIndex(self.the_stack.count() - 1)
        
        elif page == "messages_page":
            nm = MessagesUI(the_stack=self.the_stack)
            self.the_stack.addWidget(nm)
            self.the_stack.setCurrentIndex(self.the_stack.count() - 1)
            
        elif page == "tasks_page":
            nm = TaskManager(the_stack=self.the_stack)
            self.the_stack.addWidget(nm)
            self.the_stack.setCurrentIndex(self.the_stack.count() - 1)
            
        elif page == "accounts_page":
            nm = GroupFinanceUI(the_stack=self.the_stack)
            self.the_stack.addWidget(nm)
            self.the_stack.setCurrentIndex(self.the_stack.count() - 1)
        
        elif page == "meetings_page":
            self.the_stack.setCurrentIndex(5)
            
        elif page == "record_meeting_page":
            self.the_stack.setCurrentIndex(6)
            #========== Change the on going text in homepage ==============#
            self.on_going_combo.clear()
            self.on_going_combo.addItem("New Meeting In Progress")


class GroupContactsDialog(QDialog):
    def __init__(self, meeting_id, date, time, agenda):
        super().__init__()
        self.setWindowTitle(f"Group Contacts Details")
        self.setGeometry(300, 200, 600, 400)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel(f"Meeting ID: {meeting_id}"))
        layout.addWidget(QtWidgets.QLabel(f"Date: {date}"))
        layout.addWidget(QtWidgets.QLabel(f"Time: {time}"))
        layout.addWidget(QtWidgets.QLabel(f"Agenda: {agenda}"))
        layout.addWidget(QtWidgets.QLabel(f"Facilitator: John Doe"))
        layout.addWidget(QtWidgets.QLabel(f"Attendance: 25 members"))
        layout.addWidget(QtWidgets.QLabel(f"Contributions: $300"))
        layout.addWidget(QtWidgets.QLabel(f"Proposals: Discuss project funding"))
        layout.addWidget(QtWidgets.QLabel(f"Discussions: Agreed on 10% increase in contributions"))

        close_btn = QtWidgets.QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

        self.setLayout(layout)

