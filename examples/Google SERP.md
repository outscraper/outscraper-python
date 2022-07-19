# Google Search Results Scraper With Python

The library returns search results from Google based on a given search query via [Outscraper API](https://app.outscraper.com/api-docs#tag/Google-Search).

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
# Search for SERP results:
result = client.google_search(['buy iphone 13 TX'], language='en', region='us')
```
