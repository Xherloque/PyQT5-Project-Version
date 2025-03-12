from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTabWidget, QLabel,
    QTextEdit, QLineEdit, QComboBox, QFileDialog, QDateTimeEdit, QListWidget, QListWidgetItem,
    QScrollArea,QFrame
)
from PyQt5 import uic
import sys, random

class MessagesUI(QWidget):
    def __init__(self, the_stack):
        super().__init__()
        uic.loadUi("C_PROJECT/UI_FILES/messages.ui",self)
        self.the_stack = the_stack
        # Scrollable message area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_container = QWidget()
        self.message_layout = QVBoxLayout(scroll_container)
        self.message_layout.setSpacing(10)
        self.home_btn.clicked.connect(lambda x: self.the_stack.setCurrentIndex(1))
        # self.settings_btn.clicked.connect() --> Go to settings
        for i in range(12):
            #Test Type
            test_type = ["Inbox", "Sent", "Alert", "Scheduled/Draft"][random.randint(0,3)]
            self.add_message(message_type=test_type,sent_from="Admin",
                             sent_to="All Members", date_sent=f"12-{i}-2025",
                             time_sent="00:00",
                             message=f"Next Meeting will be held on 3/{i}/2025"
                             )
        
        scroll_area.setWidget(scroll_container)
        self.verticalLayout.addWidget(scroll_area)
        
    def add_message(self, message_type, sent_from,sent_to, date_sent, time_sent ,message):
        message_frame = QFrame()
        message_frame.setStyleSheet("border: 1px solid #ccc; background-color: white; padding: 10px; border-radius: 5px;")
        frame_layout = QVBoxLayout(message_frame)
        
        sender_label = QLabel(f"{message_type}   FROM: {sent_from}     TO: {sent_to}      AT: {date_sent}   {time_sent}")
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
        send_btn = QPushButton("Send")
        
        if message_type.lower() == "inbox":
            action_buttons = [reply_btn, mark_read_btn, delete_btn]
        elif message_type.lower() == "sent":
            action_buttons = [delete_btn]
        elif "schedule" in message_type.lower():
            action_buttons = [send_btn, mark_read_btn, delete_btn]
        elif message_type.lower() == "alert":
            action_buttons = [mark_read_btn, delete_btn]
            
        for btn in action_buttons:
            btn.setFixedSize(130, 40)
            btn.setStyleSheet("background-color: #FF9800; color: white; border-radius: 5px;")
            buttons_layout.addWidget(btn)
                
        frame_layout.addLayout(buttons_layout)
        
        self.message_layout.addWidget(message_frame)
    
    def filter_messages(self):
        sender = self.sender()
        category = sender.text()
        # print(f"Filtering: {category}")  # Placeholder functionality
        
    def send_sms(self):
        pass
    def schedule_sms(self):
        pass
    def send_email(self):
        pass
    def schedule_email(self):
        pass
    