# Emails And Contacts Scraper With Python

Allows finding email addresses, social links, and phones from domains via [Outscraper API](https://app.outscraper.cloud/api-docs#tag/Email-Related/paths/~1contacts-and-leads/get).

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
# Search contacts from website:
results = client.contacts_and_leads(['outscraper.com'])
```
