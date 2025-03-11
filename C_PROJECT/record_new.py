from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QDateEdit, QTimeEdit, 
    QTextEdit, QCheckBox, QScrollArea, QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout, QFrame
,QStyledItemDelegate,QDialog, QMessageBox
)
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt,QDateTime, QSize, pyqtSignal
from PyQt5 import uic
import sys, sqlite3, datetime
from database_funcs import get_table_as_object,Meeting, get_member_by_name

def tout_members():
    conn = sqlite3.connect("group_management.db")
    cursor = conn.cursor()
    mbs = get_table_as_object(cursor,"members")
    conn.close()
    return mbs

def memb_by_name(memba):
    conn = sqlite3.connect("group_management.db")
    cursor = conn.cursor()
    mbs = get_member_by_name(cursor,memba)
    conn.close()
    return mbs

class CheckBoxDelegate(QStyledItemDelegate):
    """Custom delegate to make checkboxes larger"""
    def paint(self, painter, option, index):
        option.rect.setSize(QSize(40, 40))  # Adjust checkbox size
        super().paint(painter, option, index)


class RecordMeetingScreen(QWidget):
    meeting_saving_ended = pyqtSignal()
    def __init__(self, the_stack):
        super().__init__()
        uic.loadUi("C_PROJECT/UI_FILES/record_new_meeting.ui",self)
        self.the_stack = the_stack
        self.meeting_save_dict = {"proposals":[],
                                  "attendance":[]} #    {"member_id": 4, "description": "Introduce a voluntary emergency fund"}],
        self.home_btn.clicked.connect(lambda x: self.the_stack.setCurrentIndex(1))
        self.save_meeting_btn.clicked.connect(self.saveMeeting)
        # self.meeting_date.setDisplayFormat("dd/MM/yyyy")
        self.tableWidget.cellChanged.connect(self.update_checked_count)
        self.fill_attendance_table(test_data=[[n.name, Qt.Unchecked, Qt.Unchecked] for n in tout_members()])
        self.fill_contributions_table()
        #  Connect cellChanged signal to validate and update total
        self.set_current_date_time()
        self.tableWidget_2.cellChanged.connect(self.validate_and_update_total)
        self.mark_all_btn.clicked.connect(self.mark_all_attendance)
        self.new_proposal_btn.clicked.connect(self.open_proposal_dialog)
            
    def set_current_date_time(self):
        """Sets the dateEdit and timeEdit to the current date and time."""
        now = datetime.datetime.now()
        qdatetime = QDateTime(now.year, now.month, now.day, now.hour, now.minute, now.second)
        self.meeting_date.setDateTime(qdatetime)
        self.meeting_time_edit.setDateTime(qdatetime)
        
    def open_proposal_dialog(self):
        dialog = PopupForm()
        if dialog.exec_():
            mb, pr, apr = dialog.save_data()
            lb1_text = f"-  <b>Proposal:</b> {pr} "
            lb2_text = f"<b>By:</b> {mb} ,<b> Approved:</b> {apr}"
            lb1 = QLabel(lb1_text)
            lb2 = QLabel(lb2_text)
            self.formLayout.addRow(lb1,lb2)
            
            self.meeting_save_dict["proposals"].append({
                "member_id":memb_by_name(mb).member_id,
                "description":f"Proposal: {pr}, Approved: {apr}"
            })
            
            
#TODO: Fill these details to the page then to save data....              
    
    def mark_all_attendance(self):
        test_data=[[n.name, Qt.Checked, Qt.Checked] for n in tout_members()]
        self.tableWidget.setRowCount(0)  # Removes all rows but keeps headers
        self.fill_attendance_table(test_data)
        
    def collect_attendance(self):
        """Collects (member, present/absent, on_time/late) from the table."""
        attendance_data = []
        for row in range(self.tableWidget.rowCount()):
            name_item = self.tableWidget.item(row, 0)  # Member Name
            attended_cb = self.tableWidget.cellWidget(row, 1)  # Attended checkbox
            on_time_cb = self.tableWidget.cellWidget(row, 2)  # On Time checkbox

            member = name_item.text().strip() if name_item else ""
            present = "Present" if attended_cb and attended_cb.isChecked() else "Absent"
            on_time = "On Time" if on_time_cb and on_time_cb.isChecked() else "" if present == "Absent" else "Late"

            attendance_data.append((member, present, on_time))

        return attendance_data
       
    def fill_attendance_table(self, test_data):
        """Fills attendance table with members and checkboxes for attendance and punctuality"""
        # self.test_data = [
        #     [n, Qt.Unchecked, Qt.Unchecked] for n in member_data
        # ]

        self.tableWidget.setRowCount(len(test_data))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["MEMBER", "ATTENDED", "ON TIME"])

        # Apply custom delegate for bigger checkboxes
        self.tableWidget.setItemDelegateForColumn(1, CheckBoxDelegate(self.tableWidget))
        self.tableWidget.setItemDelegateForColumn(2, CheckBoxDelegate(self.tableWidget))

        for row, (member, attended, on_time) in enumerate(test_data):
            # Member Name (Read-only)
            name_item = QTableWidgetItem(member)
            name_item.setFlags(Qt.ItemIsEnabled)
            self.tableWidget.setItem(row, 0, name_item)

            # Attended Checkbox
            attended_item = QTableWidgetItem()
            attended_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            attended_item.setCheckState(attended)
            self.tableWidget.setItem(row, 1, attended_item)

            # On Time Checkbox
            on_time_item = QTableWidgetItem()
            on_time_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            on_time_item.setCheckState(on_time)
            self.tableWidget.setItem(row, 2, on_time_item)

        # Increase row height for better checkbox visibility
        for row in range(self.tableWidget.rowCount()):
            self.tableWidget.setRowHeight(row, 40)  # Adjust row height
    
    def update_checked_count(self):
        """Counts checked checkboxes in the 'Attended' column and lists checked members"""
        checked_count = 0
        checked_names = []

        for row in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row, 1)  # 'Attended' column
            s_item = self.tableWidget.item(row, 2)  # 'Attended' column
            if item and item.checkState() == Qt.Checked:
                checked_count += 1
                checked_names.append((self.tableWidget.item(row, 0).text(),
                                      "On Time" if s_item and s_item.checkState() == Qt.Checked else "Late"))  # Get the name

        # print(checked_names)
        self.meeting_save_dict['attendance'] = checked_names
        # Update label
        self.checked_count_label.setText(f"TOTAL ATTENDANCE :     {checked_count} OUT OF {len(tout_members())}")

    def fill_contributions_table(self):
        """Fills contributions table with members, amounts, and payment method"""
        test_data = [
            [o.name, "", "Cash"] for o in tout_members() 
        ]#'Cash', 'Bank Transfer', 'Mobile Payment'

        self.tableWidget_2.setRowCount(len(test_data))
        self.tableWidget_2.setColumnCount(3)
        self.tableWidget_2.setHorizontalHeaderLabels(["MEMBER", "AMOUNT", "PAID BY"])

        for row, (member, amount, payment_method) in enumerate(test_data):
            # Member Name
            name_item = QTableWidgetItem(member)
            # name_item.setFlags(Qt.ItemIsEnabled)  # Read-only
            self.tableWidget_2.setItem(row, 0, name_item)

            # Amount
            amount_item = QTableWidgetItem(amount)
            # amount_item.setFlags(Qt.ItemIsEnabled)
            self.tableWidget_2.setItem(row, 1, amount_item)

            # Paid By
            payment_item = QTableWidgetItem(payment_method)
            # payment_item.setFlags(Qt.ItemIsEnabled)
            self.tableWidget_2.setItem(row, 2, payment_item)
        self.update_total_contributions()  # Initialize total

    def validate_and_update_total(self, row, column):
        """Validates input in the AMOUNT column and updates the total dynamically."""
        if column == 1:  # "AMOUNT" column
            item = self.tableWidget_2.item(row, column)
            if item:
                text = item.text().strip()

                if not text.isdigit() or int(text) < 0:  # Invalid input
                    self.tableWidget_2.blockSignals(True)  # Stop recursion
                    self.tableWidget_2.setItem(row, column, QTableWidgetItem(""))  # Clear invalid input
                    self.tableWidget_2.blockSignals(False)  # Resume signals

                self.update_total_contributions()  # Recalculate total

    def update_total_contributions(self):
        """Calculates and updates the total contributions."""
        total = 0
        for row in range(self.tableWidget_2.rowCount()):
            item = self.tableWidget_2.item(row, 1)  # AMOUNT column
            if item and item.text().isdigit():
                total += int(item.text())

        # Update label
        self.total_label.setText(f"TOTAL CONTRIBUTION: KSH. {total}")
    
    
    def collect_contributions(self):
        """Collects (member, amount, paid_by) from the table when 'Save' is clicked."""
        contributions = []
        for row in range(self.tableWidget_2.rowCount()):
            name_item = self.tableWidget_2.item(row, 0)
            amount_item = self.tableWidget_2.item(row, 1)
            paid_by_item = self.tableWidget_2.item(row, 2)

            # Get text, default to empty string if None
            member = name_item.text().strip() if name_item else ""
            amount = amount_item.text().strip() if amount_item else ""
            paid_by = paid_by_item.text().strip() if paid_by_item else ""

            # Append tuple (even if some fields are empty)
            contributions.append((member, amount, paid_by))

        return contributions
        
    def saveMeeting(self):
        meeting_form = Meeting(
            meeting_label=self.meeting_label.text(),
            meeting_date=self.meeting_date.date().toString("yyyy-MM-dd"),
            meeting_time=self.meeting_time_edit.time().toString("HH:mm"),#TODO: Does this have toString?,
            time_ended=self.time_ended.time().toString("HH:mm"),
            agenda=self.agenda.toPlainText(),
            facilitator=self.facilitator_edit.text(),
            proposals=self.meeting_save_dict["proposals"],
            attendance=[(memb_by_name(x).member_id,y) for x,y in self.meeting_save_dict['attendance']],#Member,present,on_time
            contributions=[{"member_id":memb_by_name(mmb).member_id,"amount":amm, "payment_method":pdb, "contribution_date": self.meeting_date.date().toString("yyyy-MM-dd")}
                           for mmb, amm, pdb in self.collect_contributions() if amm and pdb]#member, amount,paid by
        )
        conn = sqlite3.connect("group_management.db")
        cursor = conn.cursor()
        meeting_form.save_meeting(cursor=cursor)
        conn.commit()
        conn.close()
        QMessageBox.critical(self, "Success", "Meeting Saved Successfully!!")
        self.meeting_saving_ended.emit()
        self.the_stack.setCurrentIndex(5)
        #----------------------------------------------
        #      Clear Everything
        self.meeting_label.setText("")
        self.fill_attendance_table(test_data=[[n.name, Qt.Unchecked, Qt.Unchecked] for n in tout_members()])
        self.fill_contributions_table()
        self.agenda.setPlainText("")
        #Delete proposals
        while self.formLayout.count():
            item = self.formLayout.takeAt(0)  # Take and remove the first item
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()  # Schedule the widget for deletion
        self.facilitator_edit.setText("")
        
        #========== Change the on going text in homepage ==============#
        hm_page = self.the_stack.widget(1)
        if hm_page:
            hm_page.on_going_combo.clear()
            hm_page.on_going_combo.addItem("No Meeting In Progress")
        
         
    
    
    
class PopupForm(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add Proposal")
        self.setGeometry(200, 200, 300, 150)

        layout = QVBoxLayout()

        # Label & Input 1
        self.label1 = QLabel("Proposal By: ")
        self.input1 = QLineEdit()
        layout.addWidget(self.label1)
        layout.addWidget(self.input1)


        self.labelm = QLabel("Proposal: ")
        self.inputm = QLineEdit()
        layout.addWidget(self.labelm)
        layout.addWidget(self.inputm)
        
        self.checkbox = QCheckBox("Approved")
        self.checkbox.setStyleSheet("QCheckBox::indicator { width: 25px; height: 25px; }")
        layout.addWidget(self.checkbox)
        
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
        member = self.input1.text().strip()
        proposal = self.inputm.text().strip()
        approved = self.checkbox.isChecked()
        
        if not member and not proposal and not approved:
            QMessageBox.critical(self, "Error", "All fields must be filled!")
            return
        else:
            if member in [g.name for g in tout_members()]:
                self.accept()  # Close dialog
                return [member, proposal, approved]
            else:
                QMessageBox.critical(self, "Error", "Member Must Be From The Group")
                return