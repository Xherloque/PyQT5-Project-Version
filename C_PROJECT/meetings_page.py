from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTableWidget, QTableWidgetItem, QComboBox, QDialog
)
from PyQt5 import uic
import sys
import sqlite3
from database_funcs import get_table_as_object
from meeting_details import MeetingDetails


class MeetingRecordsUI(QWidget):
    def __init__(self, the_stack):
        super().__init__()
        self.the_stack = the_stack
        uic.loadUi("C_PROJECT/UI_FILES/meetings_page.ui", self)  # Load the UI file
        self.home_btn.clicked.connect(lambda x: self.the_stack.setCurrentIndex(1))
        self.view_meeting.clicked.connect(self.show_meeting_details)
        self.populate_meetings()
        
    def populate_meetings(self):
        """ Populates the table with test meeting records """
        conn = sqlite3.connect("group_management.db")
        cursor = conn.cursor()
        all_meetings = get_table_as_object(cursor, "meetings")
        conn.commit()
        conn.close()
        meetings = [
            (f"{'Meeting' + str(mt.meeting_id) if not mt.meeting_label else mt.meeting_label}", str(mt.meeting_date), str(mt.meeting_time), str(mt.agenda), str(mt.total_contributions),
             str(mt.facilitator), str(mt.attendance_count)) for mt in all_meetings
        ]

        self.tableWidget.setRowCount(len(meetings))
        for row, (meeting_id,meeting_date,meeting_time,agenda,total_contributions,facilitator,attendance_count) in enumerate(meetings):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(meeting_id))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(meeting_date))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(meeting_time))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(agenda))
            self.tableWidget.setItem(row, 4, QTableWidgetItem(total_contributions))
            self.tableWidget.setItem(row, 5, QTableWidgetItem(facilitator))
            self.tableWidget.setItem(row, 6, QTableWidgetItem(attendance_count))

    def show_meeting_details(self):
        if self.get_selected_row_id():
            mt_class = MeetingDetails(the_stack=self.the_stack, meeting_id=self.get_selected_row_id(), back_page_index=self.the_stack.currentIndex())
            self.the_stack.addWidget(mt_class)
            self.the_stack.setCurrentIndex(self.the_stack.count() - 1)
        
    def get_selected_row_id(self):
        """Gets the ID (row number) of the currently selected row."""
        selected_row = self.tableWidget.currentRow() + 1
        print(selected_row)
        return str(selected_row)
