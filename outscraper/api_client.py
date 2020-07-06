import requests
import json
from time import sleep


class ApiClient(object):
    """OutScraperApiClient - Python sdk that allows extracting data from Google services via OutScraper API.
    ```python
    from outscraper import ApiClient
    api_cliet = ApiClient(api_key='SECRET_API_KEY')
    maps_result = api_cliet.google_maps_search('restaurants brooklyn usa')
    search_result = api_cliet.google_search('bitcoin')
    ```
    https://github.com/outscraper/google-services-api-pyhton
    """

    _api_url = 'https://api.app.outscraper.com'
    _api_key = None

    _max_ttl = 60 * 5

    def __init__(self, api_key):
        self._api_key = api_key

    def get_request_archive(self, request_id):
        """Fetch request data from archive
        Parameters:
            request_id (int): unique id for the request provided by ['id']
        Returns:
            dict: result from the archive
        """
        response = requests.get(f'{self._api_url}/requests/{request_id}')
        return response.json()

    def _wait_request_archive(self, request_id, requests_pause):
        ttl = self._max_ttl / requests_pause

        while ttl > 0:
            ttl -= 1

            result = self.get_request_archive(request_id)
            if result['status'] != 'Pending': return result

            sleep(requests_pause)

    def google_search(self, query, language='en', region='us'):
        response = requests.get(f'{self._api_url}/search', params={
            'apiKey': self._api_key,
            'async': True,
            'query': query,
            'language': language,
            'region': region,
        })

        sleep(10)
        return self._wait_request_archive(response.json()['id'], 2)

    def google_maps_search(self, query, language='en', region='us', limit=400, extract_contacts=False, coordinates=None):
        response = requests.get(f'{self._api_url}/maps/search', params={
            'apiKey': self._api_key,
            'async': True,
            'query': query,
            'coordinates': coordinates,
            'language': language,
            'region': region,
            'organizationsPerQueryLimit': limit,
            'extractContacts': extract_contacts,
        })

        sleep(15)
        return self._wait_request_archive(response.json()['id'], 5)

    def google_maps_business_reviews(self, query, language='en', region='us', limit=100, cutoff=None, coordinates=None):
        response = requests.get(f'{self._api_url}/maps/reviews', params={
            'apiKey': self._api_key,
            'async': True,
            'query': query,
            'coordinates': coordinates,
            'language': language,
            'region': region,
            'limit': 1,
            'cutoff': cutoff,
            'reviewsPerOrganizationLimit': limit
        })

        sleep(30)
        return self._wait_request_archive(response.json()['id'], 5).get('data', [])
