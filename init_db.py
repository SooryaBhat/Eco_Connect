from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker
from app import Base, User, Bin, Complaint, WasteSale
from datetime import datetime, timedelta
import os

DATABASE_URL = os.environ.get('DATABASE_URL')
engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

demo_user = session.query(User).filter_by(username='demo_user').first()
if not demo_user:
    demo_user = User(username='demo_user',
                     email='user@example.com',
                     contact='1234567890',
                     role='User',
                     location='Mumbai')
    demo_user.set_password('password123')
    session.add(demo_user)

demo_collector = session.query(User).filter_by(
    username='demo_collector').first()
if not demo_collector:
    demo_collector = User(username='demo_collector',
                          email='collector@example.com',
                          contact='1234567891',
                          role='Collector',
                          location='Mumbai')
    demo_collector.set_password('password123')
    session.add(demo_collector)

demo_recycler = session.query(User).filter_by(username='demo_recycler').first()
if not demo_recycler:
    demo_recycler = User(username='demo_recycler',
                         email='recycler@example.com',
                         contact='1234567892',
                         role='Recycler',
                         location='Mumbai')
    demo_recycler.set_password('password123')
    session.add(demo_recycler)

demo_gov = session.query(User).filter_by(username='demo_gov').first()
if not demo_gov:
    demo_gov = User(username='demo_gov',
                    email='gov@example.com',
                    contact='1234567893',
                    role='Government',
                    location='Mumbai')
    demo_gov.set_password('password123')
    session.add(demo_gov)

bin1 = session.query(Bin).filter_by(bin_code='BIN001').first()
if not bin1:
    bin1 = Bin(bin_code='BIN001',
               location='Mumbai',
               recyclable_weight=35.5,
               non_recyclable_weight=28.3,
               capacity=100.0,
               last_cleaned=datetime.now() - timedelta(days=2))
    bin1.update_status()
    session.add(bin1)

bin2 = session.query(Bin).filter_by(bin_code='BIN002').first()
if not bin2:
    bin2 = Bin(bin_code='BIN002',
               location='Mumbai',
               recyclable_weight=75.0,
               non_recyclable_weight=10.0,
               capacity=100.0,
               last_cleaned=datetime.now() - timedelta(days=5))
    bin2.update_status()
    session.add(bin2)

bin3 = session.query(Bin).filter_by(bin_code='BIN003').first()
if not bin3:
    bin3 = Bin(bin_code='BIN003',
               location='Mumbai',
               recyclable_weight=15.0,
               non_recyclable_weight=10.0,
               capacity=100.0,
               last_cleaned=datetime.now() - timedelta(days=1))
    bin3.update_status()
    session.add(bin3)

session.commit()
session.close()

print("Database initialized successfully with demo data!")
print("\nDemo Accounts:")
print("User - username: demo_user, password: password123")
print("Collector - username: demo_collector, password: password123")
print("Recycler - username: demo_recycler, password: password123")
print("Government - username: demo_gov, password: password123")
print("\nDemo Bins: BIN001, BIN002, BIN003")
