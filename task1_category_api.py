import requests
import pandas as pd 
import json
import logging 
import time 



file_path = "data\categories_api.csv"
#create pandas dataframe from the categories csv file
df = pd.read_csv(file_path)


headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}

# Configure logging
logging.basicConfig(filename='crawler.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#function to get product_id from each category CAN Y
def get_product_id(category):
    product_list = []
    i = 1
    category_url = "https://tiki.vn/api/v2/products?limit=48&include=advertisement&aggregations=1&category={}&page={}&urlKey=laptop"

    while True:

        try: 
            response = requests.get(category_url.format(category,i), headers=headers)
            logging.info(f'Crawl page number {i} for the {category} successfully')


            #to avoid the JSONdecode errors
            if response.text.strip():
                products = response.json()
                #print(products)
                product_length = len(products['data'])
                logging.info(product_length)
                                        
                if 'data' not in products or len(products.get('data', [])) == 0:
                    break

            else:
                 logging.info(f'Response for URL {category_url.format(category, i)} is empty.')

        except requests.exceptions.RequestException as e:
            logging.info(f'Crawl page number {i} for the {category} NOT successfully, Error: {e}')
        
        


        #if (response.status_code != 200):
            #print('Error', response.text)
            #break
        
        #break it when the products has no data
       


        for product in products['data']:
            product_list.append(product)

        i += 1
    
    #print(product_list)
    
    return product_list

product = get_product_id(24382)

#main crawling function 
def crawl_categories(start,end,filename):
    logging.info('this is a test')
    result_data = []
    products_processed = 0

    #take the categories id from the dataframe
    categories_id = df['LEAF_CAT_ID'][start:end].str.replace('c','')
    categories_number = len(categories_id)
    print('There are :', categories_number, ' categories')

    for category in categories_id:
        print('crawl the category: ', category)
        result = get_product_id(category)
        #print(result)
        result_data.append(result)
        products_processed += 1

        #get the product information to json file
        if products_processed % 10  == 0:

            # Write the current result_data to the JSON file
            with open(filename, 'w') as json_file:
                json.dump(result_data, json_file, indent=2)

            #result_data = []

        time.sleep(1)

#length is 2311
#crawl_categories(0,305,'') - CRAWL 26569 ID - file crawl1-305
#crawl_categories(306,1000,'') - CRAWL 512634 ID - file crawl306-1000
#crawl_categories(1001,1634,'') #873845 , stop at 1635, eror of id 11336, collect 391982 
#crawl_categories(1633,2311,'') #3:17 