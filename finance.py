import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, 
    QSplitter, QTextEdit, QPushButton, QStackedWidget,
    QFormLayout, QLineEdit, QMessageBox, QTableWidget,
    QTableWidgetItem, QDialog
    )
from PyQt5.QtCore import Qt
from random import choices
import string
from data_store_main import Engine


class AddIncome(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Income")
        self.setGeometry(200, 100, 400, 200)
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        self.income_source = QLineEdit()
        self.income_amount = QLineEdit()
        self.income_description = QLineEdit()

        form_layout.addRow(QLabel("Income Source:"), self.income_source)
        form_layout.addRow(QLabel("Amount:"), self.income_amount)
        form_layout.addRow(QLabel("Description:"), self.income_description)

        layout.addLayout(form_layout)

        add_button = QPushButton("Add Income")
        add_button.clicked.connect(self.add_income)
        layout.addWidget(add_button)

        self.setLayout(layout)
    
    def add_income(self):
        source = self.income_source.text()
        amount = float(self.income_amount.text())
        description = self.income_description.text()

        self.income_data = [source, amount, description]
        self.close()


class AddExpenses(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Expense")
        self.setGeometry(200, 100, 400, 200)
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        self.expense_category = QLineEdit()
        self.expense_amount = QLineEdit()
        self.expense_description = QLineEdit()

        form_layout.addRow(QLabel("Expenses Category:"), self.expense_category)
        form_layout.addRow(QLabel("Amount:"), self.expense_amount)
        form_layout.addRow(QLabel("Description:"), self.expense_description)

        layout.addLayout(form_layout)

        add_button = QPushButton("Add Expense")
        add_button.clicked.connect(self.add_expense)
        layout.addWidget(add_button)

        self.setLayout(layout)
    
    def add_expense(self):
        category = self.expense_category.text()
        amount = float(self.expense_amount.text())
        description = self.expense_description.text()
        
        self.expense_data = [category, amount, description]
        self.close()


class FinanceRecords(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.engine = Engine("financial_records")
        self.session = self.engine.create_session()
        # ID data strings
        self.characters = string.ascii_letters + string.digits
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Add forms 
        income_button = QPushButton("Add Income")
        income_button.clicked.connect(self.add_income_record)
        layout.addWidget(income_button)

        expense_button = QPushButton("Add Expense")
        expense_button.clicked.connect(self.add_expense_record)
        layout.addWidget(expense_button)

        # add to the layout
        # layout.addLayout(self.income_form)
        # layout.addLayout(self.expense_form)

        # Add view features
        income_view_button = QPushButton("View Income")
        income_view_button.clicked.connect(self.view_income)
        layout.addWidget(income_view_button)

        expense_view_button = QPushButton("View Expenses")
        expense_view_button.clicked.connect(self.view_expense)
        layout.addWidget(expense_view_button)

        self.setLayout(layout)
        self.setWindowTitle("Financial Records")
        self.setGeometry(100, 100, 600, 400)

    def add_income_record(self):
        dialog = AddIncome()
        dialog.exec_()
        if hasattr(dialog, "income_data"):
            self.add_income(dialog.income_data)
        
        dialog.close()
    
    def add_expense_record(self):
        dialog = AddExpenses()
        dialog.exec_()
        if hasattr(dialog, "expense_data"):
            self.add_expense(dialog.expense_data)
    
    def add_income(self, data):
        print(data)
        source, amount, description = data

        idx = self.generate_id()
        # add to the database
        result = self.engine.add_income(id=idx, source=source, amount=amount, description=description)

        if result:
            QMessageBox.information(self, "Success", "Income record added successfully...")
    
    def add_expense(self, data):
        print(data)
        category, amount, description = data

        idx = self.generate_id()
        # add to the database
        result = self.engine.add_expense(id=idx, category=category, amount=amount, description=description)

        if result:
            QMessageBox.information(self, "Success", "Expense record added successfully...")

    def view_income(self):
        records = self.engine.view_income()
        self.show_records(records, ["ID", "Source", "Amount", "Date", "Description"], "Income Records")
    
    def view_expense(self):
        records = self.engine.view_expense()
        self.show_records(records, ["ID", "Category", "Amount", "Date", "Description"], "Expense Records")
    
    def show_records(self, records, columns, title):
        table = QTableWidget()
        table.setRowCount(len(records))
        table.setColumnCount(len(columns))
        table.setHorizontalHeaderLabels(columns)

        for idx, record in enumerate(records):
            table.setItem(idx, 0, QTableWidgetItem(str(record.id)))
            table.setItem(idx, 1, QTableWidgetItem(record.source if hasattr(record, "source") else record.category))
            table.setItem(idx, 2, QTableWidgetItem(str(record.amount)))
            table.setItem(idx, 3, QTableWidgetItem(record.date.strftime("%Y-%m-%d %H:%M:%S")))
            table.setItem(idx, 4, QTableWidgetItem(record.description))
        
        table.setWindowTitle(title)
        table.resize(800, 600)
        table.show()
        self.table_record = table
    
    def generate_id(self, length=16):
        id_string = "".join(choices(self.characters, k=length))
        return id_string

if __name__ == "__main__":
    app = QApplication(sys.argv)

    finance_page = FinanceRecords()
    finance_page.show()

    sys.exit(app.exec_())