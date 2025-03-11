from PyQt5 import QtWidgets, QtCore
import random

class ContributionsPage(QtWidgets.QWidget):
    def __init__(self, the_stack):
        super().__init__()
        self.the_stack = the_stack
        self.setWindowTitle("Contributions Page")
        self.setGeometry(100, 100, 900, 650)

        # Main layout
        self.main_layout = QtWidgets.QVBoxLayout(self)

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
        members = ["Alice", "Bob", "Charlie", "Dave", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy"]
        payment_types = ["Cash", "Bank", "Mobile Money"]

        def generate_contributions():
            num_contributions = random.randint(2, 5)
            return [(random.choice(members), f"${random.randint(50, 300)}", random.choice(payment_types))
                    for _ in range(num_contributions)]

        self.meetings_data = []
        for i in range(1, 6):
            self.meetings_data.append({
                "meeting": f"Meeting {i}",
                "total": f"${random.randint(400, 800)}",
                "required": f"${random.randint(600, 1000)}",
                "type": random.choice(payment_types),
                "date": f"2025-03-{random.randint(1, 30):02d}",
                "contributions": generate_contributions()
            })

        # Generate Meetings Section
        for meeting in self.meetings_data:
            meeting_box = QtWidgets.QGroupBox(meeting["meeting"])
            meeting_box.setStyleSheet("""
                background-color: #ecf0f1;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            """)
            meeting_layout = QtWidgets.QVBoxLayout()

            meeting_details = f"📅 {meeting['date']} | 💰 Total: {meeting['total']} | Required: {meeting['required']} | Type: {meeting['type']}"
            meeting_label = QtWidgets.QLabel(meeting_details)
            meeting_label.setStyleSheet("font-size: 14px; font-weight: normal; padding-bottom: 8px;")
            meeting_layout.addWidget(meeting_label)

            # Table for Contributions
            table = QtWidgets.QTableWidget()
            table.setColumnCount(3)
            table.setHorizontalHeaderLabels(["Member", "Amount", "Payment Type"])
            table.setRowCount(len(meeting["contributions"]))
            table.setStyleSheet("border: 1px solid #bdc3c7;")

            # Resize columns
            table.setColumnWidth(0, 80)  # Increase Member column
            table.setColumnWidth(1, 40)  # Increase Amount column
            table.setColumnWidth(2, 60)  # Increase Payment Type column

            # Auto-resize to fit content
            table.resizeColumnsToContents()

            # Stretch columns to fill table width
            header = table.horizontalHeader()
            header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

            # Fill Table Data
            for row, (name, amount, pay_type) in enumerate(meeting["contributions"]):
                table.setItem(row, 0, QtWidgets.QTableWidgetItem(name))
                table.setItem(row, 1, QtWidgets.QTableWidgetItem(amount))
                table.setItem(row, 2, QtWidgets.QTableWidgetItem(pay_type))
            
            table.setAlternatingRowColors(True)
            table.setStyleSheet("alternate-background-color: #f8f9fa; background-color: #ffffff;")

            meeting_layout.addWidget(table)

            # View Meeting Button
            view_button = QtWidgets.QPushButton("📄 View Meeting")
            view_button.setStyleSheet("""
                background-color: #27ae60;
                color: white;
                padding: 8px 15px;
                border-radius: 8px;
                font-weight: bold;
            """)
            view_button.setCursor(QtCore.Qt.PointingHandCursor)

            meeting_layout.addWidget(view_button)
            meeting_box.setLayout(meeting_layout)
            self.scroll_layout.addWidget(meeting_box)

        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)
