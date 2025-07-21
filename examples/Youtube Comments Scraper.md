# Youtube Comments Scraper With Python

Returns comments from YouTube videos.[Outscraper API](https://app.outscraper.cloud/api-docs#tag/Reviews-and-Comments/paths/~1youtube-comments/get).

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
# Get information about the comments from YouTube videos:
results = client.youtube_comments(['https://www.youtube.com/watch?v=ph5pHgklaZ0'])
```
