from PyQt5.QtWidgets import (
    QApplication, QWidget, QListWidget, QStackedWidget, QVBoxLayout,
    QLabel, QCheckBox, QPushButton, QLineEdit, QFormLayout, QComboBox,
    QHBoxLayout, QTextEdit, QListWidgetItem
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys

class SettingsUI(QWidget):
    def __init__(self, the_stack):
        super().__init__()
        self.the_stack = the_stack
        self.setWindowTitle("Application Settings")
        self.setGeometry(200, 200, 800, 500)
        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout()

        # 🔹 Navigation Bar (Fixed at Top)
        nav_bar = QHBoxLayout()
        nav_bar.setSpacing(10)

        title_label = QLabel("⚙️ Application Settings")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setStyleSheet("color: #333; padding: 15px;")

        search_box = QLineEdit()
        search_box.setPlaceholderText("🔍 Search settings...")
        search_box.setStyleSheet("""
            padding: 8px 12px;
            border: 1px solid #ccc;
            border-radius: 5px;
            background-color: #f8f8f8;
        """)

        home_btn = QPushButton("🏠 Home")
        home_btn.setStyleSheet("""
            padding: 8px 15px;
            font-weight: bold;
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
        """)
        home_btn.clicked.connect(lambda x: self.the_stack.setCurrentIndex(1))

        nav_bar.addWidget(title_label)
        nav_bar.addStretch()
        nav_bar.addWidget(search_box)
        nav_bar.addWidget(home_btn)
        self.main_layout.addLayout(nav_bar)

        # 🔹 Main Layout
        layout = QHBoxLayout()

        # 🔹 Sidebar Menu (Better Styling)
        self.listWidget = QListWidget()
        self.listWidget.setFixedWidth(250)
        self.listWidget.setFont(QFont("Arial", 14))
        self.listWidget.setStyleSheet("""
            background-color: #eee;
            border-right: 2px solid #ddd;
            padding: 10px;
        """)

        settings_categories = [
            "General Settings", "User Management", "Permissions & Roles",
            "Data Backup & Restore", "Notification Preferences", "About / Help"
        ]

        for category in settings_categories:
            item = QListWidgetItem(category)
            item.setFont(QFont("Arial", 12, QFont.Bold))
            self.listWidget.addItem(item)

        # 🔹 Main Content Area
        self.stackedWidget = QStackedWidget()

        # Add Setting Pages
        self.pages = {
            "General Settings": self.general_settings_page(),
            "User Management": self.user_management_page(),
            "Permissions & Roles": self.permissions_page(),
            "Data Backup & Restore": self.backup_restore_page(),
            "Notification Preferences": self.notifications_page(),
            "About / Help": self.about_help_page()
        }

        for page in self.pages.values():
            self.stackedWidget.addWidget(page)

        # Connect Sidebar Selection
        self.listWidget.currentRowChanged.connect(
            lambda i: self.stackedWidget.setCurrentWidget(list(self.pages.values())[i])
        )

        # Add to Layout
        layout.addWidget(self.listWidget)
        layout.addWidget(self.stackedWidget)
        self.main_layout.addLayout(layout)
        self.setLayout(self.main_layout)

    # 🔹 Settings Pages (Better Styled)
    def general_settings_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        form_layout.addRow(QLabel("App Name:"), QLineEdit("Support Group Manager"))
        form_layout.addRow(QLabel("Group Name:"), QLineEdit("Unity Welfare Group"))
        form_layout.addRow(QLabel("Date Format:"), QComboBox())
        form_layout.addRow(QLabel("Time Zone:"), QComboBox())
        form_layout.addRow(QLabel("Currency:"), QComboBox())
        form_layout.addRow(QLabel("Theme:"), QComboBox())
        form_layout.addRow(QLabel("Logo:"), QPushButton("Upload Logo"))

        layout.addLayout(form_layout)
        layout.addStretch()
        page.setLayout(layout)
        return page

    def user_management_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        title = QLabel("👥 Total Members: 102 Active Users")
        title.setFont(QFont("Arial", 12, QFont.Bold))

        add_member_btn = QPushButton("➕ Add New Member")
        import_btn = QPushButton("📂 Import CSV")
        export_btn = QPushButton("📤 Export Data")

        for btn in [add_member_btn, import_btn, export_btn]:
            btn.setStyleSheet("padding: 10px; border-radius: 5px; background-color: #2196F3; color: white;")

        layout.addWidget(title)
        layout.addWidget(add_member_btn)
        layout.addWidget(import_btn)
        layout.addWidget(export_btn)
        layout.addStretch()
        page.setLayout(layout)
        return page

    def permissions_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        title = QLabel("🔑 User Roles & Permissions")
        title.setFont(QFont("Arial", 12, QFont.Bold))

        edit_roles_btn = QPushButton("✏️ Edit Roles")
        create_role_btn = QPushButton("🆕 Create New Role")

        for btn in [edit_roles_btn, create_role_btn]:
            btn.setStyleSheet("padding: 10px; border-radius: 5px; background-color: #FFC107; color: black;")

        layout.addWidget(title)
        layout.addWidget(edit_roles_btn)
        layout.addWidget(create_role_btn)
        layout.addStretch()
        page.setLayout(layout)
        return page

    def backup_restore_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        title = QLabel("💾 Last Backup: 2 Days Ago")
        title.setFont(QFont("Arial", 12, QFont.Bold))

        backup_btn = QPushButton("📀 Backup Now")
        restore_btn = QPushButton("♻️ Restore Backup")

        for btn in [backup_btn, restore_btn]:
            btn.setStyleSheet("padding: 10px; border-radius: 5px; background-color: #E91E63; color: white;")

        layout.addWidget(title)
        layout.addWidget(backup_btn)
        layout.addWidget(restore_btn)
        layout.addStretch()
        page.setLayout(layout)
        return page

    def notifications_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        title = QLabel("🔔 Notification Preferences")
        title.setFont(QFont("Arial", 12, QFont.Bold))

        email_checkbox = QCheckBox("Enable Email Notifications")
        sms_checkbox = QCheckBox("Enable SMS Notifications")
        push_checkbox = QCheckBox("Enable Push Notifications")
        customize_btn = QPushButton("⚙️ Customize Alerts")

        layout.addWidget(title)
        layout.addWidget(email_checkbox)
        layout.addWidget(sms_checkbox)
        layout.addWidget(push_checkbox)
        layout.addWidget(customize_btn)
        layout.addStretch()
        page.setLayout(layout)
        return page

    def about_help_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        title = QLabel("📜 Application Version: 1.2.5")
        title.setFont(QFont("Arial", 12, QFont.Bold))

        terms_btn = QPushButton("📄 View Terms & Policies")
        support_btn = QPushButton("📞 Contact Support")

        layout.addWidget(title)
        layout.addWidget(terms_btn)
        layout.addWidget(support_btn)
        layout.addStretch()
        page.setLayout(layout)
        return page
