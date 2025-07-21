# Email Addresses Finder Scraper With Python

Allows to validate email addresses. Checks if emails are deliverable. [Outscraper API](https://app.outscraper.cloud/api-docs#tag/Email-Related/paths/~1email-validator/get).

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
# Validate email addresses:
results = client.validate_emails(['support@outscraper.com'])
```
