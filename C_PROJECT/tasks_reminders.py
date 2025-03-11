from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QScrollArea, QFrame, QCheckBox, QComboBox
)
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QComboBox, QDateEdit, QCheckBox
)
from PyQt5.QtCore import QDate
from PyQt5 import QtCore, QtWidgets
import sys

class TaskManager(QWidget):
    def __init__(self, the_stack):
        super().__init__()
        self.the_stack = the_stack
        self.setWindowTitle("Tasks & Reminders")
        # self.setGeometry(200, 100, 650, 500)  # Slightly increased size for better spacing
        
        main_layout = QVBoxLayout()

        # Header
        header_label = QLabel("TASKS & REMINDERS")
        header_label.setStyleSheet("""
            font-size: 22px; font-weight: bold; 
            color: #333; padding: 10px; text-align: center;
        """)
        header_label.setAlignment(QtCore.Qt.AlignCenter)  # Centering text
        main_layout.addWidget(header_label)

        # Top Controls
        top_controls = QHBoxLayout()
        self.add_task_btn = QPushButton("+ Add New Task")
        self.add_task_btn.setStyleSheet("""
            background-color: #0078D7; color: white; padding: 8px 15px; 
            border-radius: 5px; font-weight: bold;
        """)
        self.add_task_btn.clicked.connect(self.open_create_task_dialog)

        self.filter_dropdown = QComboBox()
        self.filter_dropdown.addItems(["All", "High", "Medium", "Low"])
        self.filter_dropdown.setStyleSheet("padding: 5px; font-weight: bold;")
        
        home_button = QPushButton("Home")
        home_button.setFixedSize(100, 35)
        home_button.setStyleSheet("""
            background-color: #28a745; color: white; font-weight: bold;
            border-radius: 5px;
        """)
        home_button.clicked.connect(lambda x: self.the_stack.setCurrentIndex(1))

        top_controls.addWidget(self.add_task_btn)
        top_controls.addStretch(1)  # Push filter to the right
        top_controls.addWidget(QLabel("Filter:"))
        top_controls.addWidget(self.filter_dropdown)
        top_controls.addWidget(home_button)
        main_layout.addLayout(top_controls)

        # Scrollable Task List
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        self.task_container = QWidget()
        self.task_layout = QVBoxLayout(self.task_container)
        self.task_layout.setSpacing(10)

        scroll_area.setWidget(self.task_container)
        main_layout.addWidget(scroll_area)

        main_layout.setContentsMargins(10, 10, 10, 100)
        self.setLayout(main_layout)

        # Load Test Data
        self.load_test_tasks()

    def open_create_task_dialog(self):
        dialog = CreateNewTask(self)
        if dialog.exec_() == QDialog.Accepted:
            # Get values from the dialog
            task_desc = dialog.task_name.text()
            due_date = dialog.due_date.date().toString("MMM dd")  # Format date
            priority = dialog.priority.currentText()
            assigned_to = dialog.assigned_to.text()
            completed = dialog.completed.isChecked()

            if task_desc.strip() and assigned_to.strip():  # Ensure fields are filled
                self.add_task(f"{task_desc} [Assigned To: {assigned_to}]", due_date, priority, completed)
                print("Task Added!!")
    def load_test_tasks(self):
        tasks = [
            ("Collect monthly contributions [Assigned To: John Vincent]", "Mar 10", "High", True),
            ("Remind John about arrears [Assigned To: Barbara Pravi]", "Mar 12", "Medium", False),
            ("Prepare financial report [Assigned To: Hailey B.]", "Mar 15", "High", True),
            ("Schedule next meeting [Assigned To: Jacques G.]", "Mar 20", "Low", False),    
            ("Collect monthly contributions [Assigned To: John Vincent]", "Mar 10", "High", True),
            ("Remind John about arrears [Assigned To: Barbara Pravi]", "Mar 12", "Medium", False),
            ("Prepare financial report [Assigned To: Hailey B.]", "Mar 15", "High", True),
            ("Schedule next meeting [Assigned To: Jacques G.]", "Mar 20", "Low", False),
            ("Collect monthly contributions [Assigned To: John Vincent]", "Mar 10", "High", True),
            ("Remind John about arrears [Assigned To: Barbara Pravi]", "Mar 12", "Medium", False),
            ("Prepare financial report [Assigned To: Hailey B.]", "Mar 15", "High", True),
            ("Schedule next meeting [Assigned To: Jacques G.]", "Mar 20", "Low", False)
        ]
        
        for task in tasks:
            self.add_task(*task)

    def add_task(self, task_name, due_date, priority, completed):
        task_frame = QFrame()
        task_frame.setStyleSheet("""
            border: 1px solid #ccc; border-radius: 8px; 
            padding: 8px; background: #f9f9f9;
        """)

        task_layout = QHBoxLayout()

        # Task description takes more space
        task_checkbox = QCheckBox(task_name)
        task_checkbox.setChecked(completed)
        task_checkbox.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)  # Expanding horizontally

        due_label = QLabel(f"📅 Due: {due_date}")
        due_label.setStyleSheet("color: #555; font-size: 12px;")

        priority_label = QLabel(f"⚡ {priority}")
        priority_label.setStyleSheet(
            "font-weight: bold; color: #d9534f;" if priority == "High" else
            "color: #f0ad4e;" if priority == "Medium" else "color: #5bc0de;"
        )

        mark_done_btn = QPushButton("✔ Done")
        mark_done_btn.setStyleSheet("background-color: #28a745; color: white; padding: 5px; border-radius: 3px;")

        delete_btn = QPushButton("🗑 Delete")
        delete_btn.setStyleSheet("background-color: #dc3545; color: white; padding: 5px; border-radius: 3px;")

        # Add widgets in a better order
        task_layout.addWidget(task_checkbox)  # Task takes more space
        task_layout.addWidget(due_label)
        task_layout.addWidget(priority_label)  # Reduced gap
        task_layout.addWidget(mark_done_btn)
        task_layout.addWidget(delete_btn)

        task_frame.setLayout(task_layout)
        self.task_layout.addWidget(task_frame)



class CreateNewTask(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Task")
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: #f9f9f9; border-radius: 10px;")

        layout = QVBoxLayout()

        # Task Name
        self.task_name = QLineEdit()
        self.task_name.setPlaceholderText("Enter task description")
        self.task_name.setStyleSheet("padding: 8px; border-radius: 5px; border: 1px solid #ccc;")
        layout.addWidget(QLabel("Task Description:"))
        layout.addWidget(self.task_name)

        # Due Date
        self.due_date = QDateEdit()
        self.due_date.setCalendarPopup(True)
        self.due_date.setDate(QDate.currentDate())  # Auto-set to today
        self.due_date.setStyleSheet("padding: 5px; border-radius: 5px; border: 1px solid #ccc;")
        layout.addWidget(QLabel("Due Date:"))
        layout.addWidget(self.due_date)

        # Priority Level
        self.priority = QComboBox()
        self.priority.addItems(["High", "Medium", "Low"])
        self.priority.setStyleSheet("padding: 5px; border-radius: 5px; border: 1px solid #ccc;")
        layout.addWidget(QLabel("Priority:"))
        layout.addWidget(self.priority)

        # Assigned To
        self.assigned_to = QLineEdit()
        self.assigned_to.setPlaceholderText("Enter assigned person's name")
        self.assigned_to.setStyleSheet("padding: 8px; border-radius: 5px; border: 1px solid #ccc;")
        layout.addWidget(QLabel("Assigned To:"))
        layout.addWidget(self.assigned_to)

        # Completed Checkbox
        self.completed = QCheckBox("Mark as Completed")
        layout.addWidget(self.completed)

        # Buttons (Save & Cancel)
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save Task")
        self.save_btn.setStyleSheet("background-color: #28a745; color: white; padding: 7px; border-radius: 5px;")
        self.save_btn.clicked.connect(self.save_task)  # Connect Save button
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet("background-color: #dc3545; color: white; padding: 7px; border-radius: 5px;")
        self.cancel_btn.clicked.connect(self.reject)  # Closes dialog

        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        
    def save_task(self):
        # Check if required fields are filled
        if not self.task_name.text().strip():
            self.task_name.setStyleSheet("border: 1px solid red;")  # Highlight missing input
            return  # Stop if the task name is empty

        if not self.assigned_to.text().strip():
            self.assigned_to.setStyleSheet("border: 1px solid red;")  # Highlight missing input
            return  # Stop if the assigned person is empty

        # Accept the dialog (so TaskManager can retrieve the data)
        self.accept()

