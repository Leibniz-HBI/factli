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

### Querying CrowdTangle Endpoint and extracting the JSON response
Generate your own Access Token( Don't share it with anyone) from the CrowdTangle website.
```
query = 'https://api.crowdtangle.com/lists/' + \
        str(list_id) + '/accounts?token=' + \
        str(access_token) + '&count=' + str(count)
r = requests.get(query)
json_response = r.json()
```
### Converting JSON response into a Readable Format
```
normalized_json = pd.json_normalize(json_response['result']['accounts'])

data_frame = pd.DataFrame.from_dict(normalized_json, orient="columns", dtype=str)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
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
