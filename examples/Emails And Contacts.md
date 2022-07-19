# Emails And Contacts Scraper With Python

Allows finding email addresses, social links, and phones from domains via [Outscraper API](https://app.outscraper.com/api-docs#tag/Emails-and-Contacts).

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
# Search contacts from website:
result = client.emails_and_contacts(['outscraper.com'])
```
