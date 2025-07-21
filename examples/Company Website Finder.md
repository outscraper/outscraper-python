# Company Website Finder With Python

Finds company websites based on business names.[Outscraper API](https://app.outscraper.cloud/api-docs#tag/Domain-Related/paths/~1company-website-finder/get).

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
results = client.company_websites_finder(['Apple Inc'])
```
