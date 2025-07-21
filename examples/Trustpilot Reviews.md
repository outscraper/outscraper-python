# Trustpilot Reviews With Python

Returns reviews from Trustpilot businesses. In case no reviews were found by your search criteria, your search request will consume the usage of one review.[Outscraper API](https://app.outscraper.cloud/api-docs#tag/Reviews-and-Comments/paths/~1trustpilot~1reviews/get).

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
# Get information about the reviews from Trustpilot:
results = client.trustpilot_reviews(['https://www.trustpilot.com/review/outscraper.com'])
```
