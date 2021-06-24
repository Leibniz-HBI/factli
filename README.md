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
### Usage (Posts)
```
usage: factli [OPTIONS]

Options:
  --list_id TEXT       Saved List ID (mandatory)
  --count INTEGER      Number of posts returned per call, maximum 100, if not given defaults to 100
  --access_token TEXT  Your unique access token
  --start_date TEXT    Start Date (older), Format=YYYY-MM-DD, if not given defaults to NULL
  --end_date TEXT      End Date(newer), Format=YYYY-MM-DD, if not given defaults to current date
  --help               Show this message and exit.
```

## Output

Output of get_posts.py stores the raw JSON response in the following folder structure:


`Facebook/results/list_id/account_id/start-date_end-date.json`

An example of the JSON data can be viewed [here](https://github.com/CrowdTangle/API/wiki/Posts)

Output of get_list.py stores the accounts of a saved list in a CSV file of the format:
``` date_lists.csv```

Example(only headers):   id(str), name(str), handle(str)......




