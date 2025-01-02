import csv # library for managing csv file

# print current form as dictionary
# return inventory data as a list, each row is a dictionary.
def ShowAsDict():
        with open('database.csv', 'r') as file:
                reader = csv.DictReader(file) 
                '''
                for row in reader:
                        print(row)
                '''
                return list(reader)


# print current form as dictionary, but not including used item.
# return inventory data as a list, each row is a dictionary.
def ShowValidAsDict():
        with open('database.csv', 'r') as file:
                new_list = []
                reader = csv.DictReader(file) # reader is a list of dictionary
                for row in reader: # row is a dictionary
                        if (row["Status"] == 'Used'):
                                pass
                        else:
                                new_list.append(row) # only include not used item in new list
                '''
                #print new list except used item
                for row in new_list:
                        print(row)
                '''
                return new_list


# print current form as string
def ShowAsString():
        with open('database.csv', 'r') as file:
                reader = csv.reader(file); #reader is a list, each row is an string item in the list.
                for row in reader:
                                print(row)


# return specified ingridient in inventory.
# This function can be used to compare prices of the same ingridient in different stroe and time.
# 待删除：比价函数，输入名字，输出一个字典的列表
def ShowSpecifiedItem(name):
    with open('database.csv', 'r') as file:
        new_list = []
        reader = csv.DictReader(file) # reader is a list of dictionary
        for row in reader: # row is a dictionary
                if (row["Name"] == name):
                        new_list.append(row) # only include specified item in new list.
        
        #print new list except used item
        for row in new_list:
                print(row)
        
        return new_list

