# Run Async Requests to Outscraper API

The example shows how to send async requests to Outscraper API and retrieve the results later using request IDs (the requests are processed in parallel).

## Installation

Python 3+
```bash
pip install outscraper
```
[Link to the Python package page](https://pypi.org/project/outscraper/)

## Initialization
```python
from time import sleep
from outscraper import ApiClient


client = ApiClient(api_key='SECRET_API_KEY')
```
[Link to the profile page to create the API key](https://app.outscraper.com/profile)

## Usage

```python
results = []
running_request_ids = set()
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

for place_id in place_ids:
    response = client.google_maps_search(place_id, limit=1, async_request=True)
    running_request_ids.add(response['id'])

attempts = 5 # retry 5 times
while attempts and running_request_ids: # stop when no more attempts are left or when no more running request ids
    attempts -= 1
    sleep(60)

    for request_id in list(running_request_ids): # we don't want to change the set while iterating, so cloning it to list
        result = client.get_request_archive(request_id)

        if result['status'] == 'Success':
            results.append(result['data'])
            running_request_ids.remove(request_id)

print(results)
```
