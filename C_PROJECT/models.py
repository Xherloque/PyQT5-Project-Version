from sqlalchemy import (
    create_engine, Column, Integer, String, Text, Date, ForeignKey, Numeric, CheckConstraint
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Define the Base class
Base = declarative_base()

class Member(Base):
    __tablename__ = "members"

    member_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    id_number = Column(String(20), unique=True, nullable=False)
    role = Column(String(20), CheckConstraint("role IN ('Admin', 'Treasurer', 'Secretary', 'Member')"))
    address = Column(Text)
    status = Column(String(20), CheckConstraint("status IN ('Active', 'Inactive', 'Suspended')"))
    contacts = Column(String(100), nullable=False)
    date_joined = Column(Date)
    date_of_birth = Column(Date)

    # Relationship with attendance, contributions, loans, and arrears
    attendances = relationship("Attendance", back_populates="member", cascade="all, delete")
    contributions = relationship("Contribution", back_populates="member", cascade="all, delete")
    loans = relationship("Loan", back_populates="member", cascade="all, delete")
    arrears = relationship("Arrear", back_populates="member", cascade="all, delete")

    def __repr__(self):
        return f"<Member(name={self.name}, role={self.role})>"


class Meeting(Base):
    __tablename__ = "meetings"

    meeting_id = Column(Integer, primary_key=True, autoincrement=True)
    meeting_date = Column(Date, nullable=False)
    agenda = Column(Text, nullable=False)
    facilitator = Column(String(100), nullable=False)
    attendance_count = Column(Integer, default=0)

    # Relationship with attendance and contributions
    attendances = relationship("Attendance", back_populates="meeting", cascade="all, delete")
    contributions = relationship("Contribution", back_populates="meeting", cascade="all, delete")

    def __repr__(self):
        return f"<Meeting(date={self.meeting_date}, agenda={self.agenda})>"


class Attendance(Base):
    __tablename__ = "attendance"

    attendance_id = Column(Integer, primary_key=True, autoincrement=True)
    meeting_id = Column(Integer, ForeignKey("meetings.meeting_id", ondelete="CASCADE"), nullable=False)
    member_id = Column(Integer, ForeignKey("members.member_id", ondelete="CASCADE"), nullable=False)

    # Relationships
    meeting = relationship("Meeting", back_populates="attendances")
    member = relationship("Member", back_populates="attendances")

    def __repr__(self):
        return f"<Attendance(meeting={self.meeting_id}, member={self.member_id})>"


class Contribution(Base):
    __tablename__ = "contributions"

    contribution_id = Column(Integer, primary_key=True, autoincrement=True)
    meeting_id = Column(Integer, ForeignKey("meetings.meeting_id", ondelete="SET NULL"))
    member_id = Column(Integer, ForeignKey("members.member_id", ondelete="CASCADE"), nullable=False)
    amount = Column(Numeric(10, 2), CheckConstraint("amount > 0"), nullable=False)
    payment_method = Column(String(20), CheckConstraint("payment_method IN ('Cash', 'Bank Transfer', 'Mobile Money')"))
    date_paid = Column(Date)

    # Relationships
    meeting = relationship("Meeting", back_populates="contributions")
    member = relationship("Member", back_populates="contributions")

    def __repr__(self):
        return f"<Contribution(member={self.member_id}, amount={self.amount})>"


class Loan(Base):
    __tablename__ = "loans"

    loan_id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey("members.member_id", ondelete="CASCADE"), nullable=False)
    amount = Column(Numeric(10, 2), CheckConstraint("amount > 0"), nullable=False)
    amount_paid = Column(Numeric(10, 2), default=0)
    status = Column(String(20), CheckConstraint("status IN ('Pending', 'Overdue', 'Partially Paid', 'Cleared')"))
    issue_date = Column(Date)
    due_date = Column(Date, nullable=False)

    # Relationship
    member = relationship("Member", back_populates="loans")

    def __repr__(self):
        return f"<Loan(member={self.member_id}, amount={self.amount}, status={self.status})>"




# Database connection
engine = create_engine("sqlite:///group_management.db", echo=True)

# Create all tables
Base.metadata.create_all(engine)

# Session
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()
