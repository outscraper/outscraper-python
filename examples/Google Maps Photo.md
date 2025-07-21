# Google Maps Photos With Python

Returns Google Maps photos from places when using search queries (e.g., restaurants, Manhattan, NY, USA) or from a single place when using IDs or names (e.g., NoMad Restaurant, NY, USA, 0x886916e8bc273979:0x5141fcb11460b226, ChIJu7bMNFV-54gR-lrHScvPRX4).
In case no photos were found by your search criteria, your search request will consume the usage of one photo.[Outscraper API](https://app.outscraper.cloud/api-docs#tag/Google/paths/~1maps~1photos-v3/get).

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
# Get information about the places photos:
results = client.google_maps_photos(['The NoMad Restaurant, NY, USA'])
```
