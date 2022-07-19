# Google Maps Reviews Scraper With Python

The library provides real-time access to the reviews from Google Maps via [Outscraper API](https://app.outscraper.com/api-docs#tag/Google-Reviews).

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

## Usage

```python
# Get reviews of the specific place by id
result = client.google_maps_reviews_v3(['ChIJrc9T9fpYwokRdvjYRHT8nI4'], reviews_limit=20, language='en')

# Get reviews for places found by search query
result = client.google_maps_reviews_v3(['Memphis Seoul brooklyn usa'], reviews_limit=20, limit=500, language='en')

# Get only new reviews during last 24 hours
yesterday_timestamp = 1657980986
result = client.google_maps_reviews_v3(
    ['ChIJrc9T9fpYwokRdvjYRHT8nI4'], sort='newest', cutoff=yesterday_timestamp, reviews_limit=100, language='en')

# Scrap Places Reviews by Place Ids
results = client.google_maps_reviews_v3(
    ["ChIJN5X_gWdZwokRck9rk2guJ1M", "ChIJxWLy8DlawokR1jvfXUPSTUE"],
    reviewsLimit=20, # limit of reviews per each place
    limit=1, # limit of palces per each query
)

for place in results:
    print('name:', place['name'])
    for review in place.get('reviews_data', []):
        print('review:', review['review_text'])

# Scrap Only New Reviews
results = client.google_maps_reviews_v3(
    ["ChIJN5X_gWdZwokRck9rk2guJ1M", "ChIJxWLy8DlawokR1jvfXUPSTUE"],
    reviewsLimit=1000,
    limit=1,
    sort='newest',
    cutoff=1654596109, # the maximum timestamp value for reviews (oldest review you want to extract). Can be used to scrape only the new reviews since your latest update
)

for place in results:
    print('name:', place['name'])
    new_reviews = place.get('reviews_data', []))
    print('new reviews', len(new_reviews))
```
