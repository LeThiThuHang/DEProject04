#Mỗi category (bao gồm cả sub-category) có bao nhiêu sản phẩm
#connect with monggodb
#function write_to_csv(): write results as category_id, category_name, product_count to the csv file
#function count_product_by_category: go to collection in mongodb, loop through the documents ,get the id and name, and count to the dictionary category_counts {}
#function write_info_to_csv(): run the count_product_by_category function and store it in the dictionary. Loop through each fields and values in the dictionary 
    ##and use function write_to_csv() to write to the output file 

import pymongo
import csv

#connect with mongodb
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["Unigap_Project04"]
mongo_collection = mongo_db["Products_full"]

#extract data from csv 
def write_to_csv(category_id, category_name, product_count):
    with open('task4a.csv', 'a', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Write the header row if the file is empty
        if csvfile.tell() == 0:
            csv_writer.writerow(["Category ID", "Category Name", "Product Count"])

        csv_writer.writerow([category_id, category_name, product_count])


def count_product_by_category():
    category_counts = {}

    for mongo_document in mongo_collection.find({}):

        categories_id = mongo_document.get("categories", {}).get("id")
        categories_name = mongo_document.get("categories", {}).get("name")
        print(categories_id)
        if categories_id:
            if categories_id not in category_counts:
                category_counts[categories_id] = {"count": 1, "name": categories_name}
            else:
                category_counts[categories_id]["count"] += 1
    return category_counts

def write_info_to_csv():
    category_counts = count_product_by_category()
    for category_id, info in category_counts.items():
        category_name = info['name']
        product_count = info['count']
        write_to_csv(category_id, category_name, product_count)

write_info_to_csv()