from PyQt5 import uic, QtWidgets
import sys
from add_members_to_db import test_data
from member_profile import UserProfile
import sqlite3
from database_funcs import get_all_members_with_contacts
from add_from_prev import AddFromPrev
from register_member import RegisterMember
from PyQt5.QtCore import pyqtSignal


class MembersPage(QtWidgets.QWidget):
    count_down_signal = pyqtSignal()
    
    def __init__(self,the_stack):
        super().__init__()
        self.the_stack =the_stack
        uic.loadUi("C_PROJECT/UI_FILES/members_page.ui", self)  # Load the UI file

        # Get references to the UI elements
        self.search_box = self.findChild(QtWidgets.QLineEdit, "searchLineEdit")  # Replace with your object name
        self.table_widget = self.findChild(QtWidgets.QTableWidget, "membersTableWidget")  # Replace with your object name
        self.home_btn.clicked.connect(lambda x: self.the_stack.setCurrentIndex(1))
        self.go_to_register.clicked.connect(self.reg_page)
        self.add_member_btn.clicked.connect(self.prev_page)
        # Load data into the table
        self.load_table_data()
        # Connect search box to filter function
        self.search_box.textChanged.connect(self.filter_table)
        self.table_widget.cellClicked.connect(self.on_row_click)
        # add_members_page.member_added.connect(self.refresh_members_list)

    def refresh_members_list(self):
        print("Refreshing members list...")
        self.load_table_data()  # Call the function that loads members
        self.count_down_signal.emit()
        
    def reg_page(self):
        m_page = self.the_stack.findChild(RegisterMember)
        
        if m_page:
            self.the_stack.setCurrentWidget(m_page)
        else:
            m_page = RegisterMember(the_stack=self.the_stack)
            self.the_stack.addWidget(m_page)
            self.the_stack.setCurrentWidget(m_page)

    def prev_page(self):
        add_page = self.the_stack.findChild(AddFromPrev)
        
        if add_page:
            self.the_stack.setCurrentWidget(add_page)
        else:
            add_page = AddFromPrev(the_stack=self.the_stack)
            self.the_stack.addWidget(add_page)
            self.the_stack.setCurrentWidget(add_page)
        
    def on_row_click(self):
        row = self.table_widget.currentRow()
        col = self.table_widget.currentColumn()
        row_data = {}
        headers = ["Name", "ID Number", "Role", "Address", "Status", "Contacts", "Date Joined","Date Of Birth"]

        for column in range(self.table_widget.columnCount()):
            item = self.table_widget.item(row, column)
            if item:
                row_data[headers[column]] = item.text()

        clicked_cell_value = self.table_widget.item(row, col).text()
        # print(f"Clicked Cell: {headers[col]}: {clicked_cell_value}")
        # print("Row Data:", row_data)
        u_profile = UserProfile(member_name=row_data['Name'],the_stack=self.the_stack)
        existing_prof = self.the_stack.findChild(UserProfile)
        if existing_prof:
            self.the_stack.removeWidget(existing_prof)
            existing_prof.deleteLater()
            
        self.the_stack.addWidget(u_profile)
        self.the_stack.setCurrentWidget(u_profile)
        
            

    def load_table_data(self):
        """Load initial data into the QTableWidget"""
        conn = sqlite3.connect("group_management.db")
        cursor = conn.cursor()
        self.data = get_all_members_with_contacts(cursor)
        conn.close()
        self.data = [[m.name,m.id_number,m.role,m.address,m.status,m.contacts,m.date_joined,m.date_of_birth] for m in self.data]
        self.table_widget.setRowCount(len(self.data))
        self.table_widget.setColumnCount(8)  # Adjust based on data
        self.table_widget.setHorizontalHeaderLabels(["Name", "ID Number", "Role", "Address", "Status", "Contacts", "Date Joined", "Date Of Birth"])
        self.table_widget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        for row, (name, id_number, role, address, status, contacts, date_joined, date_of_birth) in enumerate(self.data):
            self.table_widget.setItem(row, 0, QtWidgets.QTableWidgetItem(name))
            self.table_widget.setItem(row, 1, QtWidgets.QTableWidgetItem(id_number))
            self.table_widget.setItem(row, 2, QtWidgets.QTableWidgetItem(role))
            self.table_widget.setItem(row, 3, QtWidgets.QTableWidgetItem(address))
            self.table_widget.setItem(row, 4, QtWidgets.QTableWidgetItem(status))
            self.table_widget.setItem(row, 5, QtWidgets.QTableWidgetItem(str(contacts).replace("[",'').replace("]",'').replace("'",'').replace("'",'')))
            self.table_widget.setItem(row, 6, QtWidgets.QTableWidgetItem(date_joined))
            self.table_widget.setItem(row, 7, QtWidgets.QTableWidgetItem(date_of_birth))


    def filter_table(self):
        """Filter table rows based on search box input"""
        search_text = self.search_box.text().lower()

        for row in range(self.table_widget.rowCount()):
            row_match = False
            for col in range(self.table_widget.columnCount()):
                item = self.table_widget.item(row, col)
                if item and search_text in item.text().lower():
                    row_match = True
                    break

            self.table_widget.setRowHidden(row, not row_match)


