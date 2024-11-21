# Inventory Management Package

This is a Python package for managing inventory, customer tracking, and generating reports. It is designed to help businesses handle inventory efficiently, monitor customer activities, and generate insightful reports.

## Features
- Add and update items in inventory
- Track customer purchases with automatic ID assignment
- Generate inventory reports with low-stock warnings
- Identify top customers from purchase history stored in CSV files

## Installation

To install the package locally:

1. Clone the repository or download the source code.
   ```bash
   git clone https://github.com/CKraiss18/inventory_management.git
   cd inventory_management

2. Install the package.
    ```bash
    pip install -e .

## Requirements

The package requires the following dependencies:

- pandas: For handling CSV files
- datetime: For timestamp generation (standard library)
- csv: For writing and reading CSV files (standard library)

## Usage

Importing the Package:

After installation, you can import the package and use its components:

    from inventory_management import Inventory, Item, Customer

    # Create an inventory instance
    inventory = Inventory()

    # Add an item to the inventory
    item = Item("Laptop", "BrandX", 1500, 10)
    inventory.add_item(item)

    # Purchase an item
    inventory.purchase_item(item.item_id, 2, "John Doe", "john@example.com")

    # Generate a report
    inventory.generate_report()

## Running Tests

The package includes a suite of tests to validate its functionality. To run the tests, navigate to the package directory and execute the following command:
`python tests/test_inventory.py`

### Important Notes:

File Cleanup: During the tests, several files (Customer_Information.csv, purchase_records.csv, and inventory_report.txt) are created to validate CSV handling and report generation. However, these files are automatically removed at the end of the test suite using a cleanup process (teardown_files()).
Viewing Generated Files: If you wish to inspect the generated files during testing:

- Comment out the teardown_files() function in the test file (tests/test_inventory.py).
- Alternatively, modify the teardown_files() function to exclude specific files from being removed (e.g., inventory_report.txt).

### In Normal Use:
When the package is used outside of testing, the generated files will persist and will not be automatically removed. These files are designed to provide actionable data:

- Customer_Information.csv: Tracks customer information and purchase history.
- purchase_records.csv: Logs all purchase transactions.
- inventory_report.txt: Contains inventory details and low-stock warnings.


## File Outputs

The package creates the following CSV files:

- Customer_Information.csv: Contains customer details, including purchase history and total amount spent.
- purchase_records.csv: Logs all purchases made through the system.
- inventory_report.txt: Provides a detailed inventory report, including low-stock warnings.

## Contributing

Contributions are welcome! If you find bugs or have suggestions for new features, please open an issue or submit a pull request on GitHub.

## Author
Charlee Kraiss
Email: charlee.e.kraiss@vanderbilt.com
