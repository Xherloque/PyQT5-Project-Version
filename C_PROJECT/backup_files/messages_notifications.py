from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTabWidget, QLabel,
    QTextEdit, QLineEdit, QComboBox, QFileDialog, QDateTimeEdit, QListWidget, QListWidgetItem,
    QScrollArea,QFrame
)
import sys

class MessagesUI(QWidget):
    def __init__(self, the_stack):
        super().__init__()
        self.the_stack = the_stack
        self.setWindowTitle("Messages & Notifications")
        self.setGeometry(200, 100, 800, 500)
        
        main_layout = QVBoxLayout()
        
        # Navigation Bar
        nav_bar = QHBoxLayout()
        self.title_label = QLabel("Messages & Notifications")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        home_button = QPushButton("Home")
        home_button.setFixedSize(100, 35)
        home_button.clicked.connect(lambda x: self.the_stack.setCurrentIndex(1))
        nav_bar.addWidget(self.title_label)
        nav_bar.addStretch()
        nav_bar.addWidget(home_button)
        
        main_layout.addLayout(nav_bar)
        
        # Tabs for different sections
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("font-size: 14px;")
        self.tabs.addTab(self.create_messages_tab(), "Messages & Notifications")
        self.tabs.addTab(self.create_send_sms_tab(), "Send SMS")
        self.tabs.addTab(self.create_send_email_tab(), "Send Email")
        
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)
    
    def create_messages_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 100)
        # Tabs for Inbox, Sent, Alerts
        top_buttons_layout = QHBoxLayout()
        self.inbox_btn = QPushButton("Inbox")
        self.sent_btn = QPushButton("Sent")
        self.alerts_btn = QPushButton("Alerts")
        
        for btn in [self.inbox_btn, self.sent_btn, self.alerts_btn]:
            btn.setFixedSize(120, 35)
            btn.setStyleSheet("background-color: #2196F3; color: white; border-radius: 5px;")
            btn.clicked.connect(self.filter_messages)
        
        top_buttons_layout.addWidget(self.inbox_btn)
        top_buttons_layout.addWidget(self.sent_btn)
        top_buttons_layout.addWidget(self.alerts_btn)
        layout.addLayout(top_buttons_layout)
        
        # Scrollable message area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_container = QWidget()
        self.message_layout = QVBoxLayout(scroll_container)
        self.message_layout.setSpacing(10)
        
        for i in range(10):
            self.add_message(sent_from=f"Sender {i+1}", message=f"This is message {i+1}")
        
        scroll_area.setWidget(scroll_container)
        layout.addWidget(scroll_area)
        tab.setLayout(layout)
        return tab
    
    def add_message(self, sent_from, message):
        message_frame = QFrame()
        message_frame.setStyleSheet("border: 1px solid #ccc; background-color: white; padding: 10px; border-radius: 5px;")
        frame_layout = QVBoxLayout(message_frame)
        
        sender_label = QLabel(f"New Message From: {sent_from}")
        sender_label.setStyleSheet("font-weight: bold; color: #333;")
        frame_layout.addWidget(sender_label)
        
        message_display = QTextEdit(message)
        message_display.setFixedHeight(80)
        message_display.setReadOnly(True)
        frame_layout.addWidget(message_display)
        
        buttons_layout = QHBoxLayout()
        reply_btn = QPushButton("Reply")
        mark_read_btn = QPushButton("Mark as Read")
        delete_btn = QPushButton("Delete")
        
        for btn in [reply_btn, mark_read_btn, delete_btn]:
            btn.setFixedSize(130, 40)
            btn.setStyleSheet("background-color: #FF9800; color: white; border-radius: 5px;")
        
        buttons_layout.addWidget(reply_btn)
        buttons_layout.addWidget(mark_read_btn)
        buttons_layout.addWidget(delete_btn)
        frame_layout.addLayout(buttons_layout)
        
        self.message_layout.addWidget(message_frame)
    
    def filter_messages(self):
        sender = self.sender()
        category = sender.text()
        print(f"Filtering: {category}")  # Placeholder functionality
        
    def create_send_sms_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 100)
        
        layout.addWidget(QLabel("To:"))
        self.sms_recipient = QLineEdit()
        layout.addWidget(self.sms_recipient)
        
        layout.addWidget(QLabel("Send to Group:"))
        self.sms_group = QComboBox()
        self.sms_group.addItems(["-- Select Group --", "Active Members", "Loan Defaulters"])
        layout.addWidget(self.sms_group)
        
        layout.addWidget(QLabel("Select Template:"))
        self.sms_template = QComboBox()
        self.sms_template.addItems(["-- Choose Template --", "Payment Reminder", "Meeting Notice"])
        layout.addWidget(self.sms_template)
        
        layout.addWidget(QLabel("Message:"))
        self.sms_message = QTextEdit()
        layout.addWidget(self.sms_message)
        
        self.sms_attachment_btn = QPushButton("Attach File")
        layout.addWidget(self.sms_attachment_btn)
        
        self.sms_schedule = QDateTimeEdit()
        layout.addWidget(QLabel("Schedule Send:"))
        layout.addWidget(self.sms_schedule)
        
        send_buttons_layout = QHBoxLayout()
        send_now_btn = QPushButton("Send Now")
        schedule_btn = QPushButton("Schedule SMS")
        send_buttons_layout.addWidget(send_now_btn)
        send_buttons_layout.addWidget(schedule_btn)
        layout.addLayout(send_buttons_layout)
        
        tab.setLayout(layout)
        return tab
    
    def create_send_email_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 100)
        
        layout.addWidget(QLabel("To:"))
        self.email_recipient = QLineEdit()
        layout.addWidget(self.email_recipient)
        
        layout.addWidget(QLabel("Send to Group:"))
        self.email_group = QComboBox()
        self.email_group.addItems(["-- Select Group --", "Active Members", "Loan Defaulters"])
        layout.addWidget(self.email_group)
        
        layout.addWidget(QLabel("Subject:"))
        self.email_subject = QLineEdit()
        layout.addWidget(self.email_subject)
        
        layout.addWidget(QLabel("Select Template:"))
        self.email_template = QComboBox()
        self.email_template.addItems(["-- Choose Template --", "Payment Reminder", "Meeting Notice"])
        layout.addWidget(self.email_template)
        
        layout.addWidget(QLabel("Message:"))
        self.email_message = QTextEdit()
        layout.addWidget(self.email_message)
        
        self.email_attachment_btn = QPushButton("Attach File")
        layout.addWidget(self.email_attachment_btn)
        
        self.email_schedule = QDateTimeEdit()
        layout.addWidget(QLabel("Schedule Send:"))
        layout.addWidget(self.email_schedule)
        
        send_buttons_layout = QHBoxLayout()
        send_now_btn = QPushButton("Send Now")
        schedule_btn = QPushButton("Schedule Email")
        send_buttons_layout.addWidget(send_now_btn)
        send_buttons_layout.addWidget(schedule_btn)
        layout.addLayout(send_buttons_layout)
        
        tab.setLayout(layout)
        return tab
    
