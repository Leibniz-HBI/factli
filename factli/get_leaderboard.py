import requests
import time
import pandas as pd
from datetime import date
from loguru import logger
import click


@click.command()
@click.option('--list_id', help='Saved List ID')
@click.option('--count', default=100, help='Number of accounts returned per call, limit:100')
@click.option('--access_token', help='Your unique access token')
def leaderboard(list_id, count, access_token):
    '''
    This function generates a data frame containing all the
    accounts (with information) for the given List ID.

    Args:
        list_id (int): This ID corresponds to the saved list of Facebook pages.
        count (int): The number of accounts to be returned per API request.
        access_token(str): The access token associated with your CrowdTangle account.

    Returns: Complete data frame containing all the accounts.
                 Example(headers):   id(str), name(str), handle(str)......
    '''
    if access_token is None:
        import Access_Token
        access_token = Access_Token.access_token

    all_accounts = pd.DataFrame(columns=[''])
    query = f'https://api.crowdtangle.com/leaderboard?token={access_token}&listId={list_id}&count={count}&startDate=2021-09-26&endDate=2021-10-10'

    while(query != ''):
        try:
            print("Fetching:\t", query)

            r = requests.get(query)
            json_response = r.json()
            status = r.status_code
            logger.debug(status)
            
            if (status == 429):

                print("API rate limit hit, sleeping...")
                time.sleep(60)

                continue
            normalized_json = pd.json_normalize(
                json_response['result']['accountStatistics'])

            data_frame = pd.DataFrame.from_dict(
                normalized_json, orient="columns", dtype=str)

            pd.set_option('display.max_columns', None)
            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_colwidth', None)
            accounts_count = len(data_frame)
            logger.debug(accounts_count)

            if(status == 200 and accounts_count != 0):

                accounts = data_frame
                all_accounts = all_accounts.append(accounts)
                query = json_response['result']['pagination']['nextPage']

            else:
                print("Other Status: ", status)
                query = ''

        except KeyError:
            print("No next page")
            print(json_response)
            file_name = "26.09-10.10_stats.csv"
            all_accounts.to_csv(file_name, encoding='utf-8')

            break

    return None
