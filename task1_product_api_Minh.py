import threading
import requests 
import json
import logging 
import time 
from pymongo import MongoClient

# Configure the logging settings
logging.basicConfig(
    filename='product.log',  # Specify the name of the log file
    level=logging.DEBUG,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Example log messages
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')


def load_data_to_mongodb(collection,data) :
    #connect to mongodb
    mongodb_uri = "mongodb://localhost:27017/"
    client = MongoClient(mongodb_uri)
    db = client["Unigap_Project04"]
    collection = db[collection]

    filter_condition = {"id": data["id"]}
    update_operation = {"$set" : data}
    result = collection.update_one(filter_condition, update_operation, upsert = True )

    # Print the number of documents matched and modified
    print("import to mongo")

    #close connection
    client.close()

def get_product_api(start,end):
    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}
    api = "https://tiki.vn/api/v2/products/{}"

    # Read the text file and load its content as a Python object
    data = []
    try:
        with open('data/product_id_1.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                data.append(line.strip())
                
    except FileNotFoundError:
            print(f"File not found at")
    except Exception as e:
            print(f"An error occurred: {e}")


    for id in data[start:end]:
        api = "https://tiki.vn/api/v2/products/{}"
        try: 
            response = requests.get(api.format(id),headers= headers)
            print('get: ', api.format(id))
            product_data = response.json()
            load_data_to_mongodb('Products_Minh',product_data)
            logging.info(f'{api.format(id)} run successfully')          
        except:
            logging.error('Error: ',response.status_code)
        
        time.sleep(1)
        
#find_length('data/transformed_crawl1-305') #26569

thread_1 = threading.Thread(target=get_product_api, args=(1,75000))
thread_2 = threading.Thread(target=get_product_api, args=(75000,150000))


 # Start Multi thread
thread_1.start()
thread_2.start()


# Wait for both threads to finish
thread_1.join()
thread_2.join()


print("All threads have finished.")



