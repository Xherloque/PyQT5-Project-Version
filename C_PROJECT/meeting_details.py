from PyQt5 import QtWidgets, QtGui,uic
from database_funcs import get_table_as_object, get_member_details, get_member_by_name
import sqlite3


def memb_by_name(memba):
    conn = sqlite3.connect("group_management.db")
    cursor = conn.cursor()
    mbs = get_member_by_name(cursor,memba)
    conn.close()
    return mbs


class MeetingDetails(QtWidgets.QWidget):
    def __init__(self,the_stack, meeting_id, back_page_index):
        super().__init__()
        uic.loadUi("C_PROJECT/UI_FILES/meeting_details.ui",self)
        self.the_stack = the_stack
        self.meeting_id = int(meeting_id)
        self.back_page_index = back_page_index
        self.back_btn.clicked.connect(self.go_back)
        
        #Get stuff from the database
        conn = sqlite3.connect("group_management.db")
        cursor = conn.cursor()
        all_proposals = get_table_as_object(cursor, "proposals")
        self.all_attendance = get_table_as_object(cursor, "attendance")
        self.all_contributions = get_table_as_object(cursor, "contributions")
        all_meetings = get_table_as_object(cursor, "meetings")
        spec_meeting = [mting for mting in all_meetings if mting.meeting_id == self.meeting_id]
        # print("ALL IDS",[i.meeting_id for i in all_meetings])
        conn.commit()
        conn.close()
        
        if spec_meeting:
            meetingDetails = spec_meeting[0]
            self.title_label.setText(f"Meeting {self.meeting_id} Full Details")
            self.total_label.setText(f"TOTAL CONTRIBUTION:     KSH.{meetingDetails.total_contributions}")
            self.lineEdit.setText(meetingDetails.meeting_label)
            self.label_4.setText(meetingDetails.meeting_date)
            self.label_6.setText(meetingDetails.meeting_time)
            self.label_8.setText(meetingDetails.time_ended)
            self.label_10.setText(meetingDetails.facilitator)
            self.label_12.setText(meetingDetails.agenda)
            
            for prp in [pr for pr in all_proposals if pr.meeting_id == self.meeting_id]:
                print((prp.proposal_description, prp.meeting_id, self.meeting_id, prp.member_id))
                conn = sqlite3.connect("group_management.db")
                cursor = conn.cursor()
                prp_member = get_member_details(cursor,prp.member_id)
                fk_name = [h.name for h in prp_member["member"] if h.member_id == prp.member_id][0]
                conn.commit()
                conn.close()
                prp_text = f"{prp.proposal_description}  By: {fk_name}"
                item = QtWidgets.QListWidgetItem(prp_text)
                self.listWidget.addItem(item)
                
        self.fill_attendance_table()
        self.fill_contributions_table()
                
    def fill_attendance_table(self):
        #Header names ["MEMBER", "PRESENT/ABSENT", ON TIME]
        self.checked_count_label.setText(f"Total Attendance: {len([att for att in self.all_attendance if att.meeting_id==self.meeting_id])} Members")
        if len([att for att in self.all_attendance if att.meeting_id==self.meeting_id]) > 0:
            # name of the table --> self.tableWidget
            # col 1 --> memb_by_name(att.member_id).name
            # col 2 --> "Present"
            # col 3 --> att.on_time
            
            self.tableWidget.setRowCount(0)
            for att in [att for att in self.all_attendance if att.meeting_id == self.meeting_id]:
                row_position = self.tableWidget.rowCount()
                conn = sqlite3.connect("group_management.db")
                cursor = conn.cursor()
                prp_member = get_member_details(cursor,att.member_id)
                fk_name = [h.name for h in prp_member["member"] if h.member_id == att.member_id][0]
                conn.commit()
                conn.close()
                self.tableWidget.insertRow(row_position)
                self.tableWidget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(fk_name))
                self.tableWidget.setItem(row_position, 1, QtWidgets.QTableWidgetItem("Present"))
                self.tableWidget.setItem(row_position, 2, QtWidgets.QTableWidgetItem(att.on_time))
        
    def fill_contributions_table(self):
        #Header names ["MEMBER", "Amount", "Paid By"]
        if len([contrib for contrib in self.all_contributions if contrib.meeting_id==self.meeting_id]) > 0:
            # name of the table --> self.tableWidget_2
            # col 1 --> memb_by_name(contrib.member_id).name
            # col 2 --> str(contrib.amount)
            # col 3 --> contrib.payment_method    
            self.tableWidget_2.setRowCount(0)
            for contrib in [contrib for contrib in self.all_contributions if contrib.meeting_id == self.meeting_id]:
                row_position = self.tableWidget_2.rowCount()
                conn = sqlite3.connect("group_management.db")
                cursor = conn.cursor()
                prp_member = get_member_details(cursor,contrib.member_id)
                fk_name = [h.name for h in prp_member["member"] if h.member_id == contrib.member_id][0]
                conn.commit()
                conn.close()
                self.tableWidget_2.insertRow(row_position)
                self.tableWidget_2.setItem(row_position, 0, QtWidgets.QTableWidgetItem(fk_name))
                self.tableWidget_2.setItem(row_position, 1, QtWidgets.QTableWidgetItem(str(contrib.amount)))
                self.tableWidget_2.setItem(row_position, 2, QtWidgets.QTableWidgetItem(contrib.payment_method))
    
    def go_back(self):
        self.the_stack.setCurrentIndex(self.back_page_index)
        self.the_stack.removeWidget(self)
        self.deleteLater() #Schedule widget for deletion.
        