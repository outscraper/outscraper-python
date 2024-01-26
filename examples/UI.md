# Outscraper Platform UI

Allows using Outscraper Platform via [Outscraper API](https://app.outscraper.com/api-docs#tag/Outscraper-Platform-UI

## Installation

Python 3+
```bash
pip install outscraper
```

[Link to the Python package page](https://pypi.org/project/outscraper/)

## Initialization
```python
from outscraper import ApiClient

client = ApiClient(api_key='SECRET_API_KEY')
```
[Link to the profile page to create the API key](https://app.outscraper.com/profile)

## Get all UI tasks

```python
all_tasks = []

has_more = True
last_id = None

while has_more:
    tasks, has_more = api_client.get_tasks(last_id=last_id, page_size=20)

    if not tasks:
        break

    last_id = tasks[-1]['id']
    all_tasks.extend(tasks)
```

## Create UI Task for Google Maps Scraper

```python
import requests


json_data = {
    'service_name': 'google_maps_service_v2', # service ID
    'queries': [], # leave empty when using locations and enrichLocations
    'settings': {
        'output_extension': 'xlsx',
        'output_columns': [], # leave empty to get all columns
    },
    'tags': ['my first huge API task'],
    'enrichments': [
        'domains_service',
        'company_insights_service',
    ],
    'categories': [
        'restaurant',
        'dentist',
    ],
    'locations': [
        'SE>Stockholm',
    ],
    'language': 'en', # 2 letter language code
    'region': 'SE', # 2 letter country code
    'limit': 0, # total limit, 0 - unlimited
    'organizationsPerQueryLimit': 500, # limit per each query (keep it as it is)
    'useZipCodes': True, # required to use zip codes
    'dropDuplicates': True,
    'dropEmailDuplicates': False,
    'ignoreWithoutEmails': False,
    'enrichLocations': True, # reiqred when using locations
}

response = requests.post('https://api.app.outscraper.com/tasks', headers={'X-API-KEY': 'SECRET_API_KEY'}, json=json_data)
```

