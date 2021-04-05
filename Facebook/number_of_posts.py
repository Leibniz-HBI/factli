import requests
import json
import time
import pandas as pd
from datetime import date

def ct_get_posts(list_id, count, access_token):
    
    all_posts = pd.DataFrame(columns=[''])
    start_date = '2021-04-03'
    end_date = '2021-04-04'
    query = 'https://api.crowdtangle.com/' + '/posts?token=' + str(access_token) + '&listIds=' + str(list_id)  + '&startDate=' + start_date + '&endDate=' + end_date + '&count=' + str(count) 
    
    

    while(query != ''):
        try:
    
            print ("Fetching:\t", query)
    
            r = requests.get(query)
            json_response = r.json()
            #print(json_response)
            next_Page_url = json_response['result']['pagination']['nextPage']
            
        
        
            normalized_json = pd.json_normalize(json_response['result']['posts'])
            #print(normalized_json)
            data_frame = pd.DataFrame.from_dict(normalized_json, orient = "columns")
            
            #data_frame['id'] = data_frame['id'].astype(str)
            
            pd.set_option('display.max_columns', None)  
            pd.set_option('display.max_rows', None)  
            pd.set_option('display.max_colwidth', None) 
            #print(data_frame)
            posts_count = len(data_frame)
            #print(accounts_count)
            status = r.status_code

            if (status == 429):

                print("API rate limit hit, sleeping...")
                time.sleep(60)

                continue
            

            elif(status == 200 and posts_count != 0):

                posts = data_frame
                all_posts = all_posts.append(posts)
                query = next_Page_url
                

            
            else:
                print("Other Status: ", status)
                query = ''
            
        except KeyError:
            print("No next page")
            break
    
    return(all_posts)



if __name__ == "__main__":
    
    
    list_id = 1484485
    access_token = "xVwti7hHe2SYdVSGyDJ42TCSms7XvmStrWVIy41b"
    count = 100
    posts_df = ct_get_posts(list_id, count, access_token)
    posts_count = len(posts_df)
    print("Number of Posts for the time frame =", posts_count)
    file_name = str(date.today()) + ".csv" 
    posts_df.to_csv(file_name, encoding = 'utf-8')



    
    



 
 
   


