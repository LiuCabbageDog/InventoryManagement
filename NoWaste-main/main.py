'''
This is the main file of all the Application.
1. Use initializer.py to initialize database, make header, clear content.
2. Use inventory.py to add item, delete item, return item.
    2.1 Update item is actually delete and add a new one.
3. Use updateitem.py to refresh status in the database, and modify status manually.
4. Use show.py to return all kinds of needed inventory data.
5. Use visualization.py to show charts of inventory.

Programming Tool:

1. Use Matplotlib to create chart and diagram, reflecting the fluctuation of inventory.
2. Use tkinter to show front UI.
3. Use csv file "database" to store data.

'''
import inventory
import show

def main():
        inventory.add_item()

        show.ShowAsString()

        delete_id = input('please input id of the item you want to delete: ')
        inventory.delete_item(delete_id)

        show.ShowAsString()

main()