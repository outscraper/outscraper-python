# Using Enrichments Python

Using enrichments with [Outscraper API](https://app.outscraper.cloud/api-docs).

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
# Enriching data from Google Maps with Emails & Contacts Scraper and validating emails:
results = client.google_maps_search('bars ny usa', enrichment=[
    'contacts_n_leads', # Contacts & Leads Enrichment: finds emails, social links, phones, and other contacts from websites
    'emails_validator_service', # Email Address Verifier: validates emails, checks deliverability, filters out blacklists, spam traps, and complainers, while significantly reducing your bounce rate
    'company_insights_service', # Company Insights: finds company details such as revenue, size, founding year, public status, etc.
    'phones_enricher_service', # Phone Numbers Enricher: returns phones carrier data (name/type), validates phones, ensures messages deliverability
    'whitepages_phones', # Phone Numbers Enricher: returns insights about phone number owners (name, address, etc.)
])
```

## Available values

`contacts_n_leads` — **Contacts & Leads Enrichment**: finds emails, social links, phones, and other contacts from websites;

`emails_validator_service` — **Email Address Verifier**: validates emails, checks deliverability, filters out blacklists, spam traps, and complainers, while significantly reducing your bounce rate;

`disposable_email_checker` — **Disposable Emails Checker**: checks origins of email addresses (disposable, free, or corporate);

`company_insights_service` — **Company Insights**: finds company details such as revenue, size, founding year, public status, etc;

`phones_enricher_service` — **Phone Numbers Enricher**: returns phones carrier data (name/type), validates phones, ensures messages deliverability;

`trustpilot_service` — **Trustpilot Scraper**: returns data from a list of businesses;

`whitepages_phones` - **Phone Identity Finder**: returns insights about phone number owners (name, address, etc.);

`ai_chain_info` - **Chain Info**: identifies if a business is part of a chain, adding a true/false indication to your data for smarter targeting.
