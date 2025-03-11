from PyQt5 import uic, QtWidgets
import sys

class MembersPage(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("C_PROJECT/UI_FILES/members_page.ui", self)  # Load the UI file

        # Get references to the UI elements
        self.search_box = self.findChild(QtWidgets.QLineEdit, "searchLineEdit")  # Replace with your object name
        self.table_widget = self.findChild(QtWidgets.QTableWidget, "membersTableWidget")  # Replace with your object name

        # Load data into the table
        self.load_table_data()

        # Connect search box to filter function
        self.search_box.textChanged.connect(self.filter_table)
        self.table_widget.cellClicked.connect(self.on_row_click)
    
    def on_row_click(self):
        row = self.table_widget.currentRow()
        col = self.table_widget.currentColumn()
        row_data = {}
        headers = ["ID", "Name", "ID Number", "Position", "Address", "Status", "Contacts", "Date Joined"]

        for column in range(self.table_widget.columnCount()):
            item = self.table_widget.item(row, column)
            if item:
                row_data[headers[column]] = item.text()

        clicked_cell_value = self.table_widget.item(row, col).text()
        print(f"Clicked Cell: {headers[col]}: {clicked_cell_value}")
        print("Row Data:", row_data)
        """Clicked Cell: Position: ChairPerson
        Row Data: {'ID': '1', 'Name': 'Aisha Hassan', 'ID Number': '1234567890123', 'Position': 'ChairPerson', 'Address': 'Apartment 5B, Acacia Avenue, Nairobi',
        'Status': 'Active', 'Contacts': 'aisha.hassan@email.com, +254712345678', 'Date Joined': '2020-01-15'}"""
    
    def load_table_data(self):
        """Load initial data into the QTableWidget"""
        self.data = [
            (1, "Aisha Hassan", "1234567890123", "ChairPerson", "Apartment 5B, Acacia Avenue, Nairobi", "Active", "aisha.hassan@email.com, +254712345678", "2020-01-15"),
            (2, "John Mwangi", "9876543210987", "Treasurer", "House No. 10, Kijabe Street, Nairobi", "Active", "john.mwangi@email.com, +254723456789, +254111222333", "2019-03-22"),
            (3, "Fatima Omondi", "1122334455667", "Secretary", "Plot 23, Riverside Drive, Nairobi", "Inactive", "fatima.omondi@email.com", "2018-07-30"),
            (4, "David Kamau", "6677889900112", "Member", "Flat C7, Ngong Road, Nairobi", "Active", "david.kamau@email.com, +254734567890", "2021-05-10"),
            (5, "Sarah Wambui", "2233445566778", "Assistant ChairPerson", "Villa 15, Karen Road, Nairobi", "Active", "sarah.wambui@email.com, +254745678901", "2020-11-25"),
            (6, "Peter Onyango", "8899001122334", "Assistant Treasurer", "Building 8, Lavington, Nairobi", "Inactive", "peter.onyango@email.com, +254756789012", "2019-09-14"),
            (7, "Grace Akinyi", "3344556677889", "Member", "Suite 22, Westlands, Nairobi", "Active", "grace.akinyi@email.com", "2021-02-18"),
            (8, "Samuel Kimani", "9900112233445", "Member", "House 4, Runda Estate, Nairobi", "Active", "samuel.kimani@email.com, +254767890123", "2020-06-05"),
            (9, "Lucy Njeri", "4455667788990", "Assistant Secretary", "Apartment 9A, Kilimani, Nairobi", "Inactive", "lucy.njeri@email.com, +254778901234", "2018-12-12"),
            (10, "Michael Otieno", "0011223344556", "Member", "Plot 56, South C, Nairobi", "Active", "michael.otieno@email.com", "2019-04-20"),
            (11, "Jane Mutua", "5566778899001", "Member", "House 2, Eastleigh, Nairobi", "Active", "jane.mutua@email.com, +254789012345", "2021-08-15"),
            (12, "Victor Maina", "1122334455667", "Member", "Apartment 12B, Umoja, Nairobi", "Inactive", "victor.maina@email.com", "2020-10-01"),
            (13, "Esther Wangari", "6677889900112", "Member", "Plot 3, Embakasi, Nairobi", "Active", "esther.wangari@email.com, +254790123456", "2019-11-27"),
            (14, "Daniel Mwangi", "2233445566778", "Member", "House 7, Dandora, Nairobi", "Active", "daniel.mwangi@email.com", "2020-03-19"),
            (15, "Mercy Cherono", "8899001122334", "Member", "Apartment 1, Kayole, Nairobi", "Inactive", "mercy.cherono@email.com, +254701234567", "2018-05-23"),
            (16, "Kevin Odhiambo", "7788990011223", "Member", "P.O. Box 1234, Nairobi", "Active", "kevin.odhiambo@email.com", "2021-07-07"),
            (17, "Emily Wanjiku", "3344556677889", "Member", "Flat 4D, Langata, Nairobi", "Active", "emily.wanjiku@email.com, +254711223344", "2019-01-29"),
            (18, "Brian Juma", "9900112233445", "Member", "House 9, Buruburu, Nairobi", "Inactive", "brian.juma@email.com", "2020-09-13"),
            (19, "Caroline Moraa", "4455667788990", "Member", "Apartment 10C, Kileleshwa, Nairobi", "Active", "caroline.moraa@email.com, +254722334455", "2021-04-02"),
            (20, "Anthony Kioko", "0011223344556", "Member", "Plot 18, Donholm, Nairobi", "Active", "anthony.kioko@email.com", "2018-11-16"),
            (21, "Rose Jeptoo", "5566778899001", "Member", "Villa 7, Muthaiga, Nairobi", "Inactive", "rose.jeptoo@email.com, +254733445566", "2019-06-21"),
            (22, "Joseph Njoroge", "1122334455667", "Member", "Building 3, Parklands, Nairobi", "Active", "joseph.njoroge@email.com", "2020-02-28"),
            (23, "Catherine Wanjala", "6677889900112", "Member", "Suite 11, Upper Hill, Nairobi", "Active", "catherine.wanjala@email.com, +254744556677", "2021-10-09"),
            (24, "Patrick Ochieng", "2233445566778", "Member", "House 12, Industrial Area, Nairobi", "Inactive", "patrick.ochieng@email.com", "2018-08-03"),
            (25, "Faith Chebet", "8899001122334", "Member", "Apartment 6E, Madaraka, Nairobi", "Active", "faith.chebet@email.com, +254755667788", "2019-05-17"),
            ]

        self.table_widget.setRowCount(len(self.data))
        self.table_widget.setColumnCount(8)  # Adjust based on data
        self.table_widget.setHorizontalHeaderLabels(["ID", "Name", "ID Number", "Position", "Address", "Status", "Contacts", "Date Joined"])

        for row, (id, name, id_number, position, address, status, contacts, date_joined) in enumerate(self.data):
            self.table_widget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(id)))
            self.table_widget.setItem(row, 1, QtWidgets.QTableWidgetItem(name))
            self.table_widget.setItem(row, 2, QtWidgets.QTableWidgetItem(id_number))
            self.table_widget.setItem(row, 3, QtWidgets.QTableWidgetItem(position))
            self.table_widget.setItem(row, 4, QtWidgets.QTableWidgetItem(address))
            self.table_widget.setItem(row, 5, QtWidgets.QTableWidgetItem(status))
            self.table_widget.setItem(row, 6, QtWidgets.QTableWidgetItem(contacts))
            self.table_widget.setItem(row, 7, QtWidgets.QTableWidgetItem(date_joined))


    def filter_table(self):
        """Filter table rows based on search box input"""
        search_text = self.search_box.text().lower()

        for row in range(self.table_widget.rowCount()):
            row_match = False
            for col in range(self.table_widget.columnCount()):
                item = self.table_widget.item(row, col)
                if item and search_text in item.text().lower():
                    row_match = True
                    break

            self.table_widget.setRowHidden(row, not row_match)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MembersPage()
    window.show()
    sys.exit(app.exec_())
