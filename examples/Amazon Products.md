# Amazon Products Scraper With Python

The library provides real-time access to Amazon product pages via [Outscraper API](https://app.outscraper.com/api-docs#tag/Amazon/paths/~1amazon~1products-v2/get).
You can use Amazon products, searches, or summary page URLs.

It supports batching by sending arrays with up to 250 queries.
It allows multiple queries to be sent in one request and to save on network latency time.

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
# Get a single product by URL
results = client.amazon_products(
    ['https://www.amazon.com/dp/B0F22JJVMT',
     'https://www.amazon.com/dp/B07ZMKXMTG'],
    domain='amazon.com',
    postal_code='10001',
    fields=['asin', 'name', 'availability', 'price_parsed']
)

# Get products from a search results page (summary page)
results = client.amazon_products(
    ['https://www.amazon.com/s?k=wireless+earbuds'],
    limit=20,
    domain='amazon.com',
    postal_code='11201',
)

# Use multiple queries in one request (batching)
results = client.amazon_products(
    [
        'https://www.amazon.com/s?k=gaming+mouse',
        'https://www.amazon.com/s?k=mechanical+keyboard',
    ],
    limit=10,
    domain='amazon.com',
)

# Print a few key fields from the response
for query_results in results:
    for product in query_results:
        print('name:', product.get('name'))
        print('price:', product.get('price'))
        print('asin:', product.get('asin'))
        print('url:', product.get('url'))
```
