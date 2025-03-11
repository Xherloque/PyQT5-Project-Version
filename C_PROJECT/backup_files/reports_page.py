import sys
import sqlite3
import pandas as pd
from PyQt5 import QtWidgets, QtGui, QtCore
from fpdf import FPDF
import xlsxwriter

class ReportsPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.conn = sqlite3.connect("group_finance.db")

    def init_ui(self):
        self.setWindowTitle("Reports Page")
        self.setGeometry(100, 100, 900, 600)
        
        main_layout = QtWidgets.QVBoxLayout(self)
        
        # Navigation Bar
        nav_bar = QtWidgets.QHBoxLayout()
        home_btn = QtWidgets.QPushButton("Home")
        contributions_btn = QtWidgets.QPushButton("Contributions")
        loans_btn = QtWidgets.QPushButton("Loans & Debts")
        reports_btn = QtWidgets.QPushButton("Reports")
        
        for btn in [home_btn, contributions_btn, loans_btn, reports_btn]:
            btn.setStyleSheet("padding: 8px 15px; font-weight: bold;")
            nav_bar.addWidget(btn)
        
        # Search & Filter Bar
        search_layout = QtWidgets.QHBoxLayout()
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Search reports...")
        filter_btn = QtWidgets.QPushButton("Filter")
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(filter_btn)
        
        # Tabs for different reports
        self.tabs = QtWidgets.QTabWidget()
        self.financial_tab = QtWidgets.QWidget()
        self.attendance_tab = QtWidgets.QWidget()
        self.events_tab = QtWidgets.QWidget()
        
        self.tabs.addTab(self.financial_tab, "Financial Reports")
        self.tabs.addTab(self.attendance_tab, "Attendance Reports")
        self.tabs.addTab(self.events_tab, "Events Reports")
        
        # Setting up each tab
        self.setup_financial_tab()
        self.setup_attendance_tab()
        self.setup_events_tab()
        
        # Adding widgets to layout
        main_layout.addLayout(nav_bar)
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)
    
    def setup_financial_tab(self):
        layout = QtWidgets.QVBoxLayout()
        self.financial_table = QtWidgets.QTableWidget()
        self.load_financial_data()
        
        export_pdf_btn = QtWidgets.QPushButton("Export Financial Report (PDF)")
        export_pdf_btn.clicked.connect(self.export_financial_report)
        
        export_excel_btn = QtWidgets.QPushButton("Export Financial Report (Excel)")
        export_excel_btn.clicked.connect(lambda: self.export_excel_report("Financial_Report.xlsx", "transactions"))
        
        layout.addWidget(self.financial_table)
        layout.addWidget(export_pdf_btn)
        layout.addWidget(export_excel_btn)
        self.financial_tab.setLayout(layout)
    
    def setup_attendance_tab(self):
        layout = QtWidgets.QVBoxLayout()
        self.attendance_table = QtWidgets.QTableWidget()
        self.load_attendance_data()
        
        export_pdf_btn = QtWidgets.QPushButton("Export Attendance Report (PDF)")
        export_pdf_btn.clicked.connect(self.export_attendance_report)
        
        export_excel_btn = QtWidgets.QPushButton("Export Attendance Report (Excel)")
        export_excel_btn.clicked.connect(lambda: self.export_excel_report("Attendance_Report.xlsx", "attendance"))
        
        layout.addWidget(self.attendance_table)
        layout.addWidget(export_pdf_btn)
        layout.addWidget(export_excel_btn)
        self.attendance_tab.setLayout(layout)
    
    def setup_events_tab(self):
        layout = QtWidgets.QVBoxLayout()
        self.events_table = QtWidgets.QTableWidget()
        self.load_events_data()
        
        export_pdf_btn = QtWidgets.QPushButton("Export Events Report (PDF)")
        export_pdf_btn.clicked.connect(self.export_events_report)
        
        export_excel_btn = QtWidgets.QPushButton("Export Events Report (Excel)")
        export_excel_btn.clicked.connect(lambda: self.export_excel_report("Events_Report.xlsx", "events"))
        
        layout.addWidget(self.events_table)
        layout.addWidget(export_pdf_btn)
        layout.addWidget(export_excel_btn)
        self.events_tab.setLayout(layout)
    
    def load_financial_data(self):
        query = "SELECT transaction_type, amount, transaction_date, description FROM transactions ORDER BY transaction_date DESC"
        self.populate_table(self.financial_table, query)
    
    def load_attendance_data(self):
        query = "SELECT meeting_id, member_id, status FROM attendance ORDER BY meeting_id DESC"
        self.populate_table(self.attendance_table, query)
    
    def load_events_data(self):
        query = "SELECT event_id, event_name, event_date, attendees FROM events ORDER BY event_date DESC"
        self.populate_table(self.events_table, query)
    
    def populate_table(self, table, query):
        df = pd.read_sql_query(query, self.conn)
        table.setRowCount(df.shape[0])
        table.setColumnCount(df.shape[1])
        table.setHorizontalHeaderLabels(df.columns)
        
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                table.setItem(i, j, QtWidgets.QTableWidgetItem(str(df.iloc[i, j])))
        
    def export_financial_report(self):
        self.export_report("Financial_Report.pdf", "transactions")
    
    def export_attendance_report(self):
        self.export_report("Attendance_Report.pdf", "attendance")
    
    def export_events_report(self):
        self.export_report("Events_Report.pdf", "events")
    
    def export_report(self, file_name, table_name):
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql_query(query, self.conn)
        
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, f"{table_name.capitalize()} Report", ln=True, align="C")
        pdf.ln(10)
        
        for _, row in df.iterrows():
            pdf.cell(200, 8, " | ".join(str(value) for value in row), ln=True)
        
        pdf.output(file_name)
        QtWidgets.QMessageBox.information(self, "Export Success", f"{file_name} saved successfully!")
    
    def export_excel_report(self, file_name, table_name):
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql_query(query, self.conn)
        df.to_excel(file_name, index=False, engine='xlsxwriter')
        QtWidgets.QMessageBox.information(self, "Export Success", f"{file_name} saved successfully!")
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ReportsPage()
    window.showMaximized()
    sys.exit(app.exec_())
