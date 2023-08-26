from pymongo import MongoClient
import gridfs
import json 

#transform the json file 
def transform_file(file_path,output_file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    # Flatten the list of lists
    flattened_data = [item for sublist in data for item in sublist]

    #write the transform data to a new JSON file 
    with open(output_file_path, 'w') as json_file:
        json.dump(flattened_data, json_file, indent=2)

    print('Transformation completed')

#transform_file('data/crawl1-305','data/transformed_crawl1-305')
#transform_file('data/crawl306-1000','data/transformed_crawl306-1000')
#transform_file('data/crawl1001-1633','data/transformed_crawl1001-1633')
#transform_file('data/crawl1634-2311','data/transformed_crawl1634-2311')


#connect to mongodb
mongodb_uri = "mongodb://localhost:27017/"
client = MongoClient(mongodb_uri)
db = client["Unigap_Project04"]

#load data from JSON file 
def load_data_to_mongodb(collection,file_path) :
    with open(file_path,'r') as json_file:
        data = json.load(json_file)
    #choose the collection 
    collection = db[collection]

    for document in data:
        filter_criteria = {"id": document["id"]}
        update_data = {"$set": document}
        collection.update_one(filter_criteria, update_data, upsert = True)
    
    print("Import completed")

#load_data_to_mongodb('Categories','data/transformed_crawl1-305')
#load_data_to_mongodb('Categories','data/transformed_crawl306-1000')
#load_data_to_mongodb('Categories','data/crawl1000-2311')

