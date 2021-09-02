# DBoeS-stats
Collectors of reputation metrics of public speakers in social media platforms 

### About

The Facebook directory-

1. extracts posts of accounts and creates individual folders containing JSON response for every account (get_posts.py). 
2. extracts content from CrowdTangle and creates CSV files containing the statistics of facebook pages (get_list.py). 

### Storing API Access Token 

Store your API access token in a python file, name it Access_Token.py and save it in the DBoeS-stats directory.
In the file store the access token as:
```
access_token = "API access token generated from your crowd tangle account"
```
## Installation
1. Install [poetry](https://python-poetry.org/docs/#installation)
2. Clone repository
3. In the directory run `poetry install`
4. Run `poetry shell` to start development virtualenv
5. Run `factli`.

### Cloning this Repo

To clone this repository type:

```
git clone https://github.com/Leibniz-HBI/DBoeS-stats.git
```
### Usage
```
usage: factli [OPTIONS]

Options:
  --list_id TEXT       Saved List ID
  --count INTEGER      Number of posts returned per call, maximum 100,
                       defaults to 10
  --access_token TEXT  Your unique access token
  --start_date TEXT    Start Date (older), Format=YYYY-MM-DD, if not given
                       defaults to NULL
  --end_date TEXT      End Date(newer), Format=YYYY-MM-DD, if not given
                       defaults to current date
  --time_frame TEXT    The interval of time to consider from the endDate. Any
                       valid SQL interval, eg: "1 HOUR" or "30 MINUTE"
  --log_level TEXT     Level of output detail (DEBUG, INFO, WARNING, ERROR).
                       Warnings and Errors are               always logged in
                       respective log-files `errors.log` and `warnings.log`.
                       Default: ERROR
  --log_file TEXT      Path to logfile. Defaults to standard output.
  --sched TEXT         If given, waits "sched" hour(s) and then repeats.
  --notify TEXT        If given, notify email address in case of unexpected
                       errors. Needs further setup. See README.
  --path TEXT          If given, stores the output at the desired location
                       (Absolute Path needed)
  --help               Show this message and exit.
```
Email notifications with the `-n` argument use [yagmail](https://pypi.org/project/yagmail/).
## Output

Output of get_posts.py stores the raw JSON response in the following folder structure:


`Facebook/results/list_id/account_id/start-date_end-date.json`

An example of the JSON data can be viewed [here](https://github.com/CrowdTangle/API/wiki/Posts).

## Ensure that factli is continuously running, even after restart
If your system can run cronjobs, stop twacapic, run `crontab -e` and add the following to your crontab:

```cron
30 6 * * *    sh -c "cd PATH/TO/YOUR/DBoeS-stats/WORKING/DIRECTORY && PATH/TO/Poetry-env run factli [YOUR ARGUMENTS HERE]" >> out.txt 2>&1
```

This will start collection at 0630Hr (GMT) everyday. 
