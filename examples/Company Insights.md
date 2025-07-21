# Company Insights With Python

Finds company details such as revenue, size, founding year, public status, etc. [Outscraper API](https://app.outscraper.cloud/api-docs#tag/Other-Services/paths/~1company-insights/get).

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
# Get information about the companies:
results = client.company_insights(['outscraper.com'])
```
