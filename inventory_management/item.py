
from datetime import datetime

class Item:
    last_unique_ID = 0 # ID counter to name each item entered uniquely 
    def __init__(self,name,brand,price,quantity):
        self.item_id = Item.last_unique_ID # assign unique ID
        Item.last_unique_ID += 1 # increment class variable for next item
        self.name = name.title() # capitalize here
        self.brand = brand.title() # capitalize here
        self.price = price
        self.quantity = quantity
        self.update_date = datetime.now().date()

    def update_price(self, new_price):
        self.price = new_price

    def purchase(self, num_items):
        self.quantity -= num_items 
