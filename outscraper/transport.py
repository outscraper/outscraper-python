from time import sleep
from typing import Dict, Union

import requests


API_URLS = [
    'https://api.app.outscraper.com',
    'https://api.app.outscraper.cloud',
    'https://api.outscraper.net'
]


class OutscraperTransport:
    _max_ttl = 60 * 60
    _requests_pause = 5
    _max_retries = 2

    def __init__(self, api_key: str):
        self._api_headers: Dict[str, str] = {'X-API-KEY': api_key, 'client': f'Python SDK'}

    def api_request(self, method: str, path: str, *, wait_async: bool, async_request: bool, use_handle_response: bool, **kwargs) -> Union[
        requests.Response, list, dict]:
        for attempt in range(self._max_retries):

            for api_url in API_URLS:

                try:
                    response = requests.request(method, f'{api_url}{path}', headers=self._api_headers, **kwargs)
                except requests.RequestException:
                    continue

                if 500 <= response.status_code < 600:
                    continue

                if use_handle_response:
                    return self._handle_response(response, wait_async, async_request, api_url)
                return response
            sleep(self._requests_pause)

        raise Exception('Failed to perform request against all API URLs')

    def _handle_response(self, response: requests.models.Response, wait_async: bool, async_request: bool, api_url: str) -> Union[list, dict]:
        if 199 < response.status_code < 300:
            if response.json().get('error'):
                error_message = response.json().get('errorMessage')
                raise Exception(f'error: {error_message}')

            if wait_async:
                response_json = response.json()

                if async_request:
                    return response_json
                else:
                    return self._wait_request_archive(response_json['id'], api_url).get('data', [])
            else:
                return response.json().get('data', [])

        raise Exception(f'Response status code: {response.status_code}')

    def _wait_request_archive(self, request_id: str, api_url: str) -> dict:
        ttl = self._max_ttl / self._requests_pause

        while ttl > 0:
            ttl -= 1

            sleep(self._requests_pause)

            try:
                result = self.get_request_archive(request_id, api_url)
            except:
                sleep(self._requests_pause)
                result = self.get_request_archive(request_id, api_url)

            if result['status'] != 'Pending': return result

        raise Exception('Timeout exceeded')

    @staticmethod
    def get_request_archive(request_id: str, api_url: str) -> dict:
        '''
            Fetch request data from the archive

                Parameters:
                    request_id (str): unique id for the request provided by ['id']
                    api_url (str): base url of the API

                Returns:
                    dict: result from the archive

            See: https://app.outscraper.com/api-docs#tag/Requests/paths/~1requests~1{requestId}/get
        '''
        response = requests.get(f'{api_url}/requests/{request_id}')

        if 199 < response.status_code < 300:
            return response.json()

        raise Exception(f'Response status code: {response.status_code}')
