import os
import sys
import json
import time
import pathlib
import datetime
import requests
import pandas as pd
import click
import yagmail
import schedule
from loguru import logger

@click.command()
@click.option('--list_id', help='Saved List ID')
@click.option('--count', default=100, help='Number of posts returned per call, maximum 100, defaults to 10')
@click.option('--access_token', help='Your unique access token')
@click.option('--start_date', help='Start Date (older), Format=YYYY-MM-DD, if not given defaults to NULL')
@click.option('--end_date', help='End Date(newer), Format=YYYY-MM-DD, if not given defaults to current date')
@click.option('--time_frame', help='The interval of time to consider from the endDate. Any valid SQL interval, eg: "1 HOUR" or "30 MINUTE"')
@click.option('--log_level', help='Level of output detail (DEBUG, INFO, WARNING, ERROR). Warnings and Errors are \
              always logged in respective log-files `errors.log` and `warnings.log`.\
              Default: ERROR', default='ERROR')              
@click.option('--log_file', help='Path to logfile. Defaults to standard output.')
@click.option('--sched', help='If given, waits "sched" hour(s) and then repeats.')
@click.option('--notify', help='If given, notify email address in case of unexpected errors. Needs further setup. See README.')
@click.option('--path', help='If given, stores the output at the desired location (Absolute Path needed)')
def leaderboard(list_id, count, access_token, start_date, end_date, log_level, log_file, sched, notify, path, time_frame):
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
    str1 = pathlib.Path.cwd()
    
    if path is not None:
        str0 = path
        os.chdir(str0)  
        
    else:
        str0 = pathlib.Path.cwd()

    
    pathlib.Path(f'results/stats/{list_id}').mkdir(parents=True, exist_ok=True)
    os.chdir(f'{str0}/results/stats/{list_id}')

    if access_token is None:
        import Access_Token
        access_token = Access_Token.access_token
        
    try:
        with open('last_list_saved_date.txt') as f:
            d = f.read()
            end_date = d.replace(" ", "T")
        a = datetime.datetime.fromisoformat(end_date)
        b = a.date() - datetime.timedelta(days=1)
        start_date = f"{b}T{a.time()}"
        end_date = f"{a.date()}T{a.time()}"
        
    except FileNotFoundError:
        logger.error("File not created with the end date")
        start_date = None

    if log_file is None:
        logger.add(sys.stdout, level=log_level)
    else:
        logger.add(log_file, level=log_level, rotation="64 MB")
        logger.add(sys.stderr, level='ERROR')

    logger.add('errors.log', level='ERROR')
    logger.add('warnings.log', level='WARNING')


    query = f'https://api.crowdtangle.com/leaderboard?token={access_token}&orderBy=desc&listId={list_id}&endDate={end_date}&startDate={start_date}&count={count}'

    def start_collection(query):
        logger.info(f"Starting Leaderboard Collection of {list_id}")
        
        if notify is not None:
            send_mail(notify, "Hello", f"Leaderboard Collection started of {list_id}", str1)
        
        @retry
        def get_page(query):

            try:

                logger.info(f"Fetching:{query}")

                r = requests.get(query, timeout=10)
                status = r.status_code
                json_response = r.json()
                status = r.status_code
                logger.info(status)
                if (json_response['status'] == 429):

                    logger.info("API rate limit hit, sleeping...")
                    time.sleep(60)
                    return query
                
                
                logger.info(status)
                

                normalized_json = pd.json_normalize(
                    json_response['result']['accountStatistics'])
                data_frame = pd.DataFrame.from_dict(
                    normalized_json, orient="columns", dtype=str)

                accounts_count = len(data_frame)
                logger.debug(accounts_count)

                try:
                    assert status == 200
                except AssertionError as e:
                    logger.warning(r.text)
                    raise e
               
                if(status == 200 and accounts_count != 0):

                    for i in range(accounts_count):

                            x = str(json_response['result']['accountStatistics'][i-1]['account']['id'])
                            pathlib.Path(f'{x}').mkdir(exist_ok=True)
                            os.chdir(f'{str0}/results/stats/{list_id}/{x}')

                            date = end_date[0:10]

                            with open(f'{date}.ndjson', 'a', encoding='utf8') as f:
                                stat = json_response['result']['accountStatistics'][i-1]

                                json.dump(stat, f, ensure_ascii=False)
                                f.write("\n")

                            os.chdir(f'{str0}/results/stats/{list_id}')
                    next_page_query = json_response['result']['pagination']['nextPage']
                
                else:
                    logger.warning("Other Status: ", status)
                    next_page_query = ''

            except KeyError:
                logger.info(f"No next page, Collection finished for {list_id}")
                os.chdir(f'{str0}/results/stats/{list_id}')
                              
                with open('last_list_saved_date.txt', 'w', encoding='utf8') as f:
                    dt = start_date.replace("T", " ")
                    f.write(dt)
            
                next_page_query = ''

            return next_page_query

        while (query != ''):
            query = get_page(query)
        return None

    if sched is None:
        start_collection(query)
    else:
        logger.info(f"Scheduling job for every {sched} hour(s)")
        schedule.every(int(sched)).hours.do(start_collection, query)
        start_collection(query)
    
        while True:
            
            try:

                try: 
                    schedule.run_pending()
                    time.sleep(1)
                
                except Exception as e:
                    logger.error(e)
                    if notify is not None:
                        send_mail(notify, 'Hello', str(e), str1)

            except KeyboardInterrupt:
                logger.info("Keyboard Interrupt, Stopping Collection")
                if notify is not None:
                    send_mail(notify, "Error", "KeyboardInterrupt", str1)
                break


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


def send_mail(recipient, subject, content, str1):

    try:
        yag = yagmail.SMTP(oauth2_file=str1/'gmail_creds.json')
        yag.send(recipient, subject, content)
        logger.info(f'Email sent to {recipient}.\nSubject: {subject}\n{content}')
    except Exception as e:
        logger.error(f'Sending mail failed: {e}')
