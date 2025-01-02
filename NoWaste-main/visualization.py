# This file inlcude two diagrams.
# 1. Chart of comparison of spending by store.
# 2. Chart of monthly expenditure trends.

import show
import matplotlib.pyplot as plt
from datetime import datetime

def SpendingByStoreChart():
    inventory = show.ShowAsDict() # list of dict of all inventory item
    storelist = dict()

    # To get a dictionary,like {'Walmart': 99.0, "Costco": 66.6}
    for item in inventory: #every item is a list
        if item['Store'] in storelist:
            storelist[item['Store']] += float(item['Total Price']) # Price in storelist is a float.
        else:
            storelist[item['Store']] = float(item['Total Price'])

    # To convert this dictionary to a chart.
    # get spending and store name seperately
    stores = list(storelist.keys())
    spendings = list(storelist.values())

    # draw bar chart
    plt.figure(figsize=(8, 5))  # 设置画布大小
    plt.bar(stores, spendings, color='skyblue')
    plt.title('Spending by Store')  # 设置标题
    plt.xlabel('Stores')  # 设置X轴标签
    plt.ylabel('Spending ($)')  # 设置Y轴标签
    plt.tight_layout()  # 自动调整布局以防止重叠
    # plt.show()
    plt.savefig('bar_chart.png')  # 保存为文件
    plt.close()

    # draw pie chart
    plt.figure(figsize=(7, 7))  # 设置画布大小
    plt.pie(spendings, labels=stores, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    plt.title('Spending Distribution by Store')  # 设置标题
    # plt.show()
    plt.savefig('pie_chart.png')  # 保存为文件
    plt.close()

def SpendingByMonthChart():
    inventory = show.ShowAsDict() # list of dict of all inventory item
    spendingbymonth = dict()

    for item in inventory: #every item is a dict

        # convert time string in item to time object
        date_obj = datetime.strptime(item['Purchase Date'], "%Y-%m-%d")

        # extract month from date object
        month = date_obj.month # month is an int, ranging from 1 to 12.

        # spendingbymonth like: {1:13.99, 2:100.00, 4:500.50}. The front represent month(int), the back represent spending(float).
        if month in spendingbymonth:
            spendingbymonth[month] += float(item['Total Price'])
        else:
            spendingbymonth[month] = float(item["Total Price"])

    # To convert this dictionary to a chart.
    # 将字典的键值按月份排序
    months = sorted(spendingbymonth.keys())  # ordered month
    spendings = [spendingbymonth[month] for month in months]  # adjust spending order

    # Draw line chart
    plt.figure(figsize=(10, 6))  # 设置图表大小
    plt.plot(months, spendings, marker='o', color='b', linestyle='-', label='Monthly Spending')
    # 添加标题和坐标轴标签
    plt.title('Monthly Spending Overview', fontsize=16)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Spending ($)', fontsize=12)
    # 设置x轴的刻度为月份
    plt.xticks(range(1, 13))  # 设置 x 轴显示 1 到 12 月份
    # 显示网格和图例
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    # 显示图形
    plt.tight_layout()
    # plt.show() #待删除
    plt.savefig('spendingbymonth.png')  # 保存为文件
    plt.close()