# Using Enrichments Python

Using enrichments with [Outscraper API](https://app.outscraper.com/api-docs).

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
# Enriching data from Google Maps with Emails & Contacts Scraper and validating emails:
results = client.google_maps_search('bars ny usa', enrichment=[
    'domains_service', # Emails & Contacts Scraper
    'emails_validator_service' # Email Validator
])
```
