import os
import json
import time
import pathlib
import datetime
import requests
import pandas as pd
import Access_Token
from loguru import logger
import click

str0 = pathlib.Path.cwd()
str1 = "results"
pathlib.Path(f'{str1}').mkdir(exist_ok=True)
os.chdir(f'{str0}/results')


@click.command()
@click.option('--list_id', help='Saved List ID')
@click.option('--count', default=100, help='Number of posts returned per call')
@click.option('--access_token', help='Your unique access token')
@click.option('--start_date', help='Start Date (older), Format=YYYY-MM-DD')
@click.option('--end_date', help='End Date(newer), Format=YYYY-MM-DD')
def ct_get_posts(list_id, count, access_token, start_date, end_date):
    '''
    This function generates individual folders containing posts from
    accounts (with information) for the given List ID.

    Args:
        list_id (int): This ID corresponds to the saved list of Facebook Pages.
        count (int): The number of posts to be returned per API request.
        access_token(str): The access token associated with your CrowdTangle account.
        start_date(str): The earliest date at which a post could be posted.
        end_date(str): The latest date at which a post could be posted.

    Returns: None
    '''

    pathlib.Path(f'{list_id}').mkdir(exist_ok=True)
    os.chdir(f'{str0}/results/{list_id}')
    if access_token is None:
        access_token = Access_Token.access_token

    if start_date is None:
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=1)

    # query = 'https://api.crowdtangle.com/' + '/posts?token=' + str(access_token) + '&listIds=' + str(
        # list_id) + '&startDate=' + str(start_date) + '&endDate=' + str(end_date) + '&count=' + str(count)
    query = f'https://api.crowdtangle.com/posts?token={access_token}&sortBy=date&listIds={list_id}&startDate={start_date}&endDate={end_date}&count={count}'

    while(query != ''):
        try:

            print("Fetching:\t", query)

            r = requests.get(query)

            json_response = r.json()
            if (json_response['status'] == 429):

                logger.info("API rate limit hit, sleeping...")
                time.sleep(60)

                continue

            normalized_json = pd.json_normalize(
                json_response['result']['posts'])

            data_frame = pd.DataFrame.from_dict(
                normalized_json, orient="columns", dtype=str)

            posts_count = len(data_frame)
            logger.debug(posts_count)

            status = r.status_code
            logger.debug(status)

            if(status == 200 and posts_count != 0):

                for i in range(posts_count):

                    x = str(json_response['result']['posts'][i-1]['account']['id'])
                    pathlib.Path(f'{x}').mkdir(exist_ok=True)
                    os.chdir(f'{str0}/results/{list_id}/{x}')

                    with open(f'{start_date}_{end_date}.json', 'a', encoding='utf8') as f:
                        json.dump(json_response['result']['posts'][i-1], f, ensure_ascii=False, indent=4)
                    query = json_response['result']['pagination']['nextPage']

                    os.chdir(f'{str0}/results/{list_id}')

            else:
                logger.info("Other Status: ", status)
                query = ''

        except KeyError:
            logger.info("No next page")

            break

    return None


if __name__ == "__main__":

    # list_id = 1484485
    ct_get_posts()
