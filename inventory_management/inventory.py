
import csv
import pandas as pd  # Used for handling CSVs
from datetime import datetime
from .customer import Customer  # Import the Customer class
from .item import Item  # Import the Item class


class InsufficientQuantityError(Exception):
    #Custom exception for insufficient inventory quantity
    pass

class Inventory:
    def __init__(self):
        self.items = {}  # Items "stock", keys are item_id, values are item object associated
        self.customers = {}  # Dictionary to store customer objects, keys are customer_id
        self.purchase_history = []  # List of lists to store all individual purchase records (item_id, customer_id, quantity, purchase amount, date)
                                    # Will be used to write purchase history csv
    def add_item(self, item):  # Adds an item object to inventory stock items dictionary
        self.items[item.item_id] = item

    def update_price(self, item_id, new_price):
        # Check if item is in inventory items stock by key value, update corresponding item object price
        if item_id in self.items: 
            self.items[item_id].price = new_price
        else:
            print("Item not found.")

    def get_item(self, item_id):  
        # Retrieves item details and checks low stock
        # Retrieve item by its id, indexing ID as key in item stock dictionary
        item = self.items.get(item_id)
        # Check for valid item
        if item:
            if item.quantity <= 3: # Low stock warning (less than 3)
                print(f"Warning - Low {item.name} Stock! Quantity: {item.quantity}")
            return item # Item quantity will be adjusted in purchase_item method
        else:
            print("Item not found.")
            return None

    def update_purchase_csv(self):
        # Handle purchase_records csv to track each purchase made
        # Writer mode
        with open('purchase_records.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            # Each row in csv will be an individual purchase made with its necessary information
            # Header
            writer.writerow(['Item ID', 'Customer ID', 'Quantity', 'Purchase Amount', 'Date'])
            # Rewrite CSV with all purchases from purchase_history list
            # loop through each individual list inside big list and index accordingly
            for purchase in self.purchase_history:
                writer.writerow([purchase[0], purchase[1], purchase[2], purchase[3], purchase[4]])

    def assign_customer_ID(self, customer_name, customer_email):
        # Retrieve or create customer ID
        # Check if the customer already exists - if so, extract ID
        # Loop through customer dictionary with values (customer objects)
        for customer in self.customers.values():
            # If customer email found in customer dictionary - they have an ID, return
            if customer.email == customer_email:
                return customer.customer_id
        # Create a new customer since they don't exist already
        new_customer = Customer(customer_name, customer_email)
        # Add new customer to customer dictionary, key as their new ID (generated automatically by customer class)
        self.customers[new_customer.customer_id] = new_customer
        return new_customer.customer_id

    def purchase_item(self, item_id, quantity, customer_name, customer_email):
        # Check if the item exists in inventory
        item = self.get_item(item_id)
        if not item:
            print(f"Error: Item with ID {item_id} not found.")
            return

        # Check if the quantity is available
        if item.quantity < quantity:
            print(f"Error: Insufficient stock for {item.name}. Only {item.quantity} available.")
            return

        # Get or assign customer ID
        current_ID = self.assign_customer_ID(customer_name, customer_email)
        # current customer "object" that is purchasing / we are working with now 
        # Retrieved by ID from customer dictionary
        current_customer = self.customers[current_ID]

        # Log purchase in personal customer history
        current_customer.add_purchase(item_id, quantity, item.price)
        item.purchase(quantity) # purchase item - decreases individual item quantity in object

        # Log purchase in inventory purchase history list of lists - append
        purchase_record = [
            item_id,
            current_ID,
            quantity,
            quantity * item.price, 
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
        ] # total price and exact time of purchase included

        self.purchase_history.append(purchase_record)

        # Update overall purchase history csv for inventory tracking
        self.update_purchase_csv() 

        # Update customer CSV with all customer data
        # Either adds new customer, or updates existing data (total purchases, total spent)
        current_customer.update_customer_csv(self.customers)


    def generate_report(self):
        # Write txt report
        with open('inventory_report.txt', mode='w') as file:
            # Header with generation exact date
            file.write("Inventory Report\n")
            file.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            for item in self.items.values():  # Loop through items dictionary, item objects
                file.write(f"Item Name: {item.name}, Quantity: {item.quantity}\n")
                if item.quantity <= 3: # Write any low stock warnings
                    file.write(f"WARNING: Low {item.name} stock! Quantity: {item.quantity}\n")
                file.write("\n")

        print("Inventory report generated and saved to inventory_report.txt")

    def identify_top_customers_from_csv(self, customer_csv='Customer_Information.csv'):
        # List to store multiple, top customers over the spending threshold
        # list of lists [customer ID, total spend]
        top_customers = []
        # Read customer csv and ID spenders
        with open(customer_csv, mode='r') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header row when reading
            # loop through each row in csv
            for row in reader:
                try:
                    total_spent = float(row[4])  # Convert total spent to float for comparison
                    if total_spent > 5000: # top spender threshold
                        top_customers.append([row[0], total_spent])  # Add customer ID and total spent
                except ValueError:
                    print(f"Skipping row with invalid data: {row}")
        
        print("Top Customers:")
        # loop through each list of customer ID and total spent to print / return
        for spender in top_customers:
            print(f"Customer ID: {spender[0]}, Total Spent: {spender[1]}")
