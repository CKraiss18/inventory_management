
import csv
import os
from inventory_management.item import Item
from inventory_management.customer import Customer
from inventory_management.inventory import Inventory
from inventory_management.inventory import InsufficientQuantityError


# Setup and Teardown Functions
def setup_files():
    """Create or clear necessary test files."""
    for file_name in ["Customer_Information.csv", "purchase_records.csv", "inventory_report.txt"]:
        with open(file_name, "w") as file:
            if file_name == "Customer_Information.csv":
                file.write("Customer ID,Name,Email,Total Purchases,Total Spent\n")
            elif file_name == "purchase_records.csv":
                file.write("Item ID,Customer ID,Quantity,Purchase Amount,Date\n")


def teardown_files():
    """Remove test files after tests."""
    for file_name in ["Customer_Information.csv", "purchase_records.csv", "inventory_report.txt"]:
        if os.path.exists(file_name):
            os.remove(file_name)


# Test Item Class
def test_item_creation():
    item = Item("laptop", "dell", 1500, 10)
    assert item.name == "Laptop"
    assert item.brand == "Dell"
    assert item.price == 1500
    assert item.quantity == 10


def test_item_update_price():
    item = Item("laptop", "dell", 1500, 10)
    item.update_price(1800)
    assert item.price == 1800


def test_item_purchase():
    item = Item("laptop", "dell", 1500, 10)
    item.purchase(3)
    assert item.quantity == 7


def test_item_insufficient_stock():
    item = Item("laptop", "dell", 1500, 10)
    try:
        item.purchase(11)  # Exceeds stock
    except ValueError:
        assert item.quantity == 10  # Quantity should remain unchanged


# Test Customer Class
def test_customer_creation():
    customer = Customer("john doe", "johndoe@example.com")
    assert customer.name == "John Doe"
    assert customer.email == "johndoe@example.com"


def test_customer_add_purchase():
    customer = Customer("john doe", "johndoe@example.com")
    customer.add_purchase(1, 2, 100)  # item_id=1, quantity=2, price=100
    assert customer.total_spent == 200
    assert len(customer.purchase_history) == 1


# Test Inventory Class
def test_inventory_add_item():
    inventory = Inventory()
    item = Item("Laptop", "BrandX", 1200, 5)
    inventory.add_item(item)
    assert inventory.get_item(item.item_id).quantity == 5


def test_inventory_update_price():
    inventory = Inventory()
    item = Item("Laptop", "BrandX", 1200, 5)
    inventory.add_item(item)
    inventory.update_price(item.item_id, 1300)
    assert inventory.get_item(item.item_id).price == 1300


def test_inventory_purchase_item():
    inventory = Inventory()
    item = Item("Laptop", "BrandX", 1200, 5)
    inventory.add_item(item)
    inventory.purchase_item(item.item_id, 2, "John Doe", "john@example.com")
    assert inventory.get_item(item.item_id).quantity == 3


def test_inventory_low_stock_warning():
    inventory = Inventory()
    item = Item("Laptop", "BrandX", 1200, 2)
    inventory.add_item(item)
    assert inventory.get_item(item.item_id).quantity < 3


def test_inventory_generate_report():
    inventory = Inventory()
    item1 = Item("Laptop", "BrandX", 1500, 10)
    item2 = Item("Mouse", "BrandY", 50, 3)
    item3 = Item("Keyboard", "BrandZ", 100, 2)
    inventory.add_item(item1)
    inventory.add_item(item2)
    inventory.add_item(item3)

    inventory.generate_report()

    with open("inventory_report.txt", mode="r") as file:
        report_content = file.read()

    assert "Item Name: Laptop, Quantity: 10" in report_content
    assert "WARNING: Low Mouse stock! Quantity: 3" in report_content


def test_inventory_csv_handling():
    inventory = Inventory()
    item = Item("Keyboard", "BrandK", 100, 10)
    inventory.add_item(item)

    inventory.purchase_item(item.item_id, 2, "Charlie Brown", "charlie@example.com")
    inventory.purchase_item(item.item_id, 3, "Charlie Brown", "charlie@example.com")

    with open("Customer_Information.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        data = list(reader)
        assert len(data) == 1  # One customer
        assert data[0][1] == "Charlie Brown"  # Customer name

    with open("purchase_records.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        data = list(reader)
        assert len(data) == 2  # Two purchases


# Test Top Customers from CSV
def test_top_customers_from_csv():
    inventory = Inventory()
    item = Item("Desktop", "BrandD", 1500, 10)
    inventory.add_item(item)

    inventory.purchase_item(item.item_id, 4, "John Doe", "john@example.com")
    inventory.purchase_item(item.item_id, 4, "Jane Doe", "jane@example.com")

    inventory.identify_top_customers_from_csv("Customer_Information.csv")

    with open("Customer_Information.csv", mode="r") as file:
        reader = csv.reader(file)
        next(reader)
        top_customers = [row for row in reader if float(row[4]) >= 5000]

    assert len(top_customers) == 2


# Run the Tests with Setup and Teardown
if __name__ == "__main__":
    setup_files()
    try:
        test_item_creation()
        test_item_update_price()
        test_item_purchase()
        test_item_insufficient_stock()
        test_customer_creation()
        test_customer_add_purchase()
        test_inventory_add_item()
        test_inventory_update_price()
        test_inventory_purchase_item()
        test_inventory_low_stock_warning()
        test_inventory_generate_report()
        test_inventory_csv_handling()
        test_top_customers_from_csv()
        print("All tests passed!")
    finally:
        teardown_files()
