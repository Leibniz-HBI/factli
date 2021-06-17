# DBoeS-stats
Collectors of reputation metrics of public speakers in social media platforms 

### About

The Facebook directory-

1. extracts content from CrowdTangle and creates CSV files containing the statistics of facebook pages (get_list.py). 
2. extracts posts of accounts and creates individual folders containing JSON response for every account (get_posts.py). 
## Basic Installation

### Cloning this Repo

To clone this repository type:

```
git clone https://github.com/Leibniz-HBI/DBoeS-stats.git
```

### Enviroment 

1. Install pipenv to create a virtual environment. The latest version can be found here:
[pipenv](https://pipenv.readthedocs.io/en/latest)

2. After installing pipenv, navigate to the DBoeS directory and run:

```
pipenv install
```
This will create a virtual environment with the credentials that we have provided in
our pipfile. 

Add ~/local/bin to PATH. Open ~/.profile file and add this line to the file: 
```
export PATH =”~/.local/bin:$PATH”
```
Then run:
```
source ~/.profile 
```
for the changes to take effect.

After this you can start a shell in the virtual environment with:

```
pipenv shell
```
To deactivate the virtual environment simply run: 
```
deactivate
```
You can execute the application within the shell with the options listed in the Usage section:

```
python get_posts.py/ get_list.py
```
### Storing Access Token 

Store your access token in a python file and name it Access_Token.py


### Usage (Posts)
```
usage: python get_posts.py [OPTIONS]

  This function generates individual folders containing posts from accounts (with complete information) for the given List ID.

  Args:     list_id (int): This ID corresponds to the saved list of Facebook pages.
              count (int): The number of posts to be returned per API request.
        access_token(str): The access token associated with your CrowdTangle account.
          start_date(str): The earliest date at which a post could be posted.
            end_date(str): The latest date at which a post could be posted.

  Returns: None

Options:
  --list_id TEXT       Saved List ID
  --count INTEGER      Number of posts returned per call
  --access_token TEXT  Your unique access token
  --start_date TEXT    Start Date (older), Format=YYYY-MM-DD
  --end_date TEXT      End Date(newer), Format=YYYY-MM-DD
  --help               Show this message and exit.
```
### Usage (List)
```
usage: python get_list.py [Options]

  This function generates a data frame containing all the accounts (with complete information) for the given List ID.

  Args:     list_id (int): This ID corresponds to the saved list of Facebook pages.
              count (int): The number of accounts to be returned per API request.
        access_token(str): The access token associated with your CrowdTangle account.

  Returns: Complete data frame containing all the accounts.
  Example(headers):   id(str), name(str), handle(str)......

Options:
  --list_id TEXT       Saved List ID
  --count INTEGER      Number of accounts returned per call
  --access_token TEXT  Your unique access token
  --help               Show this message and exit.

```


