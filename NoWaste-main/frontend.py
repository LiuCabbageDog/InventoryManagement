import tkinter as tk
import show
import inventory
import updateitem
import recipe
import visualization

def showExistingItem():
    valid_inventory = show.ShowValidAsDict()
    counter = 0
    for dic in valid_inventory:
        tk.Label(root, text=dic["Name"]).grid(row=(2+counter), column=0, sticky='w', padx=5, pady=5)
        tk.Label(root, text=dic["ID"]).grid(row=(2+counter), column=1, sticky='w', padx=5, pady=5)
        tk.Label(root, text=dic["Category"]).grid(row=(2+counter), column=2, sticky='w', padx=5, pady=5)
        tk.Label(root, text=dic["Quantity"]).grid(row=(2+counter), column=3, sticky='w', padx=5, pady=5)
        tk.Label(root, text=dic["Unit of Quantity"]).grid(row=(2+counter), column=4, sticky='w', padx=5, pady=5)
        tk.Label(root, text=dic["Purchase Date"]).grid(row=(2+counter), column=5, sticky='w', padx=5, pady=5)
        tk.Label(root, text=dic["Expired Date"]).grid(row=(2+counter), column=6, sticky='w', padx=5, pady=5)
        tk.Label(root, text=dic["Status"]).grid(row=(2+counter), column=7, sticky='w', padx=5, pady=5)
        tk.Label(root, text=dic["Total Price"]).grid(row=(2+counter), column=8, sticky='w', padx=5, pady=5)
        tk.Label(root, text=dic["Store"]).grid(row=(2+counter), column=9, sticky='w', padx=5, pady=5)
        counter += 1

def showItem(window, itemlist):
    counter = 0
    for dic in itemlist:
        tk.Label(window, text=dic["Name"]).grid(row=(2+counter), column=0, sticky='w', padx=5, pady=5)
        tk.Label(window, text=dic["ID"]).grid(row=(2+counter), column=1, sticky='w', padx=5, pady=5)
        tk.Label(window, text=dic["Category"]).grid(row=(2+counter), column=2, sticky='w', padx=5, pady=5)
        tk.Label(window, text=dic["Quantity"]).grid(row=(2+counter), column=3, sticky='w', padx=5, pady=5)
        tk.Label(window, text=dic["Unit of Quantity"]).grid(row=(2+counter), column=4, sticky='w', padx=5, pady=5)
        tk.Label(window, text=dic["Purchase Date"]).grid(row=(2+counter), column=5, sticky='w', padx=5, pady=5)
        tk.Label(window, text=dic["Expired Date"]).grid(row=(2+counter), column=6, sticky='w', padx=5, pady=5)
        tk.Label(window, text=dic["Status"]).grid(row=(2+counter), column=7, sticky='w', padx=5, pady=5)
        tk.Label(window, text=dic["Total Price"]).grid(row=(2+counter), column=8, sticky='w', padx=5, pady=5)
        tk.Label(window, text=dic["Store"]).grid(row=(2+counter), column=9, sticky='w', padx=5, pady=5)
        counter += 1

def cleanWindow():
    for widget in root.grid_slaves():
        if int(widget.grid_info()["row"]) > 1:  # 排除第一行标题
            widget.grid_forget()

# Creat Main Window
root = tk.Tk()
root.title("NoWaste")

# Set column width
for i in range(10):
    root.grid_columnconfigure(i, minsize=130)  # 设置第 i 列宽度为 130 像素

# Set title in the window
title_label = tk.Label(root, text="Your Existing Ingredients", font=("Arial", 20))
title_label.grid(sticky='w', row=0, column=0, columnspan=2, pady=20, padx=5)

# Set header of the form
fields = ['Name', 'ID', 'Category', 'Quantity', 'Unit of Quantity', 'Purchase Date',
          'Expired Date', 'Status', 'Total Price', 'Store']
for i in range(10):
    tk.Label(root, text=fields[i]).grid(row=1, column=i, sticky='w', padx=5, pady=5)

# show data of the form
updateitem.UpdateStatus()
showExistingItem();

# Add item into the form
def open_addwindow():
    # Creat a new window
    new_window = tk.Toplevel(root)
    new_window.title("Add Ingredient")
    
    # Creat element in the new window
    tk.Label(new_window, text="Name, ID, Category, Quantity, Unit of Quantity, Purchase Date, Expired Date, Status, Total Price, Store")\
        .grid(sticky='w', row=0, column=0, pady=5, padx=5)
    entry = tk.Entry(new_window, width=80)
    entry.grid(row=1, column=0, sticky='w', padx=5, pady=5)
    tk.Button(new_window, text="Save", command=lambda: close_addwindow(new_window, entry)).grid(row=2, column=0, sticky='w', padx=5, pady=5)

def close_addwindow(new_window,entry):
    inventory.add_item(entry.get())
    cleanWindow()
    updateitem.UpdateStatus()
    showExistingItem()
    new_window.destroy()


# Delete item in the form
def open_deletewindow():
    # Creat a new window
    new_window = tk.Toplevel(root)
    new_window.title("Delete Ingredient")
    
    # Creat element in the new window
    tk.Label(new_window, text="Item ID you want to delete: ")\
        .grid(sticky='w', row=0, column=0, pady=5, padx=5)
    entry = tk.Entry(new_window, width=40)
    entry.grid(row=0, column=1, sticky='w', padx=5, pady=5)
    tk.Button(new_window, text="Save", command=lambda: close_deletewindow(new_window, entry)).grid(row=2, column=0, sticky='w', padx=5, pady=5)

def close_deletewindow(new_window,entry):
    # delete 没有输入检测
    inventory.delete_item(entry.get())
    cleanWindow()
    updateitem.UpdateStatus()
    showExistingItem()
    new_window.destroy()


# Search Item in the window
def open_searchwindow():
    # 创建一个新的顶级窗口
    new_window = tk.Toplevel(root)
    new_window.title("Search Ingredient")
    
    # 在新窗口中添加小部件
    tk.Label(new_window, text="Item name you want to search: ")\
        .grid(sticky='w', row=0, column=0, pady=5, padx=5)
    entry = tk.Entry(new_window, width=20)
    entry.grid(row=0, column=1, sticky='w', padx=5, pady=5)
    tk.Button(new_window, text="Search", command=lambda: button_searchwindow(new_window, entry)).grid(row=0, column=2, sticky='w', padx=5, pady=5)

def button_searchwindow(new_window,entry):
    itemlist = show.ShowSpecifiedItem(entry.get())
    showItem(new_window, itemlist)


# Use Item in the window
def open_usewindow():
    # 创建一个新的顶级窗口
    new_window = tk.Toplevel(root)
    new_window.title("Use Ingredient")
    
    # 在新窗口中添加小部件
    tk.Label(new_window, text="Item ID you want to use: ")\
        .grid(sticky='w', row=0, column=0, pady=5, padx=5)
    entry = tk.Entry(new_window, width=40)
    entry.grid(row=0, column=1, sticky='w', padx=5, pady=5)
    tk.Button(new_window, text="Save", command=lambda: close_usewindow(new_window, entry)).grid(row=1, column=0, sticky='w', padx=5, pady=5)

def close_usewindow(new_window,entry):
    updateitem.Use(entry.get())
    cleanWindow()
    updateitem.UpdateStatus()
    showExistingItem()
    new_window.destroy()


# Show all item in window
def open_allingredwindow():
    # 创建一个新的顶级窗口
    new_window = tk.Toplevel(root)
    new_window.title("All Ingredient")

    # Set title in the window
    title_label = tk.Label(new_window, text="All Ingredients", font=("Arial", 20))
    title_label.grid(sticky='w', row=0, column=0, columnspan=2, pady=20, padx=5)

    # Set header of the form
    fields = ['Name', 'ID', 'Category', 'Quantity', 'Unit of Quantity', 'Purchase Date',
          'Expired Date', 'Status', 'Total Price', 'Store']
    for i in range(10):
        tk.Label(new_window, text=fields[i]).grid(row=1, column=i, sticky='w', padx=5, pady=5) 
    
    itemlist = show.ShowAsDict()
    showItem(new_window, itemlist)


# Generate Recipe
def open_recipewindow():
    # 创建一个新的顶级窗口
    new_window = tk.Toplevel(root)
    new_window.title("AI Recipe")

    # Set title in the window
    title_label = tk.Label(new_window, text=recipe.get_recipe(), font=("Arial", 15), anchor='w', justify='left')
    title_label.grid(sticky='w', row=0, column=0, pady=20, padx=5)

# Generate Statistics Report in the window
def open_reportwindow():
    # 创建一个新的顶级窗口
    new_window = tk.Toplevel(root)
    new_window.title("Statistic Report")
    
    # 在新窗口中添加小部件
    tk.Label(new_window, text="Select the chart you want to generate")\
        .grid(sticky='w', row=0, column=0, pady=5, padx=5)
    tk.Button(new_window, text="Spending by Store", command=lambda: button_spbystore()).grid(row=1, column=0, sticky='w', padx=5, pady=5)
    tk.Button(new_window, text="Spending by Month", command=lambda: button_spbymonth()).grid(row=2, column=0, sticky='w', padx=5, pady=5)

def button_spbystore():
    visualization.SpendingByStoreChart()

def button_spbymonth():
    visualization.SpendingByMonthChart()


# 在主窗口中添加按钮
tk.Button(root, text="Add Item", command=open_addwindow).grid(row=0, column=9, sticky='w', padx=10, pady=10)
tk.Button(root, text="Delete Item", command=open_deletewindow).grid(row=0, column=8, sticky='w', padx=10, pady=10)
tk.Button(root, text="Search Item", command=open_searchwindow).grid(row=0, column=7, sticky='w', padx=10, pady=10)
tk.Button(root, text="Use Item", command=open_usewindow).grid(row=0, column=6, sticky='w', padx=10, pady=10)
tk.Button(root, text="All Ingredient", command=open_allingredwindow).grid(row=0, column=5, sticky='w', padx=10, pady=10)
tk.Button(root, text="Generate Recipe", command=open_recipewindow).grid(row=0, column=4, sticky='w', padx=10, pady=10)
tk.Button(root, text="Statistics Report", command=open_reportwindow).grid(row=0, column=3, sticky='w', padx=10, pady=10)


# 启动主循环
root.mainloop()
