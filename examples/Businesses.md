# Business Details With Python

Retrieves a complete business profile for a specific business by `os_id`, `place_id`, or `google_id`, with optional enrichments via [Outscraper API](https://app.outscraper.cloud/api-docs#tag/businesses--poi/POST/businesses).

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
[Link to the profile page to create the API key](https://app.outscraper.cloud/profile)

## Usage

```python
# Get business details by Outscraper ID (os_id):
business = client.businesses.get('os_id')

# Get business details by Google Place ID:
business = client.businesses.get('place_id')

# Get business details by Google Business ID (google_id):
business = client.businesses.get('google_id')

# Request only specific fields (optional):
business = client.businesses.get(
    'os_id',
    fields=['name', 'phone', 'website', 'address', 'rating', 'reviews']
)

# Search (one page):
from outscraper.schema.businesses import BusinessFilters

filters = BusinessFilters(
    country_code='US',
    states=['NY'],
    cities=['New York', 'Buffalo'],
    types=['restaurant', 'cafe'],
    has_website=True,
    has_phone=True,
    business_statuses=['operational'],
)

result = client.businesses.search(
    filters=filters,
    limit=100,
    include_total=False,
    fields=[
        'name',
        'types',
        'address',
        'state',
        'postal_code',
        'country',
        'website',
        'phone',
        'rating',
        'reviews',
        'photo',
    ]
)

# Search with dict filters (alternative)
result = client.businesses.search(
    filters={
        'country_code': 'US',
        'states': ['NY'],
        'types': ['restaurant', 'cafe'],
        'has_website': True,
        'business_statuses': ['operational'],
    },
    limit=50
)

# Collect search parameters in one json:
json = {
    'limit': 10,
    'cursor': None,
    'include_total': False,
    'fields': ['name', 'types', 'address', 'state', 'postal_code', 'country', 'website', 'phone', 'rating', 'reviews', 'photo'],
    'filters': {
        "country_code": "US",
        "states": [
            "NY"
        ],
        "cities": [
            "New York",
            "Buffalo"
        ],
        "types": [
            "restaurant",
            "cafe"
        ],
        "has_website": True,
        "has_phone": True,
        "business_statuses": ["operational"],
    }
}
result = client.businesses.search(**json)

# Iterate over all results (auto-pagination)
from outscraper.schema.businesses import BusinessFilters

filters = BusinessFilters(country_code='US', states=['NY'], business_statuses=['operational'])

for business in client.businesses.iter_search(
    filters=filters,
    limit=100,
    fields=['name', 'phone', 'address', 'rating', 'reviews']
):
    # business is a Business dataclass instance
    print(business)
```
