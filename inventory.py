import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, 
    QSplitter, QTextEdit, QPushButton, QStackedWidget,
    QFormLayout, QLineEdit, QMessageBox, QTableWidget,
    QTableWidgetItem, QDialog, QComboBox
    )
from PyQt5.QtCore import Qt
from new_id import NewID
from data_store_main import Engine

class AddInventory(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Inventory Record")
        self.setGeometry(100, 100, 400, 200)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.item_name = QLineEdit()
        self.quantity = QLineEdit()
        self.price_per_unit = QLineEdit()
        self.description = QLineEdit()

        form_layout.addRow(QLabel("Item Name:"), self.item_name)
        form_layout.addRow(QLabel("Quantity:"), self.quantity)
        form_layout.addRow(QLabel("Price per Unit:"), self.price_per_unit)
        form_layout.addRow(QLabel("Description:"), self.description)

        layout.addLayout(form_layout)

        add_button = QPushButton("Add Inventory Item")
        add_button.clicked.connect(self.add_inventory_item)
        layout.addWidget(add_button)

        self.setLayout(layout)

    def add_inventory_item(self):
        item_name = self.item_name.text()
        quantity = int(self.quantity.text())
        price_per_unit = float(self.price_per_unit.text())
        description = self.description.text()

        self.inventory_data = [item_name, quantity, price_per_unit, description]
        self.close()


class UpdateInventory(QDialog):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.setWindowTitle("Update Inventory Records")
        self.setGeometry(100, 100, 400, 200)
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.items = QComboBox()
        records = self.engine.get_current_inventory()
        self.data_items = {}
        for record in records:
            self.items.addItem(f"{record.item_name} (Current Quantity: {record.quantity})", record.id)
            self.data_items[record.id] = record.item_name
        
        self.new_quantity = QLineEdit()

        form_layout.addRow(QLabel("Select Item"), self.items)
        form_layout.addRow(QLabel("New Quantity"), self.new_quantity)

        layout.addLayout(form_layout)

        update_button = QPushButton("Update Quantity")
        update_button.clicked.connect(self.update_inventory)
        layout.addWidget(update_button)

        self.setLayout(layout)
    
    def update_inventory(self):
        item_id = self.items.currentData()
        new_quantity = int(self.new_quantity.text())
        item_name = self.data_items.get(item_id, "")
        self.details = [item_id, new_quantity, item_name]
        self.close()


class InventoryRecords(QWidget):
    def __init__(self):
        super().__init__()
        self.engine = Engine("inventory_records")
        self.session = self.engine.create_session()
        self.new_id = NewID()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Add buttons for adding and viewing inventory records
        add_inventory_button = QPushButton("Add Inventory")
        add_inventory_button.clicked.connect(self.add_inventory_record)
        layout.addWidget(add_inventory_button)

        # Update inventory button
        update_inventory_button = QPushButton("Update Inventory")
        update_inventory_button.clicked.connect(self.update_inventory_record)
        layout.addWidget(update_inventory_button)

        view_inventory_button = QPushButton("View Inventory Records")
        view_inventory_button.clicked.connect(self.view_inventory_records)
        layout.addWidget(view_inventory_button)

        self.setLayout(layout)
        self.setWindowTitle('Inventory Management')
        self.setGeometry(100, 100, 600, 400)

    def add_inventory_record(self):
        dialog = AddInventory()
        dialog.exec_()
        if hasattr(dialog, "inventory_data"):
            self.add_inventory(dialog.inventory_data)
    
    def add_inventory(self, data):
        print(data)
        item_name, quantity, price_per_unit, description = data

        idx = self.new_id.generate()
        kwargs = {
            "id":idx,
            "item_name":item_name,
            "quantity":quantity,
            "price_per_unit":price_per_unit,
            "description":description
        }
        result = self.engine.add_inventory(**kwargs)
        if result:
            QMessageBox.information(self, "Success", "Inventory added successfully...")

    def update_inventory_record(self, data):
        dialog = UpdateInventory(self.engine)
        dialog.exec_()
        if hasattr(dialog, "details"):
            self.update_inventory(dialog.details)

    def update_inventory(self, data):
        print(data)
        data_id, quantity, item_name = data
        result = self.engine.update_inventory(data_id, quantity)
        if result:
            QMessageBox.information(self, "Success", f"Inventory for {item_name} updated...")
        else:
            QMessageBox.warning(self, "Error", f"Failed to update inventory for {item_name}")

    def view_inventory_records(self):
        records = self.engine.get_current_inventory()
        self.show_records(records, ["ID", "Item Name", "Quantity", "Price per Unit", "Date Added", "Description"], "Inventory Records")

    def show_records(self, records, headers, title):
        table_widget = QTableWidget()
        table_widget.setRowCount(len(records))
        table_widget.setColumnCount(len(headers))
        table_widget.setHorizontalHeaderLabels(headers)

        for row, record in enumerate(records):
            table_widget.setItem(row, 0, QTableWidgetItem(str(record.id)))
            table_widget.setItem(row, 1, QTableWidgetItem(record.item_name))
            table_widget.setItem(row, 2, QTableWidgetItem(str(record.quantity)))
            table_widget.setItem(row, 3, QTableWidgetItem(str(record.price_per_unit)))
            table_widget.setItem(row, 4, QTableWidgetItem(record.date_added.strftime("%Y-%m-%d %H:%M:%S")))
            table_widget.setItem(row, 5, QTableWidgetItem(record.description))

        table_widget.setWindowTitle(title)
        table_widget.resize(800, 600)
        table_widget.show()
        self.record_table_widget = table_widget
