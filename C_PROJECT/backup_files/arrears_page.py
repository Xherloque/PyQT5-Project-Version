from PyQt5 import QtWidgets, QtGui

class ArrearsPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Arrears Page")
        self.setGeometry(100, 100, 1000, 600)  # Default size
        self.setStyleSheet("background-color: #f4f4f4;")

        # Main Layout
        main_layout = QtWidgets.QVBoxLayout(self)

        # Navigation Bar
        self.nav_bar = QtWidgets.QHBoxLayout()
        self.add_nav_button("Home", main_layout)
        self.add_nav_button("Contributions", main_layout)
        self.add_nav_button("Loans & Debts", main_layout)
        self.add_nav_button("Arrears", main_layout)
        self.add_nav_button("Meetings", main_layout)
        self.add_nav_button("More", main_layout)
        main_layout.addLayout(self.nav_bar)

        # Scroll Area Setup
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll_area)

        # Sample Data for Arrears (Could be from a database)
        arrears_data = [
            {"name": "John Doe", "total": "$500", "status": "Pending", "records": [
                {"id": 1, "amount": "$200", "due": "2024-03-10", "desc": "Missed Feb Meeting Contribution", "paid": "$50", "remaining": "$150", "status": "Partially Paid"},
                {"id": 2, "amount": "$300", "due": "2024-04-15", "desc": "Missed March Loan Repayment", "paid": "$0", "remaining": "$300", "status": "Unpaid"}
            ]},
            {"name": "Jane Smith", "total": "$150", "status": "Partially Paid", "records": [
                {"id": 1, "amount": "$150", "due": "2024-02-25", "desc": "Missed January Burial Contribution", "paid": "$50", "remaining": "$100", "status": "Partially Paid"}
            ]},
            {"name": "John Doe", "total": "$500", "status": "Pending", "records": [
                {"id": 1, "amount": "$200", "due": "2024-03-10", "desc": "Missed Feb Meeting Contribution", "paid": "$50", "remaining": "$150", "status": "Partially Paid"},
                {"id": 2, "amount": "$300", "due": "2024-04-15", "desc": "Missed March Loan Repayment", "paid": "$0", "remaining": "$300", "status": "Unpaid"}
            ]},
            {"name": "John Doe", "total": "$500", "status": "Pending", "records": [
                {"id": 1, "amount": "$200", "due": "2024-03-10", "desc": "Missed Feb Meeting Contribution", "paid": "$50", "remaining": "$150", "status": "Partially Paid"},
                {"id": 2, "amount": "$300", "due": "2024-04-15", "desc": "Missed March Loan Repayment", "paid": "$0", "remaining": "$300", "status": "Unpaid"}
            ]},
        ]

        # Populate Arrears
        for member in arrears_data:
            self.add_member_arrears(member)

        self.setLayout(main_layout)

    def add_nav_button(self, text, layout):
        button = QtWidgets.QPushButton(text)
        button.setFixedHeight(40)
        button.setStyleSheet("background-color: #0078D7; color: white; border-radius: 5px;")
        self.nav_bar.addWidget(button)

    def add_member_arrears(self, member):
        # Member Header
        member_box = QtWidgets.QGroupBox(f"Member: {member['name']} | Total Arrears: {member['total']} | Status: {member['status']}")
        member_box.setStyleSheet("font-weight: bold; background-color: #e0e0e0; padding: 10px;")
        member_layout = QtWidgets.QVBoxLayout()

        # Arrear Records
        for record in member["records"]:
            record_box = QtWidgets.QGroupBox(f"Arrear Record #{record['id']}")
            record_box.setStyleSheet("background-color: white; padding: 5px; border-radius: 5px;")
            record_layout = QtWidgets.QVBoxLayout()
            
            details = (f"Amount Due: {record['amount']} | Due Date: {record['due']}\n"
                       f"Description: {record['desc']}\n"
                       f"Amount Paid: {record['paid']} | Remaining: {record['remaining']}\n"
                       f"Status: {record['status']}")
            label = QtWidgets.QLabel(details)
            label.setWordWrap(True)
            record_layout.addWidget(label)
            
            # View Details Button
            view_button = QtWidgets.QPushButton("View Full Details")
            view_button.setStyleSheet("background-color: #28a745; color: white; padding: 5px; border-radius: 3px;")
            record_layout.addWidget(view_button)
            record_box.setLayout(record_layout)
            
            member_layout.addWidget(record_box)
        
        member_box.setLayout(member_layout)
        self.scroll_layout.addWidget(member_box)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = ArrearsPage()
    window.show()
    sys.exit(app.exec_())
