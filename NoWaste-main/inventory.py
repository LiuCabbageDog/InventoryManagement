import csv # library for managing csv file

# Add new items into inventroy.
'''
1. status = ['Normal','Expiring soon', 'Expired', 'Used', 'Invalid date']
        Normal status is longer than 3 days before expired date
        Expiring soon status is within 3 days before expired date
        Expired status is after expired date
        Used status is past and invalid item, all 3 status above is unused status.
2. editing item can be simplified to delet first and then add it back.

'''
def add_item(user_input):
        # input fields of a new item into a list.
        # input item name, item id, category, quantity, unit of quantity, purchase date, expired date, status, total price, where you buy.
        # Every data is separated by comma.
        new_item = []
        new_item = user_input.split(',')

        # input error handling.
        if (len(new_item) != 10): # Use a constant here, can be optimized in the future.
                print("Input wrong number of fields!\n")
                return

        # put the new item list into databse.
        fields = [new_item]
        with open('database.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(fields)

        '''
        Input data separately as below:

        Name = input("Please input item name")
        new_item.append(Name)

        Category = input("Please input item category")
        new_item.append(Category)

        Quantity = input("Please input item quantity")
        new_item.append(Quantity)

        Quantity_Unit = input("Please input unit of quantity")
        new_item.append(Quantity_Unit)

        Date_Purchase = input("Please input item purchase date")
        new_item.append(Date_Purchase)

        Shelf_Life = input("Please input item shelf life")
        new_item.append(Shelf_Life)

        # In future iteration, Expired Date can be calcualted based on its shelf life.
        Date_Expired = input("Please input item expired date")
        new_item.append(Date_Expired)

        # In future iteration, status can be estimated based on expired date.
        Status = input("Please input item status")
        new_item.append(Status)

        Total_Price = input("Please input item total price")
        new_item.append(Total_Price)

        Store = input("Please input where you buy this item")
        new_item.append(Store)
        '''

# delete specified row with id, id is a string.
def delete_item(id):
        # Write a new table except which we want to delete. Here is an empty list waits for qualified data.
        new_table = []
        fieldnames = None

        # Search specified rows, construct new table without them.
        with open('database.csv', 'r') as file:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames # To get fieldnames. Without this line, field name will lose.
                for row in reader:
                        if (row['ID'] != id):
                                new_table.append(row)

        # Overwrite original file.
        with open('database.csv', 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(new_table)
