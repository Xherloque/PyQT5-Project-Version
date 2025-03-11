from PyQt5 import QtWidgets, QtGui, QtCore


class ArrearsPage(QtWidgets.QWidget):
    def __init__(self, the_stack):
        super().__init__()
        self.the_stack = the_stack
        self.setWindowTitle("Arrears Page")
        self.setGeometry(100, 100, 1000, 600)  # Default size
        self.setStyleSheet("background-color: #f4f4f4;")

        # Main Layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 100)  # Leaves space at the bottom

        # Navigation Bar
        self.nav_bar = QtWidgets.QHBoxLayout()
        title_label = QtWidgets.QLabel("Arrears")
        title_label.setStyleSheet("padding: 18px 15px; font-weight: bold; font-size: 24px;")
        
        add_new_btn = QtWidgets.QPushButton("Record New Arrear")
        add_new_btn.setStyleSheet("padding: 8px 15px; font-weight: bold;")
        add_new_btn.clicked.connect(self.record_new_arrear)
        
        search_box = QtWidgets.QLineEdit("Search")
        search_box.setStyleSheet("padding: 8px 15px;")
        home_btn = QtWidgets.QPushButton("Home")
        home_btn.setStyleSheet("padding: 8px 15px; font-weight: bold;")
        home_btn.clicked.connect(lambda x: self.the_stack.setCurrentIndex(1))
        for btn in [title_label, add_new_btn, search_box, home_btn]:
            self.nav_bar.addWidget(btn)
        
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
            {"name": "John Doe", "total": "Ksh.500", "status": "Pending", "records": [
                {"id": 1, "amount": "Ksh.200", "due": "2024-03-10", "desc": "Missed Feb Meeting Contribution",
                 "paid": "Ksh.50", "remaining": "Ksh.150", "status": "Partially Paid"},
                {"id": 2, "amount": "Ksh.300", "due": "2024-04-15", "desc": "Missed March Loan Repayment",
                 "paid": "Ksh.0", "remaining": "Ksh.300", "status": "Unpaid"}
            ]},
            {"name": "Jane Smith", "total": "Ksh.150", "status": "Partially Paid", "records": [
                {"id": 1, "amount": "Ksh.150", "due": "2024-02-25", "desc": "Missed January Burial Contribution",
                 "paid": "Ksh.50", "remaining": "Ksh.100", "status": "Partially Paid"}
            ]}
        ]

        # Populate Arrears
        for member in arrears_data:
            self.add_member_arrears(member)

        self.setLayout(main_layout)

    def record_new_arrear(self):
        """ Opens the RecordNewArrear dialog """
        dialog = RecordNewArrear(self)
        dialog.exec_()

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
            
            summary = (f"Amount Due: {record['amount']} | Due Date: {record['due']}\n"
                       f"Status: {record['status']}")
            summary_label = QtWidgets.QLabel(summary)
            summary_label.setWordWrap(True)
            record_layout.addWidget(summary_label)
            
            # Expandable Details Section
            details_widget = QtWidgets.QWidget()
            details_layout = QtWidgets.QVBoxLayout(details_widget)

            details_layout.addWidget(QtWidgets.QLabel(f"📝 Description: {record['desc']}"))
            details_layout.addWidget(QtWidgets.QLabel(f"💰 Amount Paid: {record['paid']}"))
            details_layout.addWidget(QtWidgets.QLabel(f"🔻 Amount Remaining: {record['remaining']}"))

            details_widget.setLayout(details_layout)
            details_widget.setVisible(False)  # Starts hidden
            
            # View Details Button
            view_button = QtWidgets.QPushButton("View Full Details")
            view_button.setStyleSheet("background-color: #28a745; color: white; padding: 5px; border-radius: 3px;")
            view_button.setCheckable(True)
            view_button.toggled.connect(lambda checked, widget=details_widget: widget.setVisible(checked))
            
            record_layout.addWidget(view_button)
            record_layout.addWidget(details_widget)
            
            record_box.setLayout(record_layout)
            member_layout.addWidget(record_box)
        
        member_box.setLayout(member_layout)
        self.scroll_layout.addWidget(member_box)


class RecordNewArrear(QtWidgets.QDialog):
    """ Dialog for recording a new arrear """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Record New Arrear")
        self.setFixedSize(400, 320)
        self.setStyleSheet("""
            QLabel { font-size: 14px; font-weight: bold; }
            QLineEdit, QDateEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton {
                padding: 8px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #ddd;
            }
        """)

        layout = QtWidgets.QVBoxLayout(self)

        # Title Label
        title_label = QtWidgets.QLabel("Enter Arrear Details")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title_label)

        # Form Fields
        self.member_name = QtWidgets.QLineEdit()
        self.member_name.setPlaceholderText("Member Name")

        self.amount = QtWidgets.QLineEdit()
        self.amount.setPlaceholderText("Amount (Ksh.)")

        # ✅ Align Label & DateEdit Horizontally
        date_layout = QtWidgets.QHBoxLayout()
        date_label = QtWidgets.QLabel("Due Date:")
        self.due_date = QtWidgets.QDateEdit()
        self.due_date.setCalendarPopup(True)
        self.due_date.setFixedWidth(200)
        self.due_date.setDate(QtCore.QDate.currentDate())
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.due_date)
        date_layout.addStretch()  # Keeps everything aligned properly

        self.description = QtWidgets.QLineEdit()
        self.description.setPlaceholderText("Description")

        self.paid_amount = QtWidgets.QLineEdit()
        self.paid_amount.setPlaceholderText("Amount Paid")

        # Buttons
        btn_layout = QtWidgets.QHBoxLayout()
        save_btn = QtWidgets.QPushButton("Save")
        save_btn.setStyleSheet("background-color: #28a745; color: white;")
        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.setStyleSheet("background-color: #dc3545; color: white;")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)

        # Add widgets to layout
        layout.addWidget(self.member_name)
        layout.addWidget(self.amount)
        layout.addLayout(date_layout)  # ✅ Properly aligned date field
        layout.addWidget(self.description)
        layout.addWidget(self.paid_amount)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
