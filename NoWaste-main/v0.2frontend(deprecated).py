import csv

def load_inventory_data():
    inventory_data = []
    # Use with statement to open the file and read data
    with open('database.csv', mode='r') as file:
        reader = csv.DictReader(file)  # Use DictReader to read CSV as dictionaries
        for row in reader:
            inventory_data.append(row)  # Append each row to inventory_data list
    return inventory_data  # Return the list of inventory data

#inventory_data = load_inventory_data()  # Call the function to load inventory data into memory





import tkinter as tk
from show import ShowAsDict
from updateitem import UpdateStatus
from inventory import delete_item
from visualization import SpendingByStoreChart, SpendingByMonthChart
from recipe import get_recipe
from show import ShowSpecifiedItem, ShowValidAsDict


#open inventory window
#create  window for inventory
inventory_window = tk.Toplevel()
inventory_window.title("Inventory")

#get the data of inventory
#call UpdateStatus first to ensure the data is updated before displaying

UpdateStatus()

#inventory_data = ShowAsDict()
inventory_data = load_inventory_data()  # 通过 load_inventory_data() 获取数据


#display the data in the new window
row = 0
for item in inventory_data:
    for col, key in enumerate(item):
        tk.Label(inventory_window, text=f"{key}: {item[key]}", font=("Helvetica", 10)).grid(row=row, column=col, padx=10, pady=5)
        row += 1


#delete Item Button
delete_button = tk.Button(inventory_window, text="Delete Item", 
                          font=("Helvetica", 12, "bold"), bg="#ffcccc", 
                          command=lambda: delete_item(id))  #pass the ID as required
delete_button.grid(row=0, column=0, padx=10, pady=5)

#total Spend by Store Button
store_spend_button = tk.Button(inventory_window, text="Total Spend by Store", 
                               font=("Helvetica", 12, "bold"), bg="#ccffcc", 
                               command=SpendingByStoreChart)  #function call for store spending
store_spend_button.grid(row=1, column=0, padx=10, pady=5)

#monthly Spend Button
monthly_spend_button = tk.Button(inventory_window, text="Monthly Spend", 
                                 font=("Helvetica", 12, "bold"), bg="#ccffff", 
                                 command=SpendingByMonthChart)  #function call for monthly spending
monthly_spend_button.grid(row=2, column=0, padx=10, pady=5)

#random Recipe Suggestion Button
recipe_button = tk.Button(inventory_window, text="Get Recipe Suggestion", 
                          font=("Helvetica", 12, "bold"), bg="#ffffcc", 
                          command=get_recipe)  #function call for recipe suggestion
recipe_button.grid(row=3, column=0, padx=10, pady=5)

 #create price comparison button 应该写在inventory window里
price_button = tk.Button(inventory_window, text="Compare Prices", 
                         font=("Helvetica", 12, "bold"), bg="#ccffff", command=ShowSpecifiedItem)
price_button.grid(row=21, column=0, columnspan=2)

 #create reminder button 应该写在inventory window里
reminder_button = tk.Button(inventory_window, text="Check Stock", 
                            font=("Helvetica", 12, "bold"), bg="#ccffff", command=ShowValidAsDict)
reminder_button.grid(row=20, column=0, columnspan=2)

    
inventory_window.mainloop()
