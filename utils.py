import mysql.connector
import pandas as pd
from datetime import datetime

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='product',
    auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor()


def insert_data(filepath):
    try:

        df = pd.read_csv(filepath)

        for index, row in df.iterrows():
            sql = "insert into product(store_id,SKU,product_name,price,order_date) VALUES (%s,%s,%s,%s,STR_TO_DATE(%s,'%d-%b-%Y'))"
            value = (row['Store ID'], row['SKU'], row['Product Name'], row['Price'], row['Order Date'])
            mycursor.execute(sql, value)
            mydb.commit()
            print(index, row['Store ID'], row['SKU'], row['Product Name'], row['Price'], row['Order Date'])
    except Exception:
        print("Error while inserting records")


def get_data(col_name=None, val=None):
    try:
        print(col_name, val)
        if col_name in ("store_id", "sku"):
            sql = f"select * from product where {col_name}={val}"

        elif col_name == "price":
            sql = f"select * from product where cast({col_name} as decimal)=cast({val}as decimal)"

        elif col_name == "product_name":
            sql = f"select * from product where {col_name}='{val}'"

        else:
            sql = "select * from product"

        print(sql)
        mycursor.execute(sql)

        data = []
        for x in mycursor:
            print(x)
            row = [x[0], x[1], x[2], x[3], x[4].strftime('%d-%b-%Y')]

            print(row)
            data.append(row)

        return data

    except Exception:
        print(f"Error while fetching {val} result")


def update_record(store_id, sku, prod_desc, price, order_date):
    try:

        sql = f"update product set SKU={sku}, product_name='{prod_desc}', price={price}, order_date=DATE(STR_TO_DATE('{order_date}', '%d-%b-%Y')) where store_id={store_id}"
        print(sql)
        mycursor.execute(sql)
        mydb.commit()
        data = {
            "Status": "Success",
            "Message": "Record updated succesfully"
        }
        return data

    except Exception:

        data = {
            "Status": "Error",
            "Message": f"Error while updating record for store_id {store_id}"
        }
        return data

