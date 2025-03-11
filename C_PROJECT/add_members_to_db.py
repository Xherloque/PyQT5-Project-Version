import sqlite3
from datetime import datetime

# Updated test data to match the schema (added date_of_birth placeholder)
test_data = [
    (1, "Aisha Hassan", "1234567890123", "ChairPerson", "Apartment 5B, Acacia Avenue, Nairobi", "Active", ["aisha.hassan@email.com", "+254712345678"], "2023-01-15", "1985-05-12"),
    (2, "John Mwangi", "9876543210987", "Treasurer", "House No. 10, Kijabe Street, Nairobi", "Active", ["john.mwangi@email.com", "+254723456789", "+254111222333"], "2023-02-20", "1978-11-23"),
    (3, "Fatima Omondi", "1122334455667", "Secretary", "Plot 23, Riverside Drive, Nairobi", "Inactive", ["fatima.omondi@email.com"], "2023-03-25", "1990-03-15"),
    (4, "David Kamau", "6677889900112", "Member", "Flat C7, Ngong Road, Nairobi", "Active", ["david.kamau@email.com", "+254734567890"], "2023-04-30", "1982-07-19"),
    (5, "Sarah Wambui", "2233445566778", "Assistant ChairPerson", "Villa 15, Karen Road, Nairobi", "Active", ["sarah.wambui@email.com", "+254745678901"], "2023-05-05", "1987-09-25"),
    (6, "Peter Onyango", "8899001122334", "Assistant Treasurer", "Building 8, Lavington, Nairobi", "Inactive", ["peter.onyango@email.com", "+254756789012"], "2023-06-10", "1992-12-30"),
    (7, "Grace Akinyi", "3344556677889", "Member", "Suite 22, Westlands, Nairobi", "Active", ["grace.akinyi@email.com"], "2023-07-15", "1989-04-10"),
    (8, "Samuel Kimani", "9900112233445", "Member", "House 4, Runda Estate, Nairobi", "Active", ["samuel.kimani@email.com", "+254767890123"], "2023-08-20", "1983-06-18"),
    (9, "Lucy Njeri", "4455667788990", "Assistant Secretary", "Apartment 9A, Kilimani, Nairobi", "Inactive", ["lucy.njeri@email.com", "+254778901234"], "2023-09-25", "1991-01-22"),
    (10, "Michael Otieno", "0011223344556", "Member", "Plot 56, South C, Nairobi", "Active", ["michael.otieno@email.com"], "2023-10-30", "1984-08-05"),
    (11, "Jane Mutua", "5566778899001", "Member", "House 2, Eastleigh, Nairobi", "Active", ["jane.mutua@email.com", "+254789012345"], "2023-11-05", "1986-02-14"),
    (12, "Victor Maina", "1122334455667", "Member", "Apartment 12B, Umoja, Nairobi", "Inactive", ["victor.maina@email.com"], "2023-12-10", "1993-03-03"),
    (13, "Esther Wangari", "6677889900112", "Member", "Plot 3, Embakasi, Nairobi", "Active", ["esther.wangari@email.com", "+254790123456"], "2024-01-15", "1988-07-07"),
    (14, "Daniel Mwangi", "2233445566778", "Member", "House 7, Dandora, Nairobi", "Active", ["daniel.mwangi@email.com"], "2024-02-20", "1981-05-20"),
    (15, "Mercy Cherono", "8899001122334", "Member", "Apartment 1, Kayole, Nairobi", "Inactive", ["mercy.cherono@email.com", "+254701234567"], "2024-03-25", "1994-09-09"),
    (16, "Kevin Odhiambo", "7788990011223", "Member", "P.O. Box 1234, Nairobi", "Active", ["kevin.odhiambo@email.com"], "2024-04-30", "1985-11-11"),
    (17, "Emily Wanjiku", "3344556677889", "Member", "Flat 4D, Langata, Nairobi", "Active", ["emily.wanjiku@email.com", "+254711223344"], "2024-05-05", "1987-10-10"),
    (18, "Brian Juma", "9900112233445", "Member", "House 9, Buruburu, Nairobi", "Inactive", ["brian.juma@email.com"], "2024-06-10", "1990-06-06"),
    (19, "Caroline Moraa", "4455667788990", "Member", "Apartment 10C, Kileleshwa, Nairobi", "Active", ["caroline.moraa@email.com", "+254722334455"], "2024-07-15", "1983-08-08"),
    (20, "Anthony Kioko", "0011223344556", "Member", "Plot 18, Donholm, Nairobi", "Active", ["anthony.kioko@email.com"], "2024-08-20", "1989-12-12"),
    (21, "Rose Jeptoo", "5566778899001", "Member", "Villa 7, Muthaiga, Nairobi", "Inactive", ["rose.jeptoo@email.com", "+254733445566"], "2024-09-25", "1984-04-04"),
    (22, "Joseph Njoroge", "1122334455667", "Member", "Building 3, Parklands, Nairobi", "Active", ["joseph.njoroge@email.com"], "2024-10-30", "1982-02-02"),
    (23, "Catherine Wanjala", "6677889900112", "Member", "Suite 11, Upper Hill, Nairobi", "Active", ["catherine.wanjala@email.com", "+254744556677"], "2024-11-05", "1986-06-06"),
    (24, "Patrick Ochieng", "2233445566778", "Member", "House 12, Industrial Area, Nairobi", "Inactive", ["patrick.ochieng@email.com"], "2024-12-10", "1991-09-09"),
    (25, "Faith Chebet", "8899001122334", "Member", "Apartment 6E, Madaraka, Nairobi", "Active", ["faith.chebet@email.com", "+254755667788"], "2025-01-15", "1988-03-03"),
    (26, "Alice Kariuki", "1234567890124", "Member", "House 1, Kileleshwa, Nairobi", "Active", ["alice.kariuki@email.com", "+254712345679"], "2025-02-20", "1985-01-01"),
    (27, "James Karanja", "9876543210988", "Member", "Apartment 2B, Westlands, Nairobi", "Inactive", ["james.karanja@email.com", "+254723456780"], "2025-03-25", "1980-02-02"),
    (28, "Mary Njeri", "1122334455668", "Member", "Flat 3C, Kilimani, Nairobi", "Active", ["mary.njeri@email.com"], "2025-04-30", "1990-03-03"),
    (29, "Paul Otieno", "6677889900113", "Member", "House 4, Karen, Nairobi", "Active", ["paul.otieno@email.com", "+254734567891"], "2025-05-05", "1982-04-04"),
    (30, "Nancy Wambui", "2233445566779", "Member", "Apartment 5D, Lavington, Nairobi", "Inactive", ["nancy.wambui@email.com"], "2025-06-10", "1987-05-05"),
    (31, "George Mwangi", "8899001122335", "Member", "House 6, Runda, Nairobi", "Active", ["george.mwangi@email.com", "+254756789013"], "2025-07-15", "1989-06-06"),
    (32, "Helen Akinyi", "3344556677890", "Member", "Flat 7E, Ngong Road, Nairobi", "Inactive", ["helen.akinyi@email.com"], "2025-08-20", "1991-07-07"),
    (33, "Charles Kimani", "9900112233446", "Member", "House 8, Kijabe Street, Nairobi", "Active", ["charles.kimani@email.com", "+254767890124"], "2025-09-25", "1983-08-08"),
    (34, "Irene Njoroge", "4455667788991", "Member", "Apartment 9F, Acacia Avenue, Nairobi", "Inactive", ["irene.njoroge@email.com"], "2025-10-30", "1984-09-09"),
    (35, "Patrick Mwangi", "0011223344557", "Member", "House 10, Riverside Drive, Nairobi", "Active", ["patrick.mwangi@email.com"], "2025-11-05", "1985-10-10"),
    (36, "Susan Wanjiku", "5566778899002", "Member", "Flat 11G, Westlands, Nairobi", "Inactive", ["susan.wanjiku@email.com"], "2025-12-10", "1986-11-11"),
    (37, "Martin Omondi", "1122334455669", "Member", "House 12, Ngong Road, Nairobi", "Active", ["martin.omondi@email.com", "+254789012346"], "2026-01-15", "1987-12-12"),
    (38, "Grace Mwangi", "6677889900114", "Member", "Apartment 13H, Kileleshwa, Nairobi", "Inactive", ["grace.mwangi@email.com"], "2026-02-20", "1988-01-13"),
    (39, "Peter Kamau", "2233445566780", "Member", "House 14, Karen Road, Nairobi", "Active", ["peter.kamau@email.com", "+254701234568"], "2026-03-25", "1989-02-14"),
    (40, "Lucy Wambui", "8899001122336", "Member", "Flat 15I, Lavington, Nairobi", "Inactive", ["lucy.wambui@email.com"], "2026-04-30", "1990-03-15"),
    (41, "John Otieno", "3344556677891", "Member", "House 16, Runda Estate, Nairobi", "Active", ["john.otieno@email.com"], "2026-05-05", "1981-04-16"),
    (42, "Esther Akinyi", "9900112233447", "Member", "Apartment 17J, Kilimani, Nairobi", "Inactive", ["esther.akinyi@email.com"], "2026-06-10", "1982-05-17"),
    (43, "David Njoroge", "4455667788992", "Member", "House 18, Kijabe Street, Nairobi", "Active", ["david.njoroge@email.com", "+254722334456"], "2026-07-15", "1983-06-18"),
    (44, "Jane Mwangi", "0011223344558", "Member", "Flat 19K, Acacia Avenue, Nairobi", "Inactive", ["jane.mwangi@email.com"], "2026-08-20", "1984-07-19"),
    (45, "Michael Kariuki", "5566778899003", "Member", "House 20, Riverside Drive, Nairobi", "Active", ["michael.kariuki@email.com"], "2026-09-25", "1985-08-20"),
    (46, "Sarah Omondi", "1122334455670", "Member", "Apartment 21L, Westlands, Nairobi", "Inactive", ["sarah.omondi@email.com"], "2026-10-30", "1986-09-21"),
    (47, "Paul Wanjiku", "6677889900115", "Member", "House 22, Ngong Road, Nairobi", "Active", ["paul.wanjiku@email.com"], "2026-11-05", "1987-10-22"),
    (48, "Nancy Kamau", "2233445566781", "Member", "Flat 23M, Kileleshwa, Nairobi", "Inactive", ["nancy.kamau@email.com"], "2026-12-10", "1988-11-23"),
    (49, "George Wambui", "8899001122337", "Member", "House 24, Karen Road, Nairobi", "Active", ["george.wambui@email.com"], "2027-01-15", "1989-12-24"),
    (50, "Helen Mwangi", "3344556677892", "Member", "Apartment 25N, Lavington, Nairobi", "Inactive", ["helen.mwangi@email.com"], "2027-02-20", "1990-01-25"),
]

def add_member(db_name, member_data):
    """Adds a member and their contacts to the database."""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Insert into the `members` table
        query = """
            INSERT INTO members (full_name, national_id, role, address, date_joined, date_of_birth)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (member_data[1], member_data[2], member_data[3], member_data[4], member_data[7], member_data[8]))
        member_id = cursor.lastrowid  # Get the inserted member's ID

        # Insert contacts into the `group_contacts` table
        contact_query = """
            INSERT INTO group_contacts (member_id, contact)
            VALUES (?, ?)
        """
        for contact in member_data[6]:  # Use index 6 to match contacts field
            cursor.execute(contact_query, (member_id, contact))

        conn.commit()
        print(f"Added member: {member_data[1]}")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def fill_test_data(db_name, tsd=test_data):
    """Fills the database with test data."""
    for member in tsd:
        add_member(db_name, member)
        
def retrieve_members(db_name):
    """Retrieves all members and their contacts from the database."""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Retrieve members
        cursor.execute("SELECT * FROM members")
        members = cursor.fetchall()

        # Retrieve contacts
        cursor.execute("SELECT member_id, contact FROM group_contacts")
        contacts = cursor.fetchall()

        # Organize contacts by member_id
        contacts_dict = {}
        for member_id, contact in contacts:
            if member_id not in contacts_dict:
                contacts_dict[member_id] = []
            contacts_dict[member_id].append(contact)

        # Combine members and their contacts
        result = []
        for member in members:
            member_id = member[0]
            member_data = list(member)
            member_data.append(contacts_dict.get(member_id, []))
            result.append(tuple(member_data))

        return result
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        conn.close()
      
from pprint import pprint
  
if __name__ == "__main__":
    db_name = "group_management.db"
    # fill_test_data(db_name, test_data)
    pprint(retrieve_members(db_name))
