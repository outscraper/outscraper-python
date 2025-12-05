# Trustpilot Search Scraper With Python

Returns search results from Trustpilot. [Outscraper API](https://app.outscraper.cloud/api-docs#tag/Trustpilot/paths/~1trustpilot~1search/get).

## Installation

Python 3+
```bash
pip install outscraper
```

[Link to the Python package page](https://pypi.org/project/outscraper/)

## Initialization
```python
from outscraper import OutscraperClient

client = OutscraperClient(api_key='SECRET_API_KEY')
```
[Link to the profile page to create the API key](https://app.outscraper.com/profile)

## Usage

```python
# Get information about the search results from Trustpilot:
results = client.trustpilot_search(['real estate'])
```
