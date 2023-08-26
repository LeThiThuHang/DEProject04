#Tạo biểu đồ thống kê xuất xứ của các sản phẩm. Ví dụ từ biểu đồ có thể biết: Có bao nhiêu sản phẩm xuất xứ từ Trung Quốc. Từ đó so sánh tỉ lệ xuất xứ của các sản phẩm
#connect with mongodb
#function write_to_csv(): write neccessary information to the file
# function product_by_origin(): find the pattern in the mongo documents, note that need to find in the "specification" fields, then going down for attributes to find the regex pattern
    ##if find the pattern, get the value and the product_id, write to the file csv
#function to clean the duplicates based on product_id from the output file 

import pymongo
import csv
import re
import pandas as pd

#connect with mongodb
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["Unigap_Project04"]
mongo_collection = mongo_db["Products_full"]

def write_to_csv(product_id, attribute_name, origin):
    with open('task4b.csv', 'a', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Write the header row if the file is empty
        if csvfile.tell() == 0:
            csv_writer.writerow(["Product ID", "Origin", "Value"])

        csv_writer.writerow([product_id, attribute_name, origin])

def product_by_origin():
    regex_pattern = re.compile(r"xuất\s*xứ", re.IGNORECASE)
    for mongo_document in mongo_collection.find({}):
        specifications = mongo_document.get("specifications", [])
        for spec in specifications:
            for attributes in spec.get("attributes",[]):
                attribute_name = attributes.get("name","")
                if regex_pattern.search(attribute_name):
                    product_id = mongo_document.get("id")
                    print(attribute_name)

                    origin = attributes.get("value")
                    write_to_csv(product_id, attribute_name, origin)
       
def remove_duplicate(file_name,clean_file_name):
    df = pd.read_csv(file_name)
    df_no_duplicates = df.drop_duplicates(subset="Product ID", keep="first")

    #save the cleaned data to a new csv file
    df_no_duplicates.to_csv(clean_file_name)

#product_by_origin()
remove_duplicate('task4b.csv','cleaned_task4b.csv')