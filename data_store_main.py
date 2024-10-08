from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import datetime as dt

DataBase = declarative_base()

class Income(DataBase):
    __tablename__ = "income"

    id = Column(String, primary_key=True) #, autoincrement=True, default=1)
    source = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.now(dt.UTC))
    description = Column(String)

class Expenses(DataBase):
    __tablename__ = "expenses"

    id = Column(String, primary_key=True) #, autoincrement=True, default=1)
    category = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    date = Column(DateTime, default=datetime.now(dt.UTC))
    description = Column(String)

class Inventory(DataBase):
    __tablename__ = 'inventory'
    
    id = Column(String, primary_key=True) #, autoincrement=True, default=1)
    item_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price_per_unit = Column(Float, nullable=False)
    date_added = Column(DateTime, default=datetime.now(dt.UTC))
    description = Column(String)

class Engine():

    def __init__(self, db_name) -> None:
        # Set the database up
        DATABASE_URL = f"sqlite:///{db_name}.db"
        self.engine = create_engine(DATABASE_URL, echo=True)

        DataBase.metadata.create_all(self.engine)

    def create_session(self):
        """
        A function to create a session after initializing the database
        """
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        return self.session

    def add_income(self, **kwargs):
        """
        A function that interfaces with the database to create a record and add to it.
        """
        income = Income(**kwargs)
        self.session.add(income)
        self.session.commit()
        return True
    
    def add_expense(self, **kwargs):
        """
        A function that interfaces with the database and create a record and add to it.
        """
        expense = Expenses(**kwargs)
        self.session.add(expense)
        self.session.commit()
        return True

    def view_income(self):
        """
        A function to return all the income records
        """
        records = self.session.query(Income).all()
        return records
    
    def view_expense(self):
        """
        A function to return all the expense records.
        """
        records = self.session.query(Expenses).all()
        return records

    def add_inventory(self, **kwargs):
        """
        A function that interfaces with the database and creates an inventory.
        """
        inventory = Inventory(**kwargs)
        self.session.add(inventory)
        self.session.commit()
        return True

    def get_current_inventory(self):
        """
        A function to get the current inventory.
        """
        records = self.session.query(Inventory).all()
        return records
    
    def update_inventory(self, data_id, data):
        """
        A function to update the inventory record about an item.
        """
        record = self.session.query(Inventory).filter_by(id=data_id).first()
        if record:
            record.quantity = data
            self.session.commit()
            return True
        return False