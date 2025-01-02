import pandas # process csv data.
from datetime import datetime # process 'date' data type.
import csv # library for managing csv file


# 1. Compare current date to expired date with TIME library.
# 2. Update status data with PANDAS library.
# 待删除：每次拉数据库数据的时候都要调一遍更新状态函数
def UpdateStatus():
    # Read file into pandas' special data type.
    file = pandas.read_csv('database.csv')

    # Convert expired date column to datetime type in pandas
    file['Expired Date'] = pandas.to_datetime(file['Expired Date'], errors='coerce')

    # Get current date
    current_date = datetime.now().date()
    # v0.2: current_date = pandas.Timestamp.now().date()

    # Iterate over each row and compare current date to expired date
    for index, row in file.iterrows():
        # Check if the expired date is valid
        if pandas.isnull(row['Expired Date']):
            # If expired date is invalid, set status as 'Invalid date'
            file.loc[index, 'Status'] = 'Invalid date'
        elif file.loc[index, 'Status'] == 'Used':
            pass
        else:
            expired_date = row['Expired Date'].date()
            difference = (expired_date - current_date).days

            # Update status based on the difference
            if difference >= 3:
                file.loc[index, 'Status'] = 'Normal'
            elif 0 <= difference < 3:
                file.loc[index, 'Status'] = 'Expiring soon'
            else:
                file.loc[index, 'Status'] = 'Expired'

    # Save the updated data to original file
    file.to_csv('database.csv', index=False)


# input item id, change its status to 'used'. 'id' is a string.
def Use(id):  
    reader = list()
    with open('database.csv', 'r') as file:
        reader = list(csv.DictReader(file)) # reader is a list of dictionary
        for row in reader: # row is a dictionary
            if (row["ID"] == id):
                row["Status"] = 'Used'
    
    with open('database.csv', 'w', newline='') as file:
        fieldnames = ['Name', 'ID', 'Category', 'Quantity', 'Unit of Quantity', 'Purchase Date',
                   'Expired Date', 'Status', 'Total Price', 'Store']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(reader)


'''
import shutil # copy file
# copy a backup in case of error
source_path = 'database.csv'
backup_path = 'database_backup.csv'
shutil.copy2(source_path, backup_path)
print(f'Backup of {source_path} created as {backup_path}')
'''
