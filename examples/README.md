# Examples

Python SDK that allows using [Outscraper's services](https://outscraper.com/services/) and [Outscraper's API](https://app.outscraper.com/api-docs).

## Installation

Python 3+
```bash
pip install google-services-api
```

[Link to the python package page](https://pypi.org/project/google-services-api/)

## Initialization
```python
from outscraper import ApiClient

api_client = ApiClient(api_key='SECRET_API_KEY')
```
[Link to the profile page to create the API key](https://app.outscraper.com/profile)

## Example 1: Scrap Places by Two Queries

```python
results = api_client.google_maps_search_v2(
    ['restaurants brooklyn usa', 'bars brooklyn usa'],
    limit=50, # limit of palces per each query
    language='en',
    region='US',
)

for query_places in results:
    for place in query_places:
        print('query:', place['query'])
        print('name:', place['name'])
        print('phone:', place['phone'])
        print('website:', place['site'])
```

## Example 2: Scrap Places by Place Ids

```python
results = api_client.google_maps_search_v2(
    ["ChIJ8ccnM7dbwokRy-pTMsdgvS4", "ChIJN5X_gWdZwokRck9rk2guJ1M", "ChIJxWLy8DlawokR1jvfXUPSTUE"],
    limit=1, # limit of palces per each query
)

for query_places in results:
    for place in query_places:
        print('name:', place['name'])
        print('place_id:', place['place_id'])
```

## Example 3: Scrap Places Reviews by Place Ids

```python
results = api_client.google_maps_reviews_v3(
    ["ChIJN5X_gWdZwokRck9rk2guJ1M", "ChIJxWLy8DlawokR1jvfXUPSTUE"],
    reviewsLimit=20, # limit of reviews per each place
    limit=1, # limit of palces per each query
)

for place in results:
    print('name:', place['name'])
    for review in place.get('reviews_data', []):
        print('review:', review['review_text'])
```
