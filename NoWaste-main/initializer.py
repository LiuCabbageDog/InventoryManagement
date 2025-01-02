import csv

def main():
    InitializeDatabase()

# Initialize the fields included in an inventory. This will clear all data in the dabase file.
def InitializeDatabase():
        fields = [['Name', 'ID', 'Category', 'Quantity', 'Unit of Quantity', 'Purchase Date',
                   'Expired Date', 'Status', 'Total Price', 'Store']]
        with open('database.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(fields)

main()