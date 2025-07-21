# Tripadvisor Reviews Scraper With Python

Returns reviews from Tripadvisor businesses.
In case no reviews were found by your search criteria, your search request will consume the usage of one review. [Outscraper API](https://app.outscraper.cloud/api-docs#tag/Reviews-and-Comments/paths/~1tripadvisor-reviews/get).

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
# Get information about business:
results = client.tripadvisor_reviews(['https://www.tripadvisor.com Restaurant_Review-g187147-d12947099-Reviews-Mayfair_Garden-Paris_Ile_de_France.html'])
```
