from PyQt5 import QtWidgets, QtCore, uic
import sqlite3
from database_funcs import get_table_as_object, get_member_details
from meeting_details import MeetingDetails

def member_from_meetings(index):
    conn = sqlite3.connect("group_management.db")
    cursor = conn.cursor()
    member = get_member_details(cursor=cursor, member_id=index)
    conn.commit()
    conn.close()
    return member["member"][0].name

def get_all_meetings():
    conn = sqlite3.connect("group_management.db")
    cursor = conn.cursor()
    all_meetings = get_table_as_object(cursor, "meetings")
    conn.commit()
    conn.close()
    return all_meetings

def get_all_contribs():
    conn = sqlite3.connect("group_management.db")
    cursor = conn.cursor()
    all_contribs = get_table_as_object(cursor, "contributions")
    conn.commit()
    conn.close()
    return all_contribs
    
class ContributionsPage(QtWidgets.QWidget):
    def __init__(self, the_stack):
        super().__init__()
        self.the_stack = the_stack
        self.setWindowTitle("Contributions Page")
        self.setGeometry(100, 100, 900, 650)

        # Main layout
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 100)  # Leaves space at the bottom

        # Navigation Bar
        self.nav_bar = QtWidgets.QWidget()
        self.nav_bar.setFixedHeight(60)
        self.nav_bar.setStyleSheet("""
            background-color: #2c3e50; 
            color: white;
            border-bottom: 2px solid #34495e;
        """)
        self.nav_layout = QtWidgets.QHBoxLayout(self.nav_bar)

        self.page_title = QtWidgets.QLabel("📊 Contributions")
        self.page_title.setStyleSheet("font-size: 22px; font-weight: bold; padding: 10px;")
        self.home_button = QtWidgets.QPushButton("🏠 Home")
        self.home_button.setStyleSheet("""
            background-color: #3498db; 
            color: white; 
            padding: 8px 15px; 
            border-radius: 8px;
            font-weight: bold;
        """)
        self.home_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.home_button.clicked.connect(lambda x: self.the_stack.setCurrentIndex(1))

        self.nav_layout.addWidget(self.page_title)
        self.nav_layout.addStretch()
        self.nav_layout.addWidget(self.home_button)
        self.main_layout.addWidget(self.nav_bar)

        # Scroll Area Setup
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scroll_content)

        # Dummy Data
        members = []
        payment_types = ["Cash", "Bank", "Mobile Money"]

        self.meetings_data = []
        for i in get_all_meetings():
            self.meetings_data.append({
                "meeting": f"Meeting {i.meeting_id}",
                "total": f"Ksh. {i.total_contributions}",
                "required": f"Ksh. 300",
                "type": "Cash",
                "date": i.meeting_date,
                "contributions": [f for f in get_all_contribs() if f.meeting_id == i.meeting_id]
            })

        # Generate Meetings Section
        for index, meeting in enumerate(self.meetings_data, start=1):
            meeting_box = self.add_contribs_to_box(index, meeting)
            self.scroll_layout.addWidget(meeting_box)

        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)
    
    def add_contribs_to_box(self, index, meeting):
        wid = uic.loadUi("C_PROJECT/UI_FILES/mini_meeting_box.ui")
        wid.meeting_id_label.setText(f"Meeting {index}")
        wid.summary_label.setText(
            f"📅 {meeting['date']} | 💰 Total: {meeting['total']} | Required: {meeting['required']} | Type: {meeting['type']}"
        )
        wid.view_btn.clicked.connect(lambda x: self.view_the_sepcific(index))
        # Fill the contributions table
        wid.contrib_table.setRowCount(len(meeting["contributions"]))
        rel_contribs = [(member_from_meetings(contrib.member_id), str(contrib.amount), contrib.payment_method, contrib.contribution_date)
                        for contrib in meeting['contributions']]
        for row_idx, (name, amount, method, date) in enumerate(rel_contribs):
            wid.contrib_table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(name))
            wid.contrib_table.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(amount))
            wid.contrib_table.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(method))
            wid.contrib_table.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(date))

        return wid

    def view_the_sepcific(self, index):
        mt_class = MeetingDetails(the_stack=self.the_stack, meeting_id=index, back_page_index = self.the_stack.currentIndex())
        self.the_stack.addWidget(mt_class)
        self.the_stack.setCurrentIndex(self.the_stack.count() - 1)
        