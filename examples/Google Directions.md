# Google Directions With Python

Returns directions between two points from Google Maps. [Outscraper API](https://app.outscraper.cloud/api-docs#tag/Google/paths/~1maps~1directions/get).

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
# Returns directions:
results = client.google_maps_directions([
    ['29.696596, 76.994928', '30.715966244353, 76.8053887016268'],
    ['29.696596, 76.994928', '30.723065, 76.770169']
])
```
