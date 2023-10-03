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
