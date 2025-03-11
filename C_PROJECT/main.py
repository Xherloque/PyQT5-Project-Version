import sys,os
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog,QApplication,QMainWindow
from home_page import HomePage
from login_page import LoginPage
from members_page import MembersPage

from add_from_prev import AddFromPrev
from register_member import RegisterMember

from meetings_page import MeetingRecordsUI
from record_new import RecordMeetingScreen

def main():
    app = QApplication(sys.argv)
    wid = QtWidgets.QStackedWidget()
    home_page = HomePage(the_stack=wid)
    log_page = LoginPage(the_stack=wid)
    memb_page = MembersPage(the_stack=wid)
    memb_page.count_down_signal.connect(home_page.get_member_count)
    reg_memb = RegisterMember(the_stack=wid)
    reg_memb.member_registered_successfully.connect(memb_page.refresh_members_list)
    add_memb = AddFromPrev(the_stack=wid)
    add_memb.member_added_successfully.connect(memb_page.refresh_members_list)
    tout_meetings = MeetingRecordsUI(the_stack=wid)
    rec_meeting = RecordMeetingScreen(the_stack=wid)
    rec_meeting.meeting_saving_ended.connect(tout_meetings.populate_meetings)
    
    wid.setWindowTitle("CSMS Desktop App")
    wid.addWidget(log_page)
    wid.addWidget(home_page)
    wid.addWidget(memb_page)
    wid.addWidget(reg_memb)
    wid.addWidget(add_memb)
    wid.addWidget(tout_meetings)
    wid.addWidget(rec_meeting)
    wid.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
