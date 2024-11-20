
import csv
import pandas as pd  # Used for handling CSVs
from datetime import datetime

class Customer:
    def __init__(self,name,email):
        self.name = name.title() # capitialize name
        self.email = email
        self.customer_id = self.generate_customer_ID() # create unique customer ID
        self.purchase_history = [] # list of lists, each list inside is a purchase [Item ID,Quantity,Date]
        self.total_spent = 0 # total spent by customer overall - used later to ID top customers

    def generate_customer_ID(self):
        prefix = self.email.split("@")[0]  # create unique ID with customer email and date of creation
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")  # ex: "20231110123045"
        return f"{prefix}_{timestamp}"
        
    def add_purchase(self, item_ID, quantity, price):
        # Validate quantity and price
        if quantity <= 0 or price <= 0:
            raise ValueError("Quantity and price must be positive numbers.")

        total_price = price * quantity # total purchase price
        self.total_spent += total_price # add to overall customer total
        # add purchase to purchase_history list of lists
        self.purchase_history.append([item_ID, quantity, datetime.now().date(), total_price])

    def get_purchase_history(self):
        # loop through history list and index each list to extract history details
        for item in self.purchase_history:
            print(f"Item ID: {item[0]}, Quantity: {item[1]}, Date: {item[2]}")
    
    def update_customer_csv(self, all_customers):
        # Handle master customer CSV inventory
        # Write mode
        with open('Customer_Information.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write each row of csv file, each row will be an individual customer and their details
            # Header
            writer.writerow(['Customer ID', 'Name', 'Email', 'Total Purchases', 'Total Spent'])
            
            # Iterate over Customer objects not keys here so we can extract customer object details
            for customer in all_customers.values():
                writer.writerow([customer.customer_id, customer.name, customer.email, len(customer.purchase_history), customer.total_spent])
