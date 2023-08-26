#Trích xuất các trường thông tin từ Mongodb và lưu vào MySQL
#connect to SQL 
#connect to MongoDB
#function: create table 
#function: read data to sql 
#function: mongo to sql: loop through the documents in mongodb and read each document into the SQL

import pymongo
import mysql.connector
from bs4 import BeautifulSoup
import decimal
import logging

# Set up logging
logging.basicConfig(filename='task3_log.txt', level=logging.ERROR)

#connect with mongodb
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["Unigap_Project04"]
mongo_collection = mongo_db["Products_full"]


#connect with SQL
mysql_connection = mysql.connector.connect(
    host = "127.0.0.1",
    port = "3306",
    user = "root",
    password = "unigapde",
    database = "project04"
)

mysql_cursor = mysql_connection.cursor()

def create_table(name):
    create_table_query = """
    CREATE TABLE {} (
        name VARCHAR(255),
        product_id INT,
        short_description TEXT,
        description TEXT,
        url VARCHAR(255),
        rating FLOAT,
        so_luong_ban INT,
        gia_san_pham DECIMAL(10, 2),
        category_id INT,
        day_ago_created INT
    )
    """.format(name)
    mysql_cursor.execute(create_table_query)
    mysql_connection.commit()

#create_table()

#function to read data to sql
def read_data_to_sql(data):
    try: 
        mysql_insert_query = "INSERT INTO product(name, product_id, short_description,description,url,rating,so_luong_ban,gia_san_pham,category_id,day_ago_created) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        mysql_insert_values = (data["name"],data["product_id"], data["short_description"], data["description"], data["url"], data["rating"], data["so_luong_ban"],
                            data["gia_san_pham"],data["category_id"],data["day_ago_created"])
        mysql_cursor.execute(mysql_insert_query,mysql_insert_values)
        mysql_connection.commit()
        print('load to sql')
    except Exception as e:
        logging.error(f"Error inserting data: {e}, Skipped: ID={data['product_id']}, Name={data['name']}")


#read collections and documents from mongodb and only extract the needed fields
# read the data to SQL 
def mongo_to_sql(start_position=0): 
    for mongo_document in mongo_collection.find({}).skip(start_position):
        #get short description and clean
        description_html = mongo_document.get("description", "")
        soup = BeautifulSoup(description_html, "html.parser")
        cleaned_description = soup.get_text()

        # Convert the price to a decimal and ensure it's within acceptable range
        gia_san_pham_value = decimal.Decimal(str(mongo_document.get("list_price")))

        #extract information from MongoDB document: 
        extracted_data = {
            "name": mongo_document.get("name"),
            "product_id": mongo_document.get("id"),
            "short_description": mongo_document.get("short_description")[:255],
            "description": cleaned_description,
            "url": mongo_document.get("short_url"),
            "rating": mongo_document.get("rating"),
            "so_luong_ban": mongo_document.get("quantity_sold", {}).get("value"),
            "gia_san_pham": gia_san_pham_value ,
            "category_id" : mongo_document.get("categories", {}).get("id"),
            "day_ago_created": mongo_document.get("day_ago_created")
        }
        #print(extracted_data)

        read_data_to_sql(extracted_data)

    # Close connections
    mysql_cursor.close()
    mysql_connection.close()
    mongo_client.close()


# run the function
#mongo_to_sql()
#error at the position 392753
#mongo_to_sql(start_position=392753)








