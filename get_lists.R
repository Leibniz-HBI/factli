setwd("~/git/pluragraph-ct")

require("jsonlite")
require("dplyr")

# MdB test: list_id <- "1483968"
list_id <- "1484485"
access_token <- "CHANGE_SECRET_TOKEN"

ct_get_lists <- function(list_id, token = "", count = 1000) {
  
  endpoint_link <- "https://api.crowdtangle.com/lists/"
  query_string <- paste0(endpoint_link, list_id, "/accounts?token=", token, "&count=", count)
  
  all_accounts <- NULL
  
  while (!is.null(query_string)) {
    
    cat("Fetching", query_string, "\n")
    response_json <- try(fromJSON(query_string), silent = TRUE)
    
    if (!class(response_json) == "try-error") {
      
      status <- response_json$status
      
      if (status == 429) {
        
        print("API rate limit hit, sleeping...")
        Sys.sleep(60)
        
        # try again
        next
        
      }
      
      accountscount <- nrow(response_json$result$accounts)
      
      if (status == 200 & !is.null(accountscount)) {
        
        accounts <- response_json$result$accounts
        accounts <- jsonlite::flatten(accounts)
        
        all_accounts <- rbind(all_accounts, accounts)
        
        query_string <- response_json$result$pagination$nextPage
        
      } else {
        
        print("Other status", status)
        
        query_string <- NULL
        
      }
      
    } else {
      
      print("Error")
      print(response_json)
      
      query_string <- NULL
      
    }
    
  }
  
  return(all_accounts)
  
}


# run main

accounts_df <- ct_get_lists(list_id, access_token)
write.csv2(accounts_df, file = paste0(Sys.Date(),".csv"), fileEncoding = "UTF-8")
