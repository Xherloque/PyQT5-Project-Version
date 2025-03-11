from PyQt5 import QtWidgets, QtCore

class ContributionsPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Make the window full-screen
        self.setFixedSize(1366,768)

        # Layout to hold everything
        main_layout = QtWidgets.QVBoxLayout(self)
        # --- Fixed Navigation Bar ---
        self.navbar = QtWidgets.QWidget()
        self.navbar.setStyleSheet("background-color: #2C3E50;")
        self.navbar_layout = QtWidgets.QHBoxLayout(self.navbar)
        self.navbar_layout.setContentsMargins(0, 0, 0, 0)

        self.home_button = QtWidgets.QPushButton("Home")
        self.home_button.setStyleSheet("color: white; background-color: #34495E; padding: 5px;")
        self.navbar_layout.addWidget(self.home_button)
        self.navbar_layout.addStretch()

        main_layout.addWidget(self.navbar)


                # Scroll area setup
        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)  # Allow resizing
        self.scroll_content = QtWidgets.QWidget()  # Holds all meetings
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scroll_content)

        # Ensure layout expands properly
        self.scroll_layout.setAlignment(QtCore.Qt.AlignTop)
        self.scroll_layout.addStretch()

        # Add some sample meetings
    # --- Populate Meetings ---
        for i in range(1, 16):
            self.add_meeting(f"Meeting {i}", "2025-03-01", "$500", "$600", "Cash")
        # Force scroll content to adjust its size
        self.scroll_content.adjustSize()
        self.scroll_content.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        # Add scroll content to scroll area
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)

        # Add to the main layout
        main_layout.addWidget(self.scroll_area)


    def add_meeting(self, meeting_name, date, total_contributions, required_amount, payment_type):
        meeting_widget = QtWidgets.QWidget()
        meeting_layout = QtWidgets.QVBoxLayout(meeting_widget)

        # Meeting Header
        meeting_header = QtWidgets.QHBoxLayout()
        meeting_label = QtWidgets.QLabel(f"{meeting_name} - {date}")
        meeting_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        meeting_header.addWidget(meeting_label)
        meeting_header.addStretch()
        
        view_button = QtWidgets.QPushButton("View Meeting")
        view_button.setStyleSheet("background-color: #2980B9; color: white; padding: 5px;")
        view_button.clicked.connect(self.open_meeting_details)
        meeting_header.addWidget(view_button)
        
        meeting_layout.addLayout(meeting_header)
        
        # Meeting Details
        details_label = QtWidgets.QLabel(f"Total Contributions: {total_contributions}\nRequired Amount: {required_amount}\nPayment Type: {payment_type}")
        details_label.setStyleSheet("padding: 5px;")
        meeting_layout.addWidget(details_label)

        meeting_widget.setStyleSheet("border: 1px solid gray; padding: 10px; margin-bottom: 10px;")
        self.scroll_layout.addWidget(meeting_widget)

    def open_meeting_details(self):
        placeholder_screen = QtWidgets.QMessageBox()
        placeholder_screen.setWindowTitle("Meeting Details")
        placeholder_screen.setText("This is a placeholder for the meeting details page.")
        placeholder_screen.exec_()
    
        
    # Run the app
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = ContributionsPage()
    window.show()
    sys.exit(app.exec_())
