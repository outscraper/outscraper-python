# Similarweb With Python

Returns website analytics data including traffic, rankings, audience insights, and competitive intelligence from SimilarWeb [Outscraper API](https://app.outscraper.cloud/api-docs#tag/Domain-Related/paths/~1similarweb/get).

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
# Get data from Similarweb businesses:
results = client.similarweb(['apple.com'])
