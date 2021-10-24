import requests
import time
import pandas as pd
from datetime import date
from loguru import logger
import click


@click.command()
@click.option('--list_id', help='Saved List ID')
@click.option('--count', default=10000, help='Number of accounts returned per call, no limit')
@click.option('--access_token', help='Your unique access token')
def lists(list_id, count, access_token):
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
    query = 'https://api.crowdtangle.com/lists/' + \
        str(list_id) + '/accounts?token=' + \
        str(access_token) + '&count=' + str(count)

    while(query != ''):
        try:
            print("Fetching:\t", query)

            r = requests.get(query)
            json_response = r.json()

            normalized_json = pd.json_normalize(
                json_response['result']['accounts'])

            data_frame = pd.DataFrame.from_dict(
                normalized_json, orient="columns", dtype=str)

            pd.set_option('display.max_columns', None)
            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_colwidth', None)
            accounts_count = len(data_frame)
            logger.debug(accounts_count)
            status = r.status_code

            if (status == 429):

                print("API rate limit hit, sleeping...")
                time.sleep(60)

                continue

            elif(status == 200 and accounts_count != 0):

                accounts = data_frame
                all_accounts = all_accounts.append(accounts)
                query = json_response['result']['pagination']['nextPage']

            else:
                print("Other Status: ", status)
                query = ''

        except KeyError:
            print("No next page")
            file_name = str(date.today()) + "_lists.csv"
            all_accounts.to_csv(file_name, encoding='utf-8')

            break

    return None
