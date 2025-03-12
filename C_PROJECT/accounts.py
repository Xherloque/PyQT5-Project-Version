from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem,
    QScrollArea,  QTableWidget,QFrame, QTableWidgetItem,QDialog,QLineEdit,
    QMessageBox, QDateEdit
)
from PyQt5 import uic
import sys, sqlite3
from database_funcs import add_group_account, get_table_as_object

class GroupFinanceUI(QWidget):
    def __init__(self, the_stack):
        super().__init__()
        self.the_stack = the_stack
        uic.loadUi("C_PROJECT/UI_FILES/group_accounts.ui", self)  # Load the UI file
        self.home_btn.clicked.connect(lambda x: self.the_stack.setCurrentIndex(1))
        self.add_new_acc_btn.clicked.connect(self.add_new_acc)
        self.fill_the_tables()

    def add_new_acc(self):
        dialog = PopupForm()
        if dialog.exec_():  # If the dialog was accepted (Save button clicked)
            account_number, account_name,date_created, balance, description = dialog.save_data()
            #Add em to the database:
            conn = sqlite3.connect("group_management.db")
            cursor = conn.cursor()
            add_group_account(cursor,int(account_number),account_name,
                              date_created,balance,description)
            conn.commit()
            
            all_accs = get_table_as_object(cursor, "group_accounts")
            conn.close()
            
        accounts_table = self.tableWidget
        row_position = accounts_table.rowCount()
        accounts_table.insertRow(row_position)
        accounts_table.setItem(row_position, 0, QTableWidgetItem(account_number))
        accounts_table.setItem(row_position, 1, QTableWidgetItem(account_name))
        accounts_table.setItem(row_position, 2, QTableWidgetItem(date_created))
        accounts_table.setItem(row_position, 3, QTableWidgetItem(balance))
        accounts_table.setItem(row_position, 4, QTableWidgetItem(description))
    
        self.total_accs.setText(f"Total Accounts Balance:   KSH. {sum([ac.balance for ac in all_accs])}")
        self.total_active.setText(f"Total Active Accounts:  {len([a for a in all_accs])} Accounts")
    
    def fill_the_tables(self):
        #Add em to the database:
        conn = sqlite3.connect("group_management.db")
        cursor = conn.cursor()
        all_accs = get_table_as_object(cursor, "group_accounts")
        membs = [tr.name for tr in get_table_as_object(cursor, "members") if tr.role == 'Treasurer']
        conn.close()

        accounts_table = self.tableWidget
        for acc in all_accs:
            data = (acc.account_number, acc.name,acc.created, acc.balance, acc.description)
            row_position = accounts_table.rowCount()
            accounts_table.insertRow(row_position)
            accounts_table.setItem(row_position, 0, QTableWidgetItem(str(data[0])))
            accounts_table.setItem(row_position, 1, QTableWidgetItem(data[1]))
            accounts_table.setItem(row_position, 2, QTableWidgetItem(data[2]))
            accounts_table.setItem(row_position, 3, QTableWidgetItem(str(data[3])))
            accounts_table.setItem(row_position, 4, QTableWidgetItem(data[4]))
        
        self.total_accs.setText(f"Total Accounts Balance:   KSH. {sum([float(ac.balance) for ac in all_accs])}")
        self.total_active.setText(f"Total Active Accounts:  {len([a for a in all_accs])} Accounts")
        self.tresh_edit.setText(membs[0])
        transaction_table = self.tableWidget_2
        transactions = [
            [1001, "2025-03-01", "Deposit", 5000, "ACC001", "Initial group deposit"],
            [1002, "2025-03-02", "Contribution", 1000, "ACC002", "Monthly contribution - John Doe"],
            [1003, "2025-03-03", "Loan Issued", 8000, "ACC003", "Loan to Mary Jane"],
            [1004, "2025-03-04", "Withdrawal", 2000, "ACC001", "Cash withdrawal for expenses"],
            [1005, "2025-03-05", "Loan Repaid", 3000, "ACC003", "Partial loan repayment - Mary Jane"],
            [1006, "2025-03-06", "Deposit", 4500, "ACC004", "Savings deposit - Alex Kim"],
            [1007, "2025-03-07", "Penalty", 500, "ACC002", "Late contribution fee - John Doe"],
            [1008, "2025-03-08", "Contribution", 1200, "ACC005", "Monthly contribution - Alice Brown"],
            [1009, "2025-03-09", "Loan Issued", 10000, "ACC006", "Emergency loan - Robert Smith"],
            [1010, "2025-03-10", "Loan Repaid", 2000, "ACC006", "First installment - Robert Smith"],
            [1011, "2025-03-11", "Deposit", 6000, "ACC007", "Fixed deposit - Lisa Green"],
            [1012, "2025-03-12", "Withdrawal", 1500, "ACC001", "Group meeting expenses"],
            [1013, "2025-03-13", "Contribution", 900, "ACC008", "Monthly contribution - James White"],
            [1014, "2025-03-14", "Loan Repaid", 4000, "ACC003", "Loan repayment - Mary Jane"],
            [1015, "2025-03-15", "Penalty", 300, "ACC005", "Missed meeting fine - Alice Brown"],
            [1016, "2025-03-16", "Deposit", 7000, "ACC009", "Savings deposit - Kevin Blue"],
            [1017, "2025-03-17", "Withdrawal", 2500, "ACC001", "Charity donation"],
            [1018, "2025-03-18", "Contribution", 1100, "ACC010", "Monthly contribution - Susan Clark"],
            [1019, "2025-03-19", "Loan Issued", 5000, "ACC011", "Small business loan - Mark Adams"],
            [1020, "2025-03-20", "Loan Repaid", 1500, "ACC011", "Loan repayment - Mark Adams"],
        ]
        for transaction in transactions:
            row_position = transaction_table.rowCount()
            transaction_table.insertRow(row_position)
            for column, item in enumerate(transaction):
                transaction_table.setItem(row_position, column, QTableWidgetItem(str(item)))




class PopupForm(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add A New Account")
        self.setGeometry(200, 200, 300, 150)

        layout = QVBoxLayout()

        # Label & Input 1
        self.label1 = QLabel("Account Number")
        self.input1 = QLineEdit()
        layout.addWidget(self.label1)
        layout.addWidget(self.input1)


        self.labelm = QLabel("Account Name")
        self.inputm = QLineEdit()
        layout.addWidget(self.labelm)
        layout.addWidget(self.inputm)
        
        # Label & Input 2
        self.label2 = QLabel("Date Created")
        self.input2 = QDateEdit()
        layout.addWidget(self.label2)
        layout.addWidget(self.input2)
        
        
        # Label & Input 3
        self.label3 = QLabel("Balance")
        self.input3 = QLineEdit()
        layout.addWidget(self.label3)
        layout.addWidget(self.input3)
        
        
        
        # Label & Input 3
        self.label4 = QLabel("Description")
        self.input4 = QLineEdit()
        layout.addWidget(self.label4)
        layout.addWidget(self.input4)

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
        account_number = self.input1.text().strip()
        account_name = self.inputm.text().strip()
        date_created = self.input2.date().toString("yyyy-MM-dd")
        balance = self.input3.text().strip()
        description = self.input4.text().strip()
        
        if not account_number and not account_name and not date_created and not balance:
            QMessageBox.critical(self, "Error", "All fields must be filled!")
            return
        else:
            self.accept()  # Close dialog
            return [account_number,account_name,date_created,balance,description]
