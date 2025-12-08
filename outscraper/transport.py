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
        for api_url in API_URLS:

            try:
                response = requests.request(method, f'{api_url}{path}', headers=self._api_headers, **kwargs)
            except (requests.exceptions.ConnectionError, requests.exceptions.SSLError):
                continue

            if use_handle_response:
                return self._handle_response(response, wait_async, async_request)
            return response

        raise Exception('Failed to perform request against all API URLs')

    def _handle_response(self, response: requests.models.Response, wait_async: bool, async_request: bool) -> Union[list, dict]:
        if 199 < response.status_code < 300:
            if response.json().get('error'):
                error_message = response.json().get('errorMessage')
                raise Exception(f'error: {error_message}')

            if wait_async:
                response_json = response.json()

                if async_request:
                    return response_json
                else:
                    return self._wait_request_archive(response_json['id']).get('data', [])
            else:
                return response.json().get('data', [])

        raise Exception(f'Response status code: {response.status_code}')

    def _wait_request_archive(self, request_id: str) -> dict:
        ttl = self._max_ttl / self._requests_pause

        while ttl > 0:
            ttl -= 1

            sleep(self._requests_pause)

            try:
                result = self._get_archive(request_id)
            except:
                sleep(self._requests_pause)
                result = self._get_archive(request_id)

            if result['status'] != 'Pending': return result

        raise Exception('Timeout exceeded')

    def _get_archive(self, request_id: str) -> dict:
        response = self.api_request('GET', f'/requests/{request_id}', use_handle_response=False, wait_async=False, async_request=False)
        if 199 < response.status_code < 300:
            return response.json()
        raise Exception(f'Response status code: {response.status_code}')
