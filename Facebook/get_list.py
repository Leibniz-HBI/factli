import requests
import json
import time
import pandas as pd
from datetime import date

def ct_get_lists(list_id, count, access_token):
    
    all_accounts = pd.DataFrame(columns=[''])
    query = 'https://api.crowdtangle.com/lists/' + str(list_id) + '/accounts?token=' + str(access_token) + '&count=' + str(count) 
    
    

    while(query != ''):
        try:
    
            print ("Fetching:\t", query)
    
            r = requests.get(query)
            json_response = r.json()
            #print(json_response)
            next_Page_url = json_response['result']['pagination']['nextPage']
            
        
        
            normalized_json = pd.json_normalize(json_response['result']['accounts'])
            #print(normalized_json)
            data_frame = pd.DataFrame.from_dict(normalized_json, orient = "columns")
            
        
            pd.set_option('display.max_columns', None)  
            pd.set_option('display.max_rows', None)  
            pd.set_option('display.max_colwidth', None) 
            #print (accounts)
            accounts_count = len(data_frame)
            #print(accounts_count)
            status = r.status_code

            if (status == 429):

                print("API rate limit hit, sleeping...")
                time.sleep(60)

                continue
            

            elif(status == 200 and accounts_count != 0):

                accounts = data_frame
                all_accounts = all_accounts.append(accounts)
                query = next_Page_url
                

            
            else:
                print("Other Status: ", status)
                query = ''
            
        except KeyError:
            print("No next page")
            break
    
    return(all_accounts)



if __name__ == "__main__":
    
    
    list_id = 1484485
    access_token = "xVwti7hHe2SYdVSGyDJ42TCSms7XvmStrWVIy41b"
    count = 1000
    accounts_df = ct_get_lists(list_id, count, access_token)
    #print(accounts_df)
    file_name = str(date.today()) + ".csv" 
    accounts_df.to_csv(file_name, encoding = 'utf-8')



    
    



 
 
   


