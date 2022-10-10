# Run Requests to Outscraper API in Parallel

The example shows how to create multiple requests to Outscraper API in parallel to increase the execution time.

## Installation

Python 3+
```bash
pip install outscraper
```
[Link to the Python package page](https://pypi.org/project/outscraper/)

## Initialization
```python
from functools import partial
from multiprocessing.pool import ThreadPool

from outscraper import ApiClient


client = ApiClient(api_key='SECRET_API_KEY')
```
[Link to the profile page to create the API key](https://app.outscraper.com/profile)

## Usage

```python
place_ids = [
    'ChIJNw4_-cWXyFYRF_4GTtujVsw',
    'ChIJ39fGAcGXyFYRNdHIXy-W5BA',
    'ChIJVVVl-cWXyFYRQYBCEkX0W5Y',
    'ChIJScUP1R6XyFYR0sY1UwNzq-c',
    'ChIJmeiNBMeXyFYRzQrnMMDV8Jc',
    'ChIJifOTBMeXyFYRmu3EGp_QBuY',
    'ChIJ1fwt-cWXyFYR2cjoDAGs9UI',
    'ChIJ5zQrTzSXyFYRuiY31iE7M1s',
    'ChIJQSyf4huXyFYRpP9W4rtBelA',
    'ChIJRWK5W2-byFYRiaF9vVgzZA4'
]

pool = ThreadPool(4) # number of threads, use something between 2 and 40
results = pool.map(partial(client.google_maps_search, language='en', region='US'), place_ids)
```
