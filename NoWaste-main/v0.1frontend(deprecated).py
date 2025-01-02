import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, Toplevel
#import sqlite3
from datetime import datetime, timedelta
import datetime
import csv
import os
import pandas as pd
import random
from updateitem import UpdateStatus
from inventory import delete_item
from visualization import SpendingByStoreChart, SpendingByMonthChart
from recipe import get_recipe
from inventory import add_item
from show import ShowSpecifiedItem, ShowValidAsDict

# /opt/anaconda3/bin/python /Users/kirassya/FridgeInventorySystem/frontend.py
# create the main window
def create_window():
    window = tk.Tk()
    window.title("Fridge Inventory System") #window title
    window.geometry("550x400") #window size
    window.configure(bg='#ccffcc') #window color
    return window

#create style
style = ttk.Style()
style.configure("TCombobox", fieldbackground="#ffffcc", background="#ffffcc")

#add ingredient from input
def add_ingredient_input(window):
    #food name
    tk.Label(window, text="Name", font=("Helvetica",12, "bold"), 
             bg="#ffffcc", anchor="w").grid(row=0, column=0, sticky="w")
    name_entry = tk.Entry(window, justify="center", 
                          font=("Helvetica",12), bg="#ffffcc", width=15)
    name_entry.grid(row=0, column=1)

    #food category(OptionMenu to scroll)
    tk.Label(window, text="Category", font=("Helvetica",12, "bold"),
             bg="#ffffcc", anchor="w").grid(row=1, column=0, sticky="w")
    category_options = ["Vegetable", "Fruit", "Meat", "Seafood","Dairy", "Beverage", "Other"]
    category_var = tk.StringVar()
    category_var.set(category_options[0])    #set default value
    category_menu = tk.OptionMenu(window, category_var, *category_options)
    category_menu.config(font=("Helvetica",12), bg="#ffffcc", width=15)
    category_menu.grid(row=1, column=1)
    category_combobox = ttk.Combobox(window, values=category_options, 
                                     font=("Helvetica",12), style="TCombobox",
                                     width=15)
    category_combobox.grid(row=1, column=1, sticky="ew")

    #bind category to expiration
    def show_expiration_date(event):
    #add print to check the selected category
        print("Category selected:", category_combobox.get())

    category_combobox.bind("<<ComboboxSelected>>", show_expiration_date)



    #food quantity
    tk.Label(window, text="Quantity", font=("Helvetica",12, "bold"), 
             bg="#ffffcc", anchor="w").grid(row=2, column=0, sticky="w")
    quantity_entry = tk.Entry(window, validate="key", justify="center", 
                          font=("Helvetica",12), bg="#ffffcc", width=15)
    quantity_entry.grid(row=2, column=1)

    #unit of quantity
    unit_combobox = ttk.Combobox(window, values=["pounds", "oz", "ml", "bunch", "lb",
                                                  "g", "count"], state="normal")
    unit_combobox.grid(row=2, column=2)
    unit_combobox.set('pounds') #default unit

    #allow manual input and make sure the same unit
    def validate_unit(event):
        unit = unit_combobox.get()
        if unit not in ["pounds", "oz", "ml", "bunch", "lb", "g"]:
            unit_combobox.set('pounds') #back to default
        messagebox.showwarning("Invalid Unit", "Please enter a valid unit from the list or select one")
    
    unit_combobox.bind('<FocusOut>', validate_unit)


    #purchase date
    purchase_frame = tk.Frame(window, bg="#ffffcc")
    purchase_frame.grid(row=3, column=0, sticky="w")
    tk.Label(purchase_frame, text="Purchase Date", font=("Helvetica",12, "bold"), 
             bg="#ffffcc", anchor="w").grid(row=0, column=0, sticky="w")
    purchase_entry_var = tk.StringVar()
    purchase_entry = tk.Entry(window, textvariable=purchase_entry_var, justify="center", 
                          font=("Helvetica",12), bg="#ffffcc", width=15)
    purchase_entry.grid(row=3, column=1)


    #expiration date
    expiration_frame = tk.Frame(window, bg="#ffffcc")
    expiration_frame.grid(row=4, column=0, sticky="w")
    tk.Label(expiration_frame, text="Expiration Date", font=("Helvetica",12, "bold"), 
             bg="#ffffcc", anchor="w").grid(row=0, column=0, sticky="w")
    expiration_entry_var = tk.StringVar()
    expiration_entry = tk.Entry(window, textvariable=expiration_entry_var, justify="center", 
                          font=("Helvetica",12), bg="#ffffcc", width=15)
    expiration_entry.grid(row=4, column=1)

    #add placeholder text for purchase and expiration date
    placeholder_text = "(YYYY-MM-DD)"

    def add_placeholder(entry, entry_var, placeholder):
        entry.insert(0, placeholder)
        entry.config(fg='lightgrey')

        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg='black')

        def on_focus_out(event):
            if entry.get() == "":
                entry.insert(0, placeholder)
                entry.config(fg='lightgrey')

        def validate_date_format(*args):
            value = entry_var.get()
            if entry.get() != placeholder:
                if not validate_date(value):
                    entry.config(fg='red')
                else:
                    entry.config(fg='black')

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        entry_var.trace_add("write", validate_date_format)

    def validate_date(date_text):
        try:
            if date_text != placeholder_text:
                datetime.datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False


    add_placeholder(purchase_entry, purchase_entry_var, placeholder_text)
    add_placeholder(expiration_entry, expiration_entry_var, placeholder_text)

    #expiration date suggestion
#    expiration_label = tk.Label(window, text="Expiration suggestion will appear here.", 
#                                font=("Helvetica",10), fg="darkgrey", bg="#ccffcc")
#    expiration_label.grid(row=5, column=1)

    #show automatically expiration date based on category & purchase date
    def show_expiration_date(event=None):
        category = category_combobox.get()
        purchase = purchase_entry.get()

        try:
            purchase_obj = datetime.strptime(purchase, '%Y-%m-%d')
        except ValueError:
            expiration_entry.delete(0, tk.END)
            return
        
        #set expiration date of category
        #use dictionary to store expiration date
        expiration = {
            "Meat": 7,
            "Vegetable": 5,
            "Fruit": 5,
            "Dairy": 14,
            "Beverage": 30,
            "Seafood": 2,
            "Other": 14
        }
        expiration_obj = purchase_obj + timedelta(days=expiration)
        expiration_entry.delete(0,tk.END)
        expiration_entry.insert(0,expiration_obj.strftime('%Y-%m-%d'))

        #update expiration suggestion
 #       expiration_label.config(text=f"Suggested expiration: {expiration} days from purchase.")

    #bind category to expiration
    category_combobox.bind("<<ComboboxSelected>>", show_expiration_date)

    #grocery store and repurchase option
    tk.Label(window, text="Store", font=("Helvetica",12, "bold"), 
             bg="#ffffcc", anchor="w").grid(row=6, column=0, sticky="w")
    store_entry = tk.Entry(window, justify="center", 
                          font=("Helvetica",12), bg="#ffffcc", width=15)
    store_entry.grid(row=6, column=1)

    repurchase_var = tk.BooleanVar()
    repurchase_check = tk.Checkbutton(window, text="Repurchase", 
                                      font=("Helvetica",12, "bold"), 
                                      bg="#ffffcc", variable=repurchase_var)
    repurchase_check.grid(row=6, column=2)
   

    #price
    tk.Label(window, text="Total Price", font=("Helvetica",12, "bold"), 
             bg="#ffffcc", anchor="w").grid(row=7, column=0, sticky="w")
    total_price_entry = tk.Entry(window, justify="center", 
                          font=("Helvetica",12), bg="#ffffcc", width=15)
    total_price_entry.grid(row=7, column=1)

    #show unit price based on total price and quantity
    tk.Label(window, text="Unit Price", font=("Helvetica",12, "bold"), 
             bg="#ffffcc", anchor="w").grid(row=8, column=0, sticky="w")
    unit_price_entry = tk.Entry(window, justify="center", 
                          font=("Helvetica",12), bg="#ffffcc", width=15)
    unit_price_entry.grid(row=8, column=1)

#    unit_label = tk.Label(window, text=f"$/{unit_combobox.get()}", font=("Helvetica",12, "bold"),
#            bg="#ffffcc", anchor="w").grid(row=8, column=2, sticky="w")
    
    #unit price unit label  update
    def update_unit_label(event):
        global unit_label
        selected_unit = unit_combobox.get() 
        print(f"Unit changed to: {selected_unit}")
        unit_label.config(text=f"$/{selected_unit}")

    #bind unit to unit price
    unit_combobox.bind("<<ComboboxSelected>>", update_unit_label)

     #price calculation
    def calculate_price(event=None):
        try:
            quantity = float(quantity_entry.get())
            total_price = total_price_entry.get()
            unit_price = unit_price_entry.get()
            if total_price and not unit_price:
                unit_price_entry.delete(0,tk.END)
                unit_price_entry.insert(0, str(round(float(total_price) / quantity, 2)))
            elif unit_price and not total_price:
                total_price_entry.delete(0,tk.END)
                total_price_entry.insert(0, str(round(float(unit_price) * quantity, 2)))
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter numeric values for price/quantity.")
    
    total_price_entry.bind("<FocusOut>", calculate_price)
    unit_price_entry.bind("<FocusOut>", calculate_price)

  

    #create ID
    tk.Label(window, text="ID", font=("Helvetica", 12, "bold"),
                bg="#ffffcc", anchor="w").grid(row=11, column=0, sticky="w")
    #enter ID
    id_var = tk.StringVar()
    id_entry = tk.Entry(window, textvariable=id_var, justify="center",
                        font=("Helvetica", 12), bg="#ffffcc", width=15)
    id_entry.grid(row=11, column=1)



    #status 
    tk.Label(window, text="Status", font=("Helvetica", 12, "bold"), 
         bg="#ffffcc", anchor="w").grid(row=12, column=0, sticky="w")
    status_combobox = ttk.Combobox(window, values=["Normal", "Expiring soon", 
                                                   "Expired", "Used", "Invalid date"], state="normal")
    status_combobox.grid(row=12, column=1)
    status_combobox.set('Normal') #default status
    
   

    #create save button
    save_button = tk.Button(window, text="Save Ingredient", bg="#ccffcc", 
                            font=("Helvetica", 12, "bold"), command=add_item)
    save_button.grid(row=30, column=1, columnspan=2)

    

        #save ingredient button
        #Name,ID,Category,Quantity,Unit of Quantity,Purchase Date,Expired Date,Status,Total Price,Store

    def save_ingredient():
        name = name_entry.get()
        category = category_combobox.get()
        quantity = quantity_entry.get()
        unit = unit_combobox.get()
        purchase = purchase_entry.get()
        expiration = expiration_entry.get()
        store = store_entry.get()
        repurchase = repurchase_var.get()
        total_price = total_price_entry.get()
        unit_price = unit_price_entry.get()
        ID = id_var.get()
        status = status_combobox.get()

        a = name+","+ID+","+category+","+quantity+","+unit+","+purchase+","+expiration+","+status+","+total_price+","+store
        add_item(a)


        if not quantity.isdigit():
            messagebox.showwarning("Input Error", "Please enter a valid number for quantity.")
            return

        if name and category and quantity and purchase and expiration:
            #save to database
            save_to_db(name, category, purchase, expiration, quantity, unit)
            messagebox.showinfo("Success", "Ingredient added successfully!")
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")


    #create view button
    view_button = tk.Button(window, text="View Inventory", bg="#ccffcc", 
                        font=("Helvetica", 12, "bold"), command=None)
    view_button.grid(row=31, column=1, columnspan=2)

    import inventory_window  #假的按钮


    def show_price_comparison(window):
        price_comparison = compare_prices()
        comparison_text = "\n".join(
            f"{item}: " + ", ".join([f"{store} (${price})" for store, price in details])
            for item, details in price_comparison.items()
        )
        messagebox.showinfo("Prcie Comparison", comparison_text)

        


if __name__ == "__main__":
    window = create_window()
    add_ingredient_input(window)
    window.mainloop()
