import pymongo
from bs4 import BeautifulSoup
import re
import logging
import csv

# Set up logging
logging.basicConfig(filename='task6_log.txt', level=logging.ERROR)

#connect with mongodb
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["Unigap_Project04"]
mongo_collection = mongo_db["Products_full"]

def extract_element_with_content(html_cotent):
    soup = BeautifulSoup(html_cotent, 'html.parser')

    #find elements that have the words "thanh phan"

    regex = re.compile(r"thành phần", re.IGNORECASE)
    elements_with_content = soup.find_all(string=regex)

    results = []

    #if elements have the words thanh phan, and if the legnth is only for the words "Thanh phan" or ends with ":", we will check the the next sibling
    if elements_with_content:
        print('Found')
        for element in elements_with_content:
            #print(element)
            #print(len(element))
            #print(element.strip().endswith(":"))

            element_text = element.strip()

            if len(element_text) <= 15 or element_text.endswith(":"):
                next_element= element.find_next()
                next_element_text = next_element.get_text().strip()
                #print(len(next_element_text))

                #if the next sibling is emtpy, take the next sibling
                if len(next_element_text) == 0:
                    #print("next next elments")
                    next_next_element = next_element.find_next()
                    elements_combined = element_text + " " + next_next_element.get_text().strip()
                    results.append(elements_combined)
                else:
                    #print('Next element')
                    #print(next_element)
                    elements_combined = element_text + " " + next_element.get_text().strip()
                    results.append(elements_combined)
            else:
                results.append(element_text)
    else:
        print("Not found")
    
    return results
   
def write_to_csv(product_id,content):
    with open('thanhphan.csv', 'a', newline='', encoding='utf-8' ) as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([product_id,content])


#read collections and documents from mongodb and only extract the needed fields
# read the data to SQL 
def mongo_to_csv(start_position): 

    i=0
    try:
   
        for mongo_document in mongo_collection.find({}).skip(start_position):
            i = i+1
            print("Check for position", i)
            #get short description and clean
            description_html = mongo_document.get("description", "")

            #if find the elements, return the content 
            # if find the elements, save the ID of the document
            csv_content = extract_element_with_content(description_html)
            
            #print("Results: ")
            #print(csv_content)

            if csv_content :
                id = mongo_document.get("id")
                write_to_csv(id,csv_content)
                print("load to csv")
                #write to csv file
        
    except Exception as e:
        logging.error(f"Error : {e}, Skipped position: {i}")

mongo_to_csv(0)





