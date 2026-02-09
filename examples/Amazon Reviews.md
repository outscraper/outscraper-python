# Amazon Reviews Scraper With Python

The library provides real-time access to Amazon product reviews via [Outscraper API](https://app.outscraper.com/api-docs#tag/Amazon/paths/~1amazon~1reviews/get).

You can use Amazon product URLs or ASINs as input queries.
It supports batching by sending arrays with up to 250 queries, so you can scrape multiple products in one request.

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

# 1) Get reviews for one product by URL
results = client.amazon_reviews(
    query=['https://www.amazon.com/dp/1612680194'],
    limit=10,
)

# 2) Get reviews for one product by ASIN
results = client.amazon_reviews(
    query=['1612680194'],
    limit=12,
)

# 3) Use batching (many products in one request)
results = client.amazon_reviews(
    query=[
        'https://www.amazon.com/dp/1612680194',
        'B0F22JJVMT',
    ],
    limit=8,
)

# 4) Filter and sort reviews
results = client.amazon_reviews(
    query=['1612680194'],
    limit=12,
    sort='recent',
    filter_by_reviewer='avp_only_reviews',  # verified purchase only
    filter_by_star='positive',
)

# 5) Use another Amazon domain
results = client.amazon_reviews(
    query=['https://www.amazon.co.uk/dp/B007AIIGWE'],
    limit=10,
    domain='amazon.co.uk',
)

# 6) Request only selected fields to make response lighter
results = client.amazon_reviews(
    query=['1612680194'],
    limit=5,
    fields=['query', 'id', 'product_asin', 'title', 'rating', 'date', 'body'],
)

# Print parsed reviews (beginner-friendly pattern)
for query_reviews in results:
    for review in query_reviews:
        print('asin:', review.get('product_asin'))
        print('rating:', review.get('rating'))
        print('title:', review.get('title'))
        print('date:', review.get('date'))
        print('review:', review.get('body'))

# 7) Async mode for background scraping (useful for larger jobs)
task = client.amazon_reviews(
    query=['1612680194', 'B0F22JJVMT'],
    limit=12,
    async_request=True,
)

```

## Main Parameters

- `query` (required): Amazon product URLs or ASINs.
- `limit`: Number of reviews per product query (default: `10`, max: `12`).
- `sort`: `helpful` or `recent`.
- `filter_by_reviewer`: `all_reviews` or `avp_only_reviews`.
- `filter_by_star`: `all_stars`, `five_star`, `four_star`, `three_star`, `two_star`, `one_star`, `positive`, `critical`.
- `domain`: Amazon domain such as `amazon.com`, `amazon.co.uk`, `amazon.de`, etc.
- `fields`: Return only specific fields.

