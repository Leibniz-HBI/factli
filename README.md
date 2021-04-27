# DBoeS-stats
Collectors of reputation metrics of public speakers in social media platforms 

### About

The Facebook directory extracts content from CrowdTangle and creates CSV files containing the statistics of facebook pages. 
## Basic Installation

### Cloning this Repo

To clone this repository type:

```
git clone https://github.com/Leibniz-HBI/DBoeS-stats.git
```

This will download this repository. You will need to have git installed.
You can find additional information on how to do it here:

[Install Git for any Operation System](https://github.com/git-guides/install-git)

Alternatively you can download a zip folder or clone the repository via the green 'Code' button on the upper right of our repository.

### Enviroment 

1. Install pipenv to create a virtual enviroment. The latest version can be found here:
[pipenv](https://pipenv.readthedocs.io/en/latest)

2. After installing pipenv, navigate to the directory of the application and run:

```
pipenv install
```
This will create a virtual envirement with the credentials that we have provided in
our pipfile. 

After this you can start a shell in the virtual environment with:

```
pipenv shell
```

You can execute the application within the shell with:

```
python main.py
```
### Packages Required
Pandas
```
pipenv install pandas
```

### Usage (Number of Posts)
```
usage: number_of_posts.py [-h] -l  [-a] [-s] [-e]

Retrieve list of accounts

optional arguments:
  -h, --help            show this help message and exit
  -l , --list_id        Saved List ID
  -a , --access_token   Your unique access token
  -s , --start_date     Start Date (older), Format=YYYY-MM-DD
  -e , --end_date       End Date(newer), Format=YYYY-MM-DD
```
### Usage (List of Account IDs)
```
usage: get_list.py [-h] -l  [-a]

Retrieve list of accounts

optional arguments:
  -h, --help            show this help message and exit
  -l , --list_id        Saved List ID
  -a , --access_token   Your unique access token
```
### Creating and Saving the CSV File
```
file_name = str(date.today()) + ".csv"
accounts_df.to_csv(file_name, encoding='utf-8')
```
### Development and Testing

For development purposes we conduct tests before writing functions. 

#### Run all tests

To run all test you can run following command in the shell:

```
python -m unittest -v
```

Run a single test file:

```
python -m unittest -v test/mytest.py
```

#### Writing tests

Create a python file containing unittest with the name `test_*.py` within the `test` directory.

# Run tests

```
python -m unittest -v
```
