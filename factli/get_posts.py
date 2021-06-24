import os
import sys
import json
import time
import pathlib
import datetime
import requests
import pandas as pd
import Access_Token
from loguru import logger
import click
import requests.exceptions

str0 = pathlib.Path.cwd()
str1 = "results"
pathlib.Path(f'{str1}').mkdir(exist_ok=True)
os.chdir(f'{str0}/results')


@click.command()
@click.option('--list_id', help='Saved List ID')
@click.option('--count', default=100, help='Number of posts returned per call, maximum 100, defaults to 10')
@click.option('--access_token', help='Your unique access token')
@click.option('--start_date', help='Start Date (older), Format=YYYY-MM-DD, if not given defaults to NULL')
@click.option('--end_date', help='End Date(newer), Format=YYYY-MM-DD, if not given defaults to current date')
@click.option('--log_level', help='Level of output detail (DEBUG, INFO, WARNING, ERROR). Warnings and Errors are \
              always logged in respective log-files `errors.log` and `warnings.log`.\
              Default: ERROR', default='ERROR')
@click.option('--log_file', help='Path to logfile. Defaults to standard output.')
def ct_get_posts(list_id, count, access_token, start_date, end_date, log_level, log_file):
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

    if log_file is None:
        logger.add(sys.stdout, level=log_level)
    else:
        logger.add(log_file, level=log_level, rotation="64 MB")
        logger.add(sys.stderr, level='ERROR')

    logger.add('errors.log', level='ERROR')
    logger.add('warnings.log', level='WARNING')
    query = f'https://api.crowdtangle.com/posts?token={access_token}&sortBy=date&listIds={list_id}&startDate={start_date}&endDate={end_date}&count={count}'

    @retry
    def get_page(query):

        try:

            logger.info(f"Fetching:{query}")

            r = requests.get(query, timeout=5)

            json_response = r.json()
            if (json_response['status'] == 429):

                logger.info("API rate limit hit, sleeping...")
                time.sleep(60)
                return query

            normalized_json = pd.json_normalize(
                json_response['result']['posts'])

            data_frame = pd.DataFrame.from_dict(
                normalized_json, orient="columns", dtype=str)

            posts_count = len(data_frame)
            logger.debug(posts_count)

            status = r.status_code
            logger.info(status)
            try:
                assert status == 200
            except AssertionError as e:
                logger.warning(r.text)
                raise e

            if(status == 200 and posts_count != 0):

                for i in range(posts_count):

                    x = str(json_response['result']['posts'][i-1]['account']['id'])
                    pathlib.Path(f'{x}').mkdir(exist_ok=True)
                    os.chdir(f'{str0}/results/{list_id}/{x}')

                    with open(f'{start_date}_{end_date}.json', 'a', encoding='utf8') as f:
                        json.dump(json_response['result']['posts'][i-1], f, ensure_ascii=False, indent=4)
                    next_page_query = json_response['result']['pagination']['nextPage']

                    os.chdir(f'{str0}/results/{list_id}')

            else:
                logger.warning("Other Status: ", status)
                # query = ''

        except KeyError:
            logger.info("No next page, Collection over")
            next_page_query = ''

        return next_page_query

    while (query != ''):
        query = get_page(query)

    return None


def retry(func):

    def retried_func(*args, **kwargs):
        max_tries = 10
        tries = 0
        total_sleep_seconds = 0

        while True:
            try:
                resp = func(*args, **kwargs)

            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, AssertionError) as e:

                logger.warning(e)

                if tries < max_tries:

                    tries += 1

                    sleep_seconds = min(((tries * 2) ** 2), max(900 - total_sleep_seconds, 30))
                    total_sleep_seconds = total_sleep_seconds + sleep_seconds
                else:
                    logger.exception('Maximum retries reached. Raising Exception …')
                    raise e

                logger.warning(f"Retry in {sleep_seconds} seconds …")
                time.sleep(sleep_seconds)
                continue

            break

        return resp

    return retried_func


if __name__ == "__main__":

    # list_id = 1484485
    ct_get_posts()