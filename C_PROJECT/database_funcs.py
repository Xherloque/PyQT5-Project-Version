import sqlite3

SQL_SCHEMA = """
PRAGMA foreign_keys = ON;  -- Ensure foreign key enforcement

-- Members Table
CREATE TABLE IF NOT EXISTS members (
    member_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    id_number TEXT UNIQUE NOT NULL,
    role TEXT CHECK(role IN ('Admin', 'Treasurer', 'Secretary', 'Member')) NOT NULL,
    address TEXT,
    status TEXT CHECK(status IN ('Active', 'Inactive', 'Suspended')) DEFAULT 'Active',
    date_joined DATE NOT NULL,
    date_of_birth DATE,
    profile_image TEXT,
    health_details TEXT
);

-- Contacts Table
CREATE TABLE IF NOT EXISTS group_contacts (
    contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL,
    contact TEXT NOT NULL,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE
);

-- Family & Emergency Contacts Table
CREATE TABLE IF NOT EXISTS family (
    family_member_id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    contact TEXT NOT NULL,
    relation_to_member TEXT,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE
);

-- Initial Records Table (Tracks membership fees and initial financial records)
CREATE TABLE initial_records (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL,
    category TEXT CHECK(category IN ('Membership Fee', 'Arrears', 'Loans', 'Contributions')) NOT NULL,
    amount REAL NOT NULL,
    description TEXT,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE
);

-- Meetings Table
CREATE TABLE IF NOT EXISTS meetings (
    meeting_id INTEGER PRIMARY KEY AUTOINCREMENT,
    meeting_label TEXT,
    meeting_date DATE NOT NULL,
    meeting_time TIME NOT NULL,
    time_ended TIME,
    agenda TEXT,
    facilitator TEXT NOT NULL,
    attendance_count INTEGER DEFAULT 0,
    total_contributions REAL DEFAULT 0.0
);


-- Proposals Table (Tracks all proposals from all meetings)
CREATE TABLE proposals (
    proposal_id INTEGER PRIMARY KEY AUTOINCREMENT,
    meeting_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    proposal_description TEXT NOT NULL,
    FOREIGN KEY (meeting_id) REFERENCES meetings(meeting_id) ON DELETE CASCADE,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE
);

-- Attendance Table
CREATE TABLE IF NOT EXISTS attendance (
    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    meeting_id INTEGER NOT NULL,
    on_time TEXT CHECK(on_time IN ('On Time', 'Late')),
    member_id INTEGER NOT NULL,
    FOREIGN KEY (meeting_id) REFERENCES meetings(meeting_id) ON DELETE CASCADE,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE
);

-- Contributions Table
CREATE TABLE IF NOT EXISTS contributions (
    contribution_id INTEGER PRIMARY KEY AUTOINCREMENT,
    meeting_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    amount REAL CHECK(amount > 0) NOT NULL,
    payment_method TEXT CHECK(payment_method IN ('Cash', 'Bank Transfer', 'Mobile Payment')) NOT NULL,
    contribution_date DATE NOT NULL,
    FOREIGN KEY (meeting_id) REFERENCES meetings(meeting_id) ON DELETE CASCADE,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE
);

-- Loans Table
CREATE TABLE IF NOT EXISTS loans (
    loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL,
    amount REAL CHECK(amount > 0) NOT NULL,
    issued_date DATE NOT NULL,
    due_date DATE NOT NULL,
    status TEXT CHECK(status IN ('Pending', 'Overdue', 'Partially Paid', 'Paid')) DEFAULT 'Pending',
    amount_paid REAL DEFAULT 0.0,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE
);

-- Arrears Table
CREATE TABLE IF NOT EXISTS arrears (
    arrear_id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL,
    description TEXT,
    amount REAL CHECK(amount > 0) NOT NULL,
    status TEXT CHECK(status IN ('Pending', 'Overdue', 'Partially Paid', 'Paid')) DEFAULT 'Pending',
    amount_paid REAL DEFAULT 0.0,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE
);

-- Group Accounts Table
CREATE TABLE IF NOT EXISTS group_accounts (
    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    created DATE,
    balance REAL CHECK(balance > 0) NOT NULL,
    description TEXT
);


-- Financial Transactions Table
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    transaction_type TEXT CHECK(transaction_type IN ('Deposit', 'Withdrawal', 'Loan Issued', 'Loan Repaid', 'Contribution', 'Penalty')) NOT NULL,
    amount REAL CHECK(amount > 0) NOT NULL,
    transaction_date DATE NOT NULL,
    description TEXT
);

-- Tasks & Reminders Table
CREATE TABLE IF NOT EXISTS tasks (
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    assigned_to INTEGER,
    due_date DATE NOT NULL,
    priority TEXT CHECK(priority IN ('Low', 'Medium', 'High')) DEFAULT 'Medium',
    status TEXT CHECK(status IN ('Pending', 'Completed')) DEFAULT 'Pending',
    FOREIGN KEY (assigned_to) REFERENCES members(member_id) ON DELETE SET NULL
);

-- Messages Table
CREATE TABLE IF NOT EXISTS messages (
    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER,
    message TEXT NOT NULL,
    sent_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read_status BOOLEAN DEFAULT 0,
    FOREIGN KEY (sender_id) REFERENCES members(member_id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES members(member_id) ON DELETE CASCADE
);

-- Application Settings
CREATE TABLE IF NOT EXISTS general_settings (
    setting_id INTEGER PRIMARY KEY AUTOINCREMENT,
    app_name TEXT DEFAULT 'Group Manager',
    app_logo TEXT DEFAULT 'default_logo.png',
    group_name TEXT,
    registration_details TEXT,
    description TEXT,
    date_format TEXT DEFAULT 'YYYY-MM-DD',
    time_zone TEXT DEFAULT 'UTC',
    currency TEXT DEFAULT 'USD',
    language TEXT DEFAULT 'English',
    theme TEXT CHECK(theme IN ('Light', 'Dark')) DEFAULT 'Light',
    email_notifications_enabled BOOLEAN DEFAULT 1,
    sms_notifications_enabled BOOLEAN DEFAULT 1
);

-- Backups Table
CREATE TABLE IF NOT EXISTS backups (
    backup_id INTEGER PRIMARY KEY AUTOINCREMENT,
    backup_date DATE DEFAULT CURRENT_TIMESTAMP,
    backup_file TEXT,
    backup_type TEXT CHECK(backup_type IN ('Manual', 'Automatic')),
    storage_location TEXT
);

-- System Logs Table
CREATE TABLE IF NOT EXISTS system_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Integrations Table
CREATE TABLE IF NOT EXISTS integrations (
    integration_id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_name TEXT NOT NULL,
    api_key TEXT,
    api_url TEXT
);
"""



def create_database(db_path):
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Enable Foreign Keys
        cursor.execute("PRAGMA foreign_keys = ON;")

        # Execute Schema
        cursor.executescript(SQL_SCHEMA)
        
        conn.commit()
        conn.close()
        print("DATABASE CREATED SUCCESSFULLY")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()


class DBRecord:
    """Class to allow dot-notation access to SQLite query results."""
    def __init__(self, cursor, row):
        self._keys = [col[0] for col in cursor.description]  # Extract column names
        self._values = row
        self.__dict__.update(zip(self._keys, self._values))  # Assign attributes dynamically

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.__dict__}>"

def query_as_objects(cursor, query, params=()):
    """Runs an SQL query and returns results as DBRecord objects."""
    cursor.execute(query, params)
    return [DBRecord(cursor, row) for row in cursor.fetchall()]

def get_member_details(cursor, member_id):
    """Fetch full member information including contacts, family, attendance, contributions, loans, arrears, and tasks."""
    member_query = """
    SELECT * FROM members WHERE member_id = ?
    """
    contacts_query = """
    SELECT * FROM group_contacts WHERE member_id = ?
    """
    family_query = """
    SELECT * FROM family WHERE member_id = ?
    """
    attendance_query = """
    SELECT * FROM attendance WHERE member_id = ?
    """
    contributions_query = """
    SELECT * FROM contributions WHERE member_id = ?
    """
    loans_query = """
    SELECT * FROM loans WHERE member_id = ?
    """
    arrears_query = """
    SELECT * FROM arrears WHERE member_id = ?
    """
    tasks_query = """
    SELECT * FROM tasks WHERE assigned_to = ?
    """
    messages_query = """
    SELECT * FROM messages WHERE sender_id = ? OR receiver_id = ?
    """
    proposals_query = """
    SELECT * FROM proposals WHERE member_id = ?
    """
    
    member_details = {
        "member": query_as_objects(cursor, member_query, (member_id,)),
        "contacts": query_as_objects(cursor, contacts_query, (member_id,)),
        "messages": query_as_objects(cursor, messages_query, (member_id, member_id)),
        "family": query_as_objects(cursor, family_query, (member_id,)),
        "proposals": query_as_objects(cursor, proposals_query, (member_id,)),
        "attendance": query_as_objects(cursor, attendance_query, (member_id,)),
        "contributions": query_as_objects(cursor, contributions_query, (member_id,)),
        "loans": query_as_objects(cursor, loans_query, (member_id,)),
        "arrears": query_as_objects(cursor, arrears_query, (member_id,)),
        "tasks": query_as_objects(cursor, tasks_query, (member_id,))
    }

    return member_details

def get_all_members_with_contacts(cursor):
    """Fetch all members with their associated contacts efficiently."""
    
    # Set row factory to allow column-name access
    cursor.row_factory = sqlite3.Row  

    query = """
    SELECT m.*, c.contact
    FROM members m
    LEFT JOIN group_contacts c ON m.member_id = c.member_id
    ORDER BY m.member_id
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    members_dict = {}
    for row in rows:
        member_id = row["member_id"]  # Now row["member_id"] works!

        # If member not yet added, create a new DBRecord object
        if member_id not in members_dict:
            members_dict[member_id] = DBRecord(cursor, row)
            members_dict[member_id].contacts = []

        # Append contact if it exists
        if row["contact"]:
            members_dict[member_id].contacts.append(row["contact"])

    return list(members_dict.values())  # Return all members as objects


VALID_TABLES = {"members", "group_contacts", "meetings", "attendance", "proposals",
                "contributions", "loans", "arrears", "transactions", "tasks", "messages"}

def get_table_as_object(cursor, table_name):
    """Fetch all records from a table safely and return them as objects."""
    if table_name not in VALID_TABLES:
        raise ValueError(f"Invalid table name: {table_name}")

    query = f"SELECT * FROM {table_name}"  # Safe because we validated `table_name`
    cursor.execute(query)
    return [DBRecord(cursor, row) for row in cursor.fetchall()]

def get_member_contacts(cursor, member_id):
    """Fetch all contacts for a specific member."""
    contacts = get_table_as_object(cursor, "group_contacts")
    return [contact for contact in contacts if contact.member_id == member_id]


def add_member(cursor, name, id_number, role, date_joined, contact, family=None, **kwargs):
    """Add a new member to the database along with their contact and family details."""
    try:
        # Insert into members table
        member_query = """
        INSERT INTO members (name, id_number, role, date_joined, address, status, date_of_birth, profile_image, health_details)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(member_query, (
            name, id_number, role, date_joined,
            kwargs.get('address'), kwargs.get('status', 'Active'),
            kwargs.get('date_of_birth'), kwargs.get('profile_image'), kwargs.get('health_details')
        ))
        member_id = cursor.lastrowid  # Get the new member's ID

        # Insert into group_contacts table
        contact_query = "INSERT INTO group_contacts (member_id, contact) VALUES (?, ?)"
        if isinstance(contact, (list, tuple)):  # If multiple contacts
            for c in contact:
                cursor.execute(contact_query, (member_id, c))
        else:  # Single contact
            cursor.execute(contact_query, (member_id, contact))

        # Insert into family table
        if family:  # Check if family data is provided
            family_query = "INSERT INTO family (member_id, name, contact, relation_to_member) VALUES (?, ?, ?, ?)"
            for relation, (full_name, contact) in family.items():
                cursor.execute(family_query, (member_id, full_name, contact, relation))

        return member_id  # Return the new member's ID
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
    

def add_loan(cursor, member_id, amount, issued_date, due_date, status='Pending', amount_paid=0.0):
    """Add a new loan record to the loans table."""
    try:
        loan_query = """
        INSERT INTO loans (member_id, amount, issued_date, due_date, status, amount_paid)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(loan_query, (member_id, amount, issued_date, due_date, status, amount_paid))
        return cursor.lastrowid  # Return the new loan's ID
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None

def add_contribution(cursor, meeting_id, member_id, amount, payment_method, contribution_date):
    """Add a new contribution record to the contributions table."""
    try:
        contribution_query = """
        INSERT INTO contributions (meeting_id, member_id, amount, payment_method, contribution_date)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(contribution_query, (meeting_id, member_id, amount, payment_method, contribution_date))
        return cursor.lastrowid  # Return the new contribution's ID
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None

def add_arrear(cursor, member_id, description, amount, status='Pending', amount_paid=0.0):
    """Add a new arrear record to the arrears table."""
    try:
        arrear_query = """
        INSERT INTO arrears (member_id, description, amount, status, amount_paid)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(arrear_query, (member_id, description, amount, status, amount_paid))
        return cursor.lastrowid  # Return the new arrear's ID
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None

def add_task(cursor, description, due_date, assigned_to=None, priority='Medium', status='Pending'):
    """Add a new task record to the tasks table."""
    try:
        task_query = """
        INSERT INTO tasks (description, due_date, assigned_to, priority, status)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(task_query, (description, due_date, assigned_to, priority, status))
        return cursor.lastrowid  # Return the new task's ID
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None

def add_message(cursor, sender_id, message, receiver_id=None, read_status=0):
    """Add a new message record to the messages table."""
    try:
        message_query = """
        INSERT INTO messages (sender_id, receiver_id, message, read_status)
        VALUES (?, ?, ?, ?)
        """
        cursor.execute(message_query, (sender_id, receiver_id, message, read_status))
        return cursor.lastrowid  # Return the new message's ID
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None

def add_transaction(cursor, account_id, transaction_type, amount, transaction_date, description=None):
    """Add a new transaction record to the transactions table."""
    try:
        transaction_query = """
        INSERT INTO transactions (account_id, transaction_type, amount, transaction_date, description)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(transaction_query, (account_id, transaction_type, amount, transaction_date, description))
        return cursor.lastrowid  # Return the new transaction's ID
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None


class Meeting:
    def __init__(self, meeting_date, meeting_time, agenda, facilitator,time_ended=None, meeting_label=None, proposals=None, attendance=None, contributions=None):
        self.meeting_date = meeting_date
        self.meeting_time = meeting_time
        self.time_ended = time_ended
        self.meeting_label = meeting_label
        self.agenda = agenda
        self.facilitator = facilitator
        self.proposals = proposals if proposals else []
        self.attendance = attendance if attendance else []
        self.contributions = contributions if contributions else []

    def save_meeting(self, cursor):
        try:
            # Calculate total contributions and attendance count
            total_contributions = sum(int(contribution['amount']) for contribution in self.contributions)
            attendance_count = len(self.attendance)
            
            # Insert into meetings table with total contributions and attendance count
            meeting_query = """
            INSERT INTO meetings (meeting_label, meeting_date, meeting_time, time_ended, agenda, facilitator, total_contributions, attendance_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            print("Executing SQL:", meeting_query)
            print("With values:", (
                self.meeting_label, self.meeting_date, self.meeting_time, self.time_ended,
                self.agenda, self.facilitator, total_contributions, attendance_count
            ))
            cursor.execute(meeting_query, (self.meeting_label,self.meeting_date, self.meeting_time,self.time_ended ,self.agenda, self.facilitator, total_contributions, attendance_count))
            meeting_id = cursor.lastrowid  # Get the new meeting's ID

            # Insert proposals
            proposal_query = """
            INSERT INTO proposals (meeting_id, member_id, proposal_description)
            VALUES (?, ?, ?)
            """
            for proposal in self.proposals:
                cursor.execute(proposal_query, (meeting_id, proposal['member_id'], proposal['description']))

            # Insert attendance
            attendance_query = """
            INSERT INTO attendance (meeting_id, member_id, on_time)
            VALUES (?, ?, ?)
            """
            for member_id, on_time in self.attendance:
                cursor.execute(attendance_query, (meeting_id, member_id, on_time))

            # Insert contributions
            contribution_query = """
            INSERT INTO contributions (meeting_id, member_id, amount, payment_method, contribution_date)
            VALUES (?, ?, ?, ?, ?)
            """
            for contribution in self.contributions:
                cursor.execute(contribution_query, (
                    meeting_id, contribution['member_id'], contribution['amount'],
                    contribution['payment_method'], contribution['contribution_date']
                ))

            return meeting_id  # Return the new meeting's ID
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None
        
        
# Adjusted test data
test_members = [
    ("Alice Johnson", "ID12345", "Admin", "2023-01-15", ["+1234567890"], {"Father": ("Robert Johnson", "+9876543210")},
        {"address": "123 Main St", "status": "Active", "date_of_birth": "1990-05-10", "profile_image": "alice.jpg", "health_details": "None"}),

    ("Bob Smith", "ID23456", "Treasurer", "2022-06-20", ["+1987654321"], {"Sister": ("Emma Smith", "+1928374650")},
        {"address": "456 Elm St", "status": "Active", "date_of_birth": "1985-11-23", "profile_image": "bob.png", "health_details": "Asthma"}),

    ("Charlie Adams", "ID34567", "Secretary", "2020-03-10", ["+1112233445"], {"Brother": ("Liam Adams", "+5544332211")},
        {"address": "789 Oak St", "status": "Suspended", "date_of_birth": "1992-07-19", "profile_image": "charlie.jpg", "health_details": "Diabetes"}),

    ("Diana Baker", "ID45678", "Member", "2021-09-30", ["+2233445566"], {"Mother": ("Olivia Baker", "+6677889900")},
        {"address": "101 Pine St", "status": "Inactive", "date_of_birth": "1995-02-14", "profile_image": None, "health_details": None}),

    ("Ethan Carter", "ID56789", "Admin", "2019-05-22", ["+3344556677"], {"Wife": ("Sophia Carter", "+7788990011")},
        {"address": "222 Maple St", "status": "Active", "date_of_birth": "1980-12-05", "profile_image": "ethan.png", "health_details": "High BP"}),

    ("Fiona Davis", "ID67890", "Treasurer", "2023-07-10", ["+4455667788"], {"Father": ("Henry Davis", "+8899001122")},
        {"address": "333 Cedar St", "status": "Active", "date_of_birth": "1998-09-21", "profile_image": "fiona.jpg", "health_details": "None"}),

    ("George Evans", "ID78901", "Secretary", "2018-12-15", ["+5566778899"], {"Sister": ("Isabella Evans", "+9900112233")},
        {"address": "444 Birch St", "status": "Suspended", "date_of_birth": "1983-06-30", "profile_image": None, "health_details": "Migraines"}),

    ("Hannah Foster", "ID89012", "Member", "2020-04-25", ["+6677889900"], {"Husband": ("James Foster", "+1122334455")},
        {"address": "555 Willow St", "status": "Inactive", "date_of_birth": "1993-08-12", "profile_image": "hannah.png", "health_details": None}),

    ("Ian Green", "ID90123", "Admin", "2017-11-05", ["+7788990011"], {"Daughter": ("Charlotte Green", "+3344556677")},
        {"address": "666 Redwood St", "status": "Active", "date_of_birth": "1975-04-17", "profile_image": None, "health_details": "Arthritis"}),

    ("Jasmine Harris", "ID01234", "Treasurer", "2022-02-28", ["+8899001122"], {"Son": ("Daniel Harris", "+5566778899")},
        {"address": "777 Cypress St", "status": "Active", "date_of_birth": "1989-10-31", "profile_image": "jasmine.jpg", "health_details": "None"}),

    ("Kyle Irving", "ID11234", "Secretary", "2021-10-12", ["+9911223344"], {"Mother": ("Grace Irving", "+2233445566")},
        {"address": "888 Aspen St", "status": "Suspended", "date_of_birth": "1986-03-05", "profile_image": "kyle.png", "health_details": "Heart condition"}),

    ("Luna Jackson", "ID21234", "Member", "2019-06-08", ["+1122334455"], {"Father": ("Mason Jackson", "+3344556677")},
        {"address": "999 Cherry St", "status": "Inactive", "date_of_birth": "1992-12-25", "profile_image": None, "health_details": None}),

    ("Milo King", "ID31234", "Admin", "2018-08-30", ["+2233445566"], {"Wife": ("Ella King", "+6677889900")},
        {"address": "1000 Pear St", "status": "Active", "date_of_birth": "1984-09-15", "profile_image": "milo.jpg", "health_details": "Diabetes"}),

    ("Nina Lewis", "ID41234", "Treasurer", "2016-05-20", ["+3344556677"], {"Son": ("Benjamin Lewis", "+1122334455")},
        {"address": "1100 Walnut St", "status": "Active", "date_of_birth": "1979-01-22", "profile_image": None, "health_details": "None"}),

    ("Oscar Martinez", "ID51234", "Secretary", "2023-03-14", ["+4455667788"], {"Daughter": ("Ava Martinez", "+2233445566")},
        {"address": "1200 Plum St", "status": "Suspended", "date_of_birth": "1997-07-07", "profile_image": "oscar.png", "health_details": "None"}),

    ("Penelope Nelson", "ID61234", "Member", "2015-09-18", ["+5566778899"], {"Father": ("Ethan Nelson", "+4455667788")},
        {"address": "1300 Chestnut St", "status": "Inactive", "date_of_birth": "1982-05-11", "profile_image": None, "health_details": "Migraines"}),

    ("Quinn Oliver", "ID71234", "Admin", "2020-12-02", ["+6677889900"], {"Mother": ("Lily Oliver", "+7788990011")},
        {"address": "1400 Juniper St", "status": "Active", "date_of_birth": "1991-10-28", "profile_image": "quinn.jpg", "health_details": "Asthma"}),

    ("Riley Parker", "ID81234", "Treasurer", "2021-04-11", ["+7788990011"], {"Brother": ("Noah Parker", "+8899001122")},
        {"address": "1500 Fir St", "status": "Active", "date_of_birth": "1994-02-18", "profile_image": "riley.png", "health_details": None}),

    ("Sophia Quinn", "ID91234", "Secretary", "2018-07-27", ["+8899001122"], {"Sister": ("Jacob Quinn", "+9911223344")},
        {"address": "1600 Spruce St", "status": "Suspended", "date_of_birth": "1987-11-09", "profile_image": None, "health_details": "High BP"}),

    ("Theodore Roberts", "ID10123", "Member", "2017-01-22", ["+9911223344"], {"Daughter": ("Amelia Roberts", "+1122334455")},
        {"address": "1700 Pineapple St", "status": "Inactive", "date_of_birth": "1976-06-30", "profile_image": "theodore.jpg", "health_details": "None"}),
]
def get_member_by_name(cursor, name):
    """Fetch a member by their name."""
    cursor.row_factory = sqlite3.Row  # Enable column-name access

    query = """
    SELECT * FROM members WHERE name = ?
    """

    cursor.execute(query, (name,))
    row = cursor.fetchone()  # Fetch a single result

    if row:
        return DBRecord(cursor, row)  # Convert row to object
    else:
        return None  # Return None if no member is found

  

from pprint import pprint

def add_test_data_to_db(connection,crs):
    try:
        for member in test_members:
            add_member(crs, *member[:-1], **member[-1])  # Properly unpack arguments
        connection.commit()  # Save all changes to the database
    except Exception as e:
        connection.rollback()  # Undo changes if an error occurs
        print(f"Error: {e}")



if __name__ == "__main__":
#     # Create the database
    create_database("group_management.db")
    conn = sqlite3.connect("group_management.db")
    cursor = conn.cursor()
    #  pprint(get_member_details(cursor,5))
    # for memb in get_all_members_with_contacts(cursor):
    #     pprint(memb.name)
    add_test_data_to_db(conn,cursor)
    print("MEMBERS ADDED SUCCESSFULLY")
    conn.commit()
    conn.close()
    
