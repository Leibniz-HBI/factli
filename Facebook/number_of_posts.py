import requests
import json
import time
import pandas as pd
from datetime import date
import logging

logging.basicConfig(filename='posts.log', level=logging.DEBUG)

def ct_get_posts(list_id, count, access_token):
    
    all_posts = pd.DataFrame(columns=[''])
    start_date = '2021-04-02'
    end_date = '2021-04-03'
    query = 'https://api.crowdtangle.com/' + '/posts?token=' + str(access_token) + '&listIds=' + str(list_id)  + '&startDate=' + start_date + '&endDate=' + end_date + '&count=' + str(count) 
    
    

    while(query != ''):
        try:
    
            print ("Fetching:\t", query)
    
            r = requests.get(query)

            json_response = r.json()
            if (json_response['status'] == 429):

                print("API rate limit hit, sleeping...")
                time.sleep(60)

                continue
            logging.debug(json_response)
            next_Page_url = json_response['result']['pagination']['nextPage']
            
        
        
            normalized_json = pd.json_normalize(json_response['result']['posts'])
            logging.debug(normalized_json)
            data_frame = pd.DataFrame.from_dict(normalized_json, orient = "columns").astype(str)
            
            #data_frame['id'] = data_frame['id'].astype(str)
            
            pd.set_option('display.max_columns', None)  
            pd.set_option('display.max_rows', None)  
            pd.set_option('display.max_colwidth', None) 

            logging.debug(data_frame)

            posts_count = len(data_frame)
            logging.debug(posts_count)

            status = r.status_code
            logging.debug(status)
            
            if(status == 200 and posts_count != 0):

                posts = data_frame
                all_posts = all_posts.append(posts)
                query = next_Page_url
                

            
            else:
                print("Other Status: ", status)
                query = ''
            
        except KeyError:
            print("No next page")
            logging.debug(json_response)
            break
    
    return(all_posts)



if __name__ == "__main__":
    
    
    list_id = 1484485
    access_token = "xVwti7hHe2SYdVSGyDJ42TCSms7XvmStrWVIy41b"
    count = 100
    posts_df = ct_get_posts(list_id, count, access_token)
    
    df = posts_df.groupby(['account.id']).count()[['id']]
    
    logging.debug(df)
    df_new = df.rename(columns = {'account.id': 'User IDs', 'id': 'Number of Posts'})
    file_name = str(date.today()) + ".csv" 
    df_new.to_csv(file_name, encoding = 'utf-8')



    
    



 
 
   


