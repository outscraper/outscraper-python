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

    _max_ttl = 60 * 10

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

        raise Exception('Timeout exceeded')

    def google_search(self, query, language='en', region='us'):
        response = requests.get(f'{self._api_url}/search', params={
            'query': query,
            'language': language,
            'region': region,
        }, headers={'X-API-KEY': self._api_key})

        if 199 < response.status_code < 300:
            sleep(10)
            return self._wait_request_archive(response.json()['id'], 2)

        raise Exception(f'Server response code: {response.status_code}')

    def google_maps_search(self, query, language='en', region='us', limit=400, extract_contacts=False, coordinates=None):
        response = requests.get(f'{self._api_url}/maps/search', params={
            'query': query,
            'coordinates': coordinates,
            'language': language,
            'region': region,
            'organizationsPerQueryLimit': limit,
            'extractContacts': extract_contacts,
        }, headers={'X-API-KEY': self._api_key})

        if 199 < response.status_code < 300:
            sleep(15)
            return self._wait_request_archive(response.json()['id'], 5)

        raise Exception(f'Server response code: {response.status_code}')

    def google_maps_business_reviews(self, query, language='en', region='us', limit=100, cutoff=None, coordinates=None):
        response = requests.get(f'{self._api_url}/maps/reviews', params={
            'query': query,
            'coordinates': coordinates,
            'language': language,
            'region': region,
            'limit': 1,
            'cutoff': cutoff,
            'reviewsPerOrganizationLimit': limit
        }, headers={'X-API-KEY': self._api_key})

        if 199 < response.status_code < 300:
            sleep(30)
            return self._wait_request_archive(response.json()['id'], 5).get('data', [])

        raise Exception(f'Server response code: {response.status_code}')
