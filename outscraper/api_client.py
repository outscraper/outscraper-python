import requests
from time import sleep
from typing import Union, Tuple

from .utils import as_list, parse_fields


class ApiClient(object):
    """Outscraper ApiClient - Python SDK that allows using Outscraper's services and Outscraper's API.
    ```python
    from outscraper import ApiClient
    cliet = ApiClient(api_key='SECRET_API_KEY')
    maps_results = cliet.google_maps_search('restaurants brooklyn usa')
    search_results = cliet.google_search('bitcoin')
    ```
    https://github.com/outscraper/outscraper-python
    """

    _api_url = 'https://api.app.outscraper.com'
    _api_headers = {}

    _max_ttl = 60 * 60
    _requests_pause = 5

    def __init__(self, api_key: str, requests_pause: int = 5) -> None:
        self._api_headers = {
            'X-API-KEY': api_key,
            'client': f'Python SDK'
        }
        self._requests_pause = requests_pause

    def get_tasks(self, query: str = '', last_id: str = '', page_size: int = 10) -> Tuple[list, bool]:
        '''
            Fetch user UI tasks.

                    Parameters:
                            query (str): parameter specifies the search query (tag).
                            last_id (str): parameter specifies the last task ID. It's commonly used in pagination.
                            page_size (int): parameter specifies the number of items to return.

                    Returns:
                            list: requests history

            See: https://app.outscraper.com/api-docs#tag/Outscraper-Platform-UI/paths/~1tasks/get
        '''
        response = requests.get(f'{self._api_url}/tasks?query={query}&lastId={last_id}&pageSize={page_size}', headers=self._api_headers)

        if 199 < response.status_code < 300:
            data = response.json()

            if 'errorMessage' in data:
                raise Exception(f'Error: {data["errorMessage"]}')

            return data['tasks'], data['has_more']

        raise Exception(f'Response status code: {response.status_code}')

    def get_requests_history(self, type: str = 'running', skip: int = 0, page_size: int = 25) -> list:
        '''
            Fetch up to 100 of your last requests.

                    Parameters:
                            type (str): parameter allows you to filter requests by type (running/finished).
                            skip (int): skip first N records. It's commonly used in pagination.
                            page_size (int): parameter specifies the number of items to return.

                    Returns:
                            list: requests history

            See: https://app.outscraper.com/api-docs#tag/Requests/paths/~1requests/get
        '''
        response = requests.get(f'{self._api_url}/requests?type={type}&skip={skip}&pageSize={page_size}', headers=self._api_headers)

        if 199 < response.status_code < 300:
            return response.json()

        raise Exception(f'Response status code: {response.status_code}')

    def get_request_archive(self, request_id: str) -> dict:
        '''
            Fetch request data from archive

                    Parameters:
                            request_id (int): unique id for the request provided by ['id']

                    Returns:
                            dict: result from the archive

            See: https://app.outscraper.com/api-docs#tag/Requests/paths/~1requests~1{requestId}/get
        '''
        response = requests.get(f'{self._api_url}/requests/{request_id}')

        if 199 < response.status_code < 300:
            return response.json()

        raise Exception(f'Response status code: {response.status_code}')

    def _handle_response(self, response: requests.models.Response, wait_async: bool = False, async_request: bool = False) -> Union[list, dict]:
        if 199 < response.status_code < 300:
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
                result = self.get_request_archive(request_id)
            except:
                sleep(self._requests_pause)
                result = self.get_request_archive(request_id)

            if result['status'] != 'Pending': return result

        raise Exception('Timeout exceeded')

    def google_search(self, query: Union[list, str], pages_per_query: int = 1, uule: str = None, language: str = 'en', region: str = None,
        fields: Union[list, str] = None, async_request: bool = False
    ) -> Union[list, dict]:
        '''
            Get data from Google search

                    Parameters:
                            query (list | str): parameter defines the query or queries you want to search on Google. Using a lists allows multiple queries (up to 50) to be sent in one request and save on network latency time.
                            pages_per_query (int): parameter specifies the limit of pages to return from one query.
                            uule (str): Google UULE parameter is used to encode a place or an exact location (with latitude and longitude) into a code. By using it you can see a Google result page like someone located at the specified location.
                            language (str): parameter specifies the language to use for Google. Available values: "en", "de", "es", "es-419", "fr", "hr", "it", "nl", "pl", "pt-BR", "pt-PT", "vi", "tr", "ru", "ar", "th", "ko", "zh-CN", "zh-TW", "ja", "ach", "af", "ak", "ig", "az", "ban", "ceb", "xx-bork", "bs", "br", "ca", "cs", "sn", "co", "cy", "da", "yo", "et", "xx-elmer", "eo", "eu", "ee", "tl", "fil", "fo", "fy", "gaa", "ga", "gd", "gl", "gn", "xx-hacker", "ht", "ha", "haw", "bem", "rn", "id", "ia", "xh", "zu", "is", "jw", "rw", "sw", "tlh", "kg", "mfe", "kri", "la", "lv", "to", "lt", "ln", "loz", "lua", "lg", "hu", "mg", "mt", "mi", "ms", "pcm", "no", "nso", "ny", "nn", "uz", "oc", "om", "xx-pirate", "ro", "rm", "qu", "nyn", "crs", "sq", "sk", "sl", "so", "st", "sr-ME", "sr-Latn", "su", "fi", "sv", "tn", "tum", "tk", "tw", "wo", "el", "be", "bg", "ky", "kk", "mk", "mn", "sr", "tt", "tg", "uk", "ka", "hy", "yi", "iw", "ug", "ur", "ps", "sd", "fa", "ckb", "ti", "am", "ne", "mr", "hi", "bn", "pa", "gu", "or", "ta", "te", "kn", "ml", "si", "lo", "my", "km", "chr".
                            region (str): parameter specifies the region to use for Google. Available values: "AF", "AL", "DZ", "AS", "AD", "AO", "AI", "AG", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BY", "BE", "BZ", "BJ", "BT", "BO", "BA", "BW", "BR", "VG", "BN", "BG", "BF", "BI", "KH", "CM", "CA", "CV", "CF", "TD", "CL", "CN", "CO", "CG", "CD", "CK", "CR", "CI", "HR", "CU", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "EE", "ET", "FJ", "FI", "FR", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GT", "GG", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KW", "KG", "LA", "LV", "LB", "LS", "LY", "LI", "LT", "LU", "MG", "MW", "MY", "MV", "ML", "MT", "MU", "MX", "FM", "MD", "MN", "ME", "MS", "MA", "MZ", "MM", "NA", "NR", "NP", "NL", "NZ", "NI", "NE", "NG", "NU", "MK", "NO", "OM", "PK", "PS", "PA", "PG", "PY", "PE", "PH", "PN", "PL", "PT", "PR", "QA", "RO", "RU", "RW", "WS", "SM", "ST", "SA", "SN", "RS", "SC", "SL", "SG", "SK", "SI", "SB", "SO", "ZA", "KR", "ES", "LK", "SH", "VC", "SR", "SE", "CH", "TW", "TJ", "TZ", "TH", "TL", "TG", "TO", "TT", "TN", "TR", "TM", "VI", "UG", "UA", "AE", "GB", "US", "UY", "UZ", "VU", "VE", "VN", "ZM", "ZW".
                            fields (list | str): parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.
                            async_request (bool): parameter defines the way you want to submit your task to Outscraper. It can be set to `False` (default) to send a task and wait until you got your results, or `True` to submit your task and retrieve the results later using a request ID with `get_request_archive`. Each response is available for `2` hours after a request has been completed.

                    Returns:
                            list: json result

            See: https://app.outscraper.com/api-docs#tag/Google/paths/~1google-search-v3/get
        '''
        queries = as_list(query)
        wait_async = async_request or (len(queries) > 1 or pages_per_query > 1)

        response = requests.get(f'{self._api_url}/google-search-v3', params={
            'query': queries,
            'pagesPerQuery': pages_per_query,
            'uule': uule,
            'language': language,
            'region': region,
            'async': async_request,
            'fields': parse_fields(fields),
        }, headers=self._api_headers)

        return self._handle_response(response, wait_async, async_request)

    def google_search_news(self, query: Union[list, str], pages_per_query: int = 1, uule: str = None, tbs: str = None, language: str = 'en', region: str = None, fields: Union[list, str] = None) -> list:
        '''
            Returns search results from Google based on a given search query (or many queries).

                    Parameters:
                            query (list | str): parameter defines the query or queries you want to search news on Google. Using a lists allows multiple queries (up to 50) to be sent in one request and save on network latency time.
                            pages_per_query (int): parameter specifies the limit of pages to return from one query.
                            uule (str): Google UULE parameter is used to encode a place or an exact location (with latitude and longitude) into a code. By using it you can see a Google result page like someone located at the specified location.
                            tbs: parameter specifies the date range of the results (h - past hour, d - past 24 hours, w - past week, m - past month, 'y' - past year).
                            language (str): parameter specifies the language to use for Google. Available values: "en", "de", "es", "es-419", "fr", "hr", "it", "nl", "pl", "pt-BR", "pt-PT", "vi", "tr", "ru", "ar", "th", "ko", "zh-CN", "zh-TW", "ja", "ach", "af", "ak", "ig", "az", "ban", "ceb", "xx-bork", "bs", "br", "ca", "cs", "sn", "co", "cy", "da", "yo", "et", "xx-elmer", "eo", "eu", "ee", "tl", "fil", "fo", "fy", "gaa", "ga", "gd", "gl", "gn", "xx-hacker", "ht", "ha", "haw", "bem", "rn", "id", "ia", "xh", "zu", "is", "jw", "rw", "sw", "tlh", "kg", "mfe", "kri", "la", "lv", "to", "lt", "ln", "loz", "lua", "lg", "hu", "mg", "mt", "mi", "ms", "pcm", "no", "nso", "ny", "nn", "uz", "oc", "om", "xx-pirate", "ro", "rm", "qu", "nyn", "crs", "sq", "sk", "sl", "so", "st", "sr-ME", "sr-Latn", "su", "fi", "sv", "tn", "tum", "tk", "tw", "wo", "el", "be", "bg", "ky", "kk", "mk", "mn", "sr", "tt", "tg", "uk", "ka", "hy", "yi", "iw", "ug", "ur", "ps", "sd", "fa", "ckb", "ti", "am", "ne", "mr", "hi", "bn", "pa", "gu", "or", "ta", "te", "kn", "ml", "si", "lo", "my", "km", "chr".
                            region (str): parameter specifies the region to use for Google. Available values: "AF", "AL", "DZ", "AS", "AD", "AO", "AI", "AG", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BY", "BE", "BZ", "BJ", "BT", "BO", "BA", "BW", "BR", "VG", "BN", "BG", "BF", "BI", "KH", "CM", "CA", "CV", "CF", "TD", "CL", "CN", "CO", "CG", "CD", "CK", "CR", "CI", "HR", "CU", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "EE", "ET", "FJ", "FI", "FR", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GT", "GG", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KW", "KG", "LA", "LV", "LB", "LS", "LY", "LI", "LT", "LU", "MG", "MW", "MY", "MV", "ML", "MT", "MU", "MX", "FM", "MD", "MN", "ME", "MS", "MA", "MZ", "MM", "NA", "NR", "NP", "NL", "NZ", "NI", "NE", "NG", "NU", "MK", "NO", "OM", "PK", "PS", "PA", "PG", "PY", "PE", "PH", "PN", "PL", "PT", "PR", "QA", "RO", "RU", "RW", "WS", "SM", "ST", "SA", "SN", "RS", "SC", "SL", "SG", "SK", "SI", "SB", "SO", "ZA", "KR", "ES", "LK", "SH", "VC", "SR", "SE", "CH", "TW", "TJ", "TZ", "TH", "TL", "TG", "TO", "TT", "TN", "TR", "TM", "VI", "UG", "UA", "AE", "GB", "US", "UY", "UZ", "VU", "VE", "VN", "ZM", "ZW".
                            fields (list | str): parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.

                    Returns:
                            list: json result

            See: https://app.outscraper.com/api-docs#tag/Google/paths/~1google-search-news/get
        '''
        response = requests.get(f'{self._api_url}/google-search-news', params={
            'query': as_list(query),
            'pagesPerQuery': pages_per_query,
            'uule': uule,
            'tbs': tbs,
            'language': language,
            'region': region,
            'fields': parse_fields(fields),
        }, headers=self._api_headers)

        if 199 < response.status_code < 300:
            return self._wait_request_archive(response.json()['id']).get('data', [])

        raise Exception(f'Response status code: {response.status_code}')

    def google_maps_search_v1(self, query: Union[list, str], limit: int = 500, extract_contacts: bool = False, drop_duplicates: bool = False,
        coordinates: str = None, language: str = 'en', region: str = None, fields: Union[list, str] = None
    ) -> list:
        '''
            Get Google Maps Data (old verison)

            Returns places from Google Maps based on a given search query (or many queries).
            The results from searches are the same as you would see by visiting a regular Google Maps site. However, in most cases, it's recommended to use locations inside queries (e.g., bars, NY, USA) as the IP addresses of Outscraper's servers might be located in different countries.

                    Parameters:
                            query (list | str): parameter defines the query you want to search. You can use anything that you would use on a regular Google Maps site. Additionally, you can use google_id, place_id or urls to Google Maps places. Using a lists allows multiple queries (up to 50) to be sent in one request and save on network latency time.
                            limit (int): parameter specifies the limit of places to take from one query search. The same as on Google Maps site, there are no more than 400 organizations per one query search. Use more precise categories (e.g., Asian restaurant, Italian restaurant) and/or locations (e.g., restaurants, Brooklyn 11211, restaurants, Brooklyn 11215) to overcome this limitation.
                            extract_contacts (bool): parameter specifies whether the bot will scrape additional data (emails, social links, site keywords…) from companies’ websites. It increases the time of the extraction.
                            drop_duplicates (bool): parameter specifies whether the bot will drop the same organizations from different queries. Using the parameter combines results from each query inside one big array.
                            coordinates (str): parameter defines the coordinates to use along with the query. Example: "@41.3954381,2.1628662,15.1z".
                            language (str): parameter specifies the language to use for Google. Available values: "en", "de", "es", "es-419", "fr", "hr", "it", "nl", "pl", "pt-BR", "pt-PT", "vi", "tr", "ru", "ar", "th", "ko", "zh-CN", "zh-TW", "ja", "ach", "af", "ak", "ig", "az", "ban", "ceb", "xx-bork", "bs", "br", "ca", "cs", "sn", "co", "cy", "da", "yo", "et", "xx-elmer", "eo", "eu", "ee", "tl", "fil", "fo", "fy", "gaa", "ga", "gd", "gl", "gn", "xx-hacker", "ht", "ha", "haw", "bem", "rn", "id", "ia", "xh", "zu", "is", "jw", "rw", "sw", "tlh", "kg", "mfe", "kri", "la", "lv", "to", "lt", "ln", "loz", "lua", "lg", "hu", "mg", "mt", "mi", "ms", "pcm", "no", "nso", "ny", "nn", "uz", "oc", "om", "xx-pirate", "ro", "rm", "qu", "nyn", "crs", "sq", "sk", "sl", "so", "st", "sr-ME", "sr-Latn", "su", "fi", "sv", "tn", "tum", "tk", "tw", "wo", "el", "be", "bg", "ky", "kk", "mk", "mn", "sr", "tt", "tg", "uk", "ka", "hy", "yi", "iw", "ug", "ur", "ps", "sd", "fa", "ckb", "ti", "am", "ne", "mr", "hi", "bn", "pa", "gu", "or", "ta", "te", "kn", "ml", "si", "lo", "my", "km", "chr".
                            region (str): parameter specifies the region to use for Google. Available values: "AF", "AL", "DZ", "AS", "AD", "AO", "AI", "AG", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BY", "BE", "BZ", "BJ", "BT", "BO", "BA", "BW", "BR", "VG", "BN", "BG", "BF", "BI", "KH", "CM", "CA", "CV", "CF", "TD", "CL", "CN", "CO", "CG", "CD", "CK", "CR", "CI", "HR", "CU", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "EE", "ET", "FJ", "FI", "FR", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GT", "GG", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KW", "KG", "LA", "LV", "LB", "LS", "LY", "LI", "LT", "LU", "MG", "MW", "MY", "MV", "ML", "MT", "MU", "MX", "FM", "MD", "MN", "ME", "MS", "MA", "MZ", "MM", "NA", "NR", "NP", "NL", "NZ", "NI", "NE", "NG", "NU", "MK", "NO", "OM", "PK", "PS", "PA", "PG", "PY", "PE", "PH", "PN", "PL", "PT", "PR", "QA", "RO", "RU", "RW", "WS", "SM", "ST", "SA", "SN", "RS", "SC", "SL", "SG", "SK", "SI", "SB", "SO", "ZA", "KR", "ES", "LK", "SH", "VC", "SR", "SE", "CH", "TW", "TJ", "TZ", "TH", "TL", "TG", "TO", "TT", "TN", "TR", "TM", "VI", "UG", "UA", "AE", "GB", "US", "UY", "UZ", "VU", "VE", "VN", "ZM", "ZW".
                            fields (list | str): parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.

                    Returns:
                            list: json result

            See: https://app.outscraper.com/api-docs#tag/Google/paths/~1maps~1search/get
        '''
        response = requests.get(f'{self._api_url}/maps/search', params={
            'query': as_list(query),
            'coordinates': coordinates,
            'language': language,
            'region': region,
            'organizationsPerQueryLimit': limit,
            'extractContacts': extract_contacts,
            'dropDuplicates': drop_duplicates,
            'fields': parse_fields(fields),
        }, headers=self._api_headers)

        if 199 < response.status_code < 300:
            return self._wait_request_archive(response.json()['id']).get('data', [])

        raise Exception(f'Response status code: {response.status_code}')

    def google_maps_search(self, query: Union[list, str], limit: int = 20, drop_duplicates: bool = False,
        language: str = 'en', region: str = None, skip: int = 0, coordinates: str = None,
        enrichment: list = None, fields: Union[list, str] = None,
        async_request: bool = False, ui: bool = None, webhook: bool = None
    ) -> Union[list, dict]:
        '''
            Get Google Maps Data V3 (speed optimized endpoint for real time data)

            Returns places from Google Maps based on a given search query (or many queries).
            The results from searches are the same as you would see by visiting a regular Google Maps site. However, in most cases, it's recommended to use locations inside queries (e.g., bars, NY, USA) as the IP addresses of Outscraper's servers might be located in different countries.
            This endpoint is optimized for fast responses and can be used as real time API. Set the limit parameter to 20 to achieve the maximum response speed.

                    Parameters:
                            query (list | str): parameter defines the query you want to search. You can use anything that you would use on a regular Google Maps site. Additionally, you can use google_id. The example of valid queries: Real estate agency, Rome, Italy, The NoMad Restaurant, NY, USA, restaurants, Brooklyn 11203, 0x886916e8bc273979:0x5141fcb11460b226, etc. Using a lists allows multiple queries (up to 50) to be sent in one request and save on network latency time.
                            limit (int): parameter specifies the limit of places to take from one query search. The same as on Google Maps site, there are no more than 400 organizations per one query search. Use more precise categories (e.g., Asian restaurant, Italian restaurant) and/or locations (e.g., restaurants, Brooklyn 11211, restaurants, Brooklyn 11215) to overcome this limitation.
                            drop_duplicates (bool): parameter specifies whether the bot will drop the same organizations from different queries. Using the parameter combines results from each query inside one big array.
                            language (str): parameter specifies the language to use for Google. Available values: "en", "de", "es", "es-419", "fr", "hr", "it", "nl", "pl", "pt-BR", "pt-PT", "vi", "tr", "ru", "ar", "th", "ko", "zh-CN", "zh-TW", "ja", "ach", "af", "ak", "ig", "az", "ban", "ceb", "xx-bork", "bs", "br", "ca", "cs", "sn", "co", "cy", "da", "yo", "et", "xx-elmer", "eo", "eu", "ee", "tl", "fil", "fo", "fy", "gaa", "ga", "gd", "gl", "gn", "xx-hacker", "ht", "ha", "haw", "bem", "rn", "id", "ia", "xh", "zu", "is", "jw", "rw", "sw", "tlh", "kg", "mfe", "kri", "la", "lv", "to", "lt", "ln", "loz", "lua", "lg", "hu", "mg", "mt", "mi", "ms", "pcm", "no", "nso", "ny", "nn", "uz", "oc", "om", "xx-pirate", "ro", "rm", "qu", "nyn", "crs", "sq", "sk", "sl", "so", "st", "sr-ME", "sr-Latn", "su", "fi", "sv", "tn", "tum", "tk", "tw", "wo", "el", "be", "bg", "ky", "kk", "mk", "mn", "sr", "tt", "tg", "uk", "ka", "hy", "yi", "iw", "ug", "ur", "ps", "sd", "fa", "ckb", "ti", "am", "ne", "mr", "hi", "bn", "pa", "gu", "or", "ta", "te", "kn", "ml", "si", "lo", "my", "km", "chr".
                            region (str): parameter specifies the region to use for Google. Available values: "AF", "AL", "DZ", "AS", "AD", "AO", "AI", "AG", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BY", "BE", "BZ", "BJ", "BT", "BO", "BA", "BW", "BR", "VG", "BN", "BG", "BF", "BI", "KH", "CM", "CA", "CV", "CF", "TD", "CL", "CN", "CO", "CG", "CD", "CK", "CR", "CI", "HR", "CU", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "EE", "ET", "FJ", "FI", "FR", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GT", "GG", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KW", "KG", "LA", "LV", "LB", "LS", "LY", "LI", "LT", "LU", "MG", "MW", "MY", "MV", "ML", "MT", "MU", "MX", "FM", "MD", "MN", "ME", "MS", "MA", "MZ", "MM", "NA", "NR", "NP", "NL", "NZ", "NI", "NE", "NG", "NU", "MK", "NO", "OM", "PK", "PS", "PA", "PG", "PY", "PE", "PH", "PN", "PL", "PT", "PR", "QA", "RO", "RU", "RW", "WS", "SM", "ST", "SA", "SN", "RS", "SC", "SL", "SG", "SK", "SI", "SB", "SO", "ZA", "KR", "ES", "LK", "SH", "VC", "SR", "SE", "CH", "TW", "TJ", "TZ", "TH", "TL", "TG", "TO", "TT", "TN", "TR", "TM", "VI", "UG", "UA", "AE", "GB", "US", "UY", "UZ", "VU", "VE", "VN", "ZM", "ZW".
                            skip (int): skip first N places, where N should be multiple to 20 (e.g. 0, 20, 40). It's commonly used in pagination.
                            coordinates (str): parameter defines the coordinates of the location where you want your query to be applied. It has to be constructed in the next sequence: "latitude" + "," + "longitude" (e.g. "41.3954381,2.1628662").
                            enrichment (list): parameter defines enrichments you want to apply to the results. Available values: "domains_service", "emails_validator_service", "disposable_email_checker", "whatsapp_checker", "imessage_checker", "phones_enricher_service", "trustpilot_service", "companies_data".
                            fields (list | str): parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.
                            async_request (bool): parameter defines the way you want to submit your task to Outscraper. It can be set to `False` (default) to send a task and wait until you got your results, or `True` to submit your task and retrieve the results later using a request ID with `get_request_archive`. Each response is available for `2` hours after a request has been completed.
                            ui (bool): parameter defines whether a task will be executed as a UI task. This is commonly used when you want to create a regular platform task with API. Using this parameter overwrites the async_request parameter to `True`.

                    Returns:
                            list: json result

            See: https://app.outscraper.com/api-docs#tag/Google/paths/~1maps~1search-v3/get
        '''
        queries = as_list(query)
        wait_async = async_request or (len(queries) > 10 and limit > 1)

        response = requests.get(f'{self._api_url}/maps/search-v3', params={
            'query': queries,
            'language': language,
            'region': region,
            'organizationsPerQueryLimit': limit,
            'skipPlaces': skip,
            'coordinates': coordinates,
            'dropDuplicates': drop_duplicates,
            'async': wait_async,
            'enrichment': as_list(enrichment) if enrichment else '',
            'fields': parse_fields(fields),
            'ui': ui,
            'webhook': webhook,
        }, headers=self._api_headers)

        return self._handle_response(response, wait_async, async_request)

    def google_maps_directions(self, query: Union[list, str], departure_time: int = None, finish_time: int = None, interval: int = 60,
        language: str = 'en', region: str = None, async_request: bool = False, fields: Union[list, str] = None
    ) -> list:
        '''
            Get Google Maps Directions

            Returns directions between two points from Google Maps.

                    Parameters:
                            query (list | str): parameter defines the query that should contains "<origin> + <4 spaces> + <destination>". Using a lists allows multiple queries (up to 50) to be sent in one request and save on network latency time.
                            departure_time (int): parameter specifies the departure timestamp. The current timestamp is used when the value is not provided.
                            finish_time (int): parameter specifies the end departure timestamp. Using this parameter requires using the interval parameter.
                            interval (int): parameter specifies the interval to use between departure_time and finish_time.
                            language (str): parameter specifies the language to use for Google. Available values: "en", "de", "es", "es-419", "fr", "hr", "it", "nl", "pl", "pt-BR", "pt-PT", "vi", "tr", "ru", "ar", "th", "ko", "zh-CN", "zh-TW", "ja", "ach", "af", "ak", "ig", "az", "ban", "ceb", "xx-bork", "bs", "br", "ca", "cs", "sn", "co", "cy", "da", "yo", "et", "xx-elmer", "eo", "eu", "ee", "tl", "fil", "fo", "fy", "gaa", "ga", "gd", "gl", "gn", "xx-hacker", "ht", "ha", "haw", "bem", "rn", "id", "ia", "xh", "zu", "is", "jw", "rw", "sw", "tlh", "kg", "mfe", "kri", "la", "lv", "to", "lt", "ln", "loz", "lua", "lg", "hu", "mg", "mt", "mi", "ms", "pcm", "no", "nso", "ny", "nn", "uz", "oc", "om", "xx-pirate", "ro", "rm", "qu", "nyn", "crs", "sq", "sk", "sl", "so", "st", "sr-ME", "sr-Latn", "su", "fi", "sv", "tn", "tum", "tk", "tw", "wo", "el", "be", "bg", "ky", "kk", "mk", "mn", "sr", "tt", "tg", "uk", "ka", "hy", "yi", "iw", "ug", "ur", "ps", "sd", "fa", "ckb", "ti", "am", "ne", "mr", "hi", "bn", "pa", "gu", "or", "ta", "te", "kn", "ml", "si", "lo", "my", "km", "chr".
                            region (str): parameter specifies the region to use for Google. Available values: "AF", "AL", "DZ", "AS", "AD", "AO", "AI", "AG", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BY", "BE", "BZ", "BJ", "BT", "BO", "BA", "BW", "BR", "VG", "BN", "BG", "BF", "BI", "KH", "CM", "CA", "CV", "CF", "TD", "CL", "CN", "CO", "CG", "CD", "CK", "CR", "CI", "HR", "CU", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "EE", "ET", "FJ", "FI", "FR", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GT", "GG", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KW", "KG", "LA", "LV", "LB", "LS", "LY", "LI", "LT", "LU", "MG", "MW", "MY", "MV", "ML", "MT", "MU", "MX", "FM", "MD", "MN", "ME", "MS", "MA", "MZ", "MM", "NA", "NR", "NP", "NL", "NZ", "NI", "NE", "NG", "NU", "MK", "NO", "OM", "PK", "PS", "PA", "PG", "PY", "PE", "PH", "PN", "PL", "PT", "PR", "QA", "RO", "RU", "RW", "WS", "SM", "ST", "SA", "SN", "RS", "SC", "SL", "SG", "SK", "SI", "SB", "SO", "ZA", "KR", "ES", "LK", "SH", "VC", "SR", "SE", "CH", "TW", "TJ", "TZ", "TH", "TL", "TG", "TO", "TT", "TN", "TR", "TM", "VI", "UG", "UA", "AE", "GB", "US", "UY", "UZ", "VU", "VE", "VN", "ZM", "ZW".
                            fields (list | str): parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.

                    Returns:
                            list: json result

            See: https://app.outscraper.com/api-docs#tag/Google/paths/~1maps~1directions/get
        '''
        response = requests.get(f'{self._api_url}/maps/directions', params={
            'query': as_list(query),
            'departure_time': departure_time,
            'interval': interval,
            'finish_time': finish_time,
            'language': language,
            'region': region,
            'async': async_request,
            'fields': parse_fields(fields),
        }, headers=self._api_headers)

        if 199 < response.status_code < 300:
            if async_request:
                return response.json()

            return self._wait_request_archive(response.json()['id']).get('data', [])

        raise Exception(f'Response status code: {response.status_code}')

    def google_maps_reviews_v2(self, query: Union[list, str], reviews_limit: int = 100, limit: int = 1, sort: str = 'most_relevant',
        skip: int = 0, start: int = None, cutoff: int = None, cutoff_rating: int = None, ignore_empty: bool = False,
        coordinates: str = None, language: str = 'en', region: str = None, fields: Union[list, str] = None
    ) -> list:
        '''
            Get Google Maps Reviews (old verison)

            Returns Google Maps reviews from places when using search queries (e.g., restaurants, Manhattan, NY, USA) or from a single place when using IDs or names (e.g., NoMad Restaurant, NY, USA, 0x886916e8bc273979:0x5141fcb11460b226, ChIJu7bMNFV-54gR-lrHScvPRX4).
            Places information will be returned as well in the case at least one review is found.

                    Parameters:
                            query (list | str): parameter defines the query you want to search. You can use anything that you would use on a regular Google Maps site. Additionally, you can use google_id, place_id or urls to Google Maps places. Using a lists allows multiple queries (up to 50) to be sent in one request and save on network latency time.
                            reviews_limit (int): parameter specifies the limit of reviews to extract from one place.
                            limit (str): parameter specifies the limit of places to take from one query search.
                            sort (str): parameter specifies one of the sorting types. Available values: "most_relevant", "newest", "highest_rating", "lowest_rating".
                            skip (int): parameter specifies the number of items to skip. It's commonly used in pagination.
                            start (int): parameter specifies the start timestamp value for reviews (newest review). The current timestamp is used when the value is not provided. Using the start parameter overwrites sort parameter to newest.
                            cutoff (int): parameter specifies the maximum timestamp value for reviews (oldest). Using the cutoff parameter overwrites sort parameter to newest.
                            cutoff_rating (int): parameter specifies the maximum (for lowest_rating sorting) or minimum (for highest_rating sorting) rating for reviews. Using the cutoffRating requires sorting to be set to "lowest_rating" or "highest_rating".
                            ignore_empty (bool): parameter specifies whether to ignore reviews without text or not.
                            coordinates (str): parameter defines the coordinates of the location where you want your query to be applied. It has to be constructed in the next sequence: "@" + "latitude" + "," + "longitude" + "," + "zoom" (e.g. "@41.3954381,2.1628662,15.1z").
                            language (str): parameter specifies the language to use for Google. Available values: "en", "de", "es", "es-419", "fr", "hr", "it", "nl", "pl", "pt-BR", "pt-PT", "vi", "tr", "ru", "ar", "th", "ko", "zh-CN", "zh-TW", "ja", "ach", "af", "ak", "ig", "az", "ban", "ceb", "xx-bork", "bs", "br", "ca", "cs", "sn", "co", "cy", "da", "yo", "et", "xx-elmer", "eo", "eu", "ee", "tl", "fil", "fo", "fy", "gaa", "ga", "gd", "gl", "gn", "xx-hacker", "ht", "ha", "haw", "bem", "rn", "id", "ia", "xh", "zu", "is", "jw", "rw", "sw", "tlh", "kg", "mfe", "kri", "la", "lv", "to", "lt", "ln", "loz", "lua", "lg", "hu", "mg", "mt", "mi", "ms", "pcm", "no", "nso", "ny", "nn", "uz", "oc", "om", "xx-pirate", "ro", "rm", "qu", "nyn", "crs", "sq", "sk", "sl", "so", "st", "sr-ME", "sr-Latn", "su", "fi", "sv", "tn", "tum", "tk", "tw", "wo", "el", "be", "bg", "ky", "kk", "mk", "mn", "sr", "tt", "tg", "uk", "ka", "hy", "yi", "iw", "ug", "ur", "ps", "sd", "fa", "ckb", "ti", "am", "ne", "mr", "hi", "bn", "pa", "gu", "or", "ta", "te", "kn", "ml", "si", "lo", "my", "km", "chr".
                            region (str): parameter specifies the region to use for Google. Available values: "AF", "AL", "DZ", "AS", "AD", "AO", "AI", "AG", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BY", "BE", "BZ", "BJ", "BT", "BO", "BA", "BW", "BR", "VG", "BN", "BG", "BF", "BI", "KH", "CM", "CA", "CV", "CF", "TD", "CL", "CN", "CO", "CG", "CD", "CK", "CR", "CI", "HR", "CU", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "EE", "ET", "FJ", "FI", "FR", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GT", "GG", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KW", "KG", "LA", "LV", "LB", "LS", "LY", "LI", "LT", "LU", "MG", "MW", "MY", "MV", "ML", "MT", "MU", "MX", "FM", "MD", "MN", "ME", "MS", "MA", "MZ", "MM", "NA", "NR", "NP", "NL", "NZ", "NI", "NE", "NG", "NU", "MK", "NO", "OM", "PK", "PS", "PA", "PG", "PY", "PE", "PH", "PN", "PL", "PT", "PR", "QA", "RO", "RU", "RW", "WS", "SM", "ST", "SA", "SN", "RS", "SC", "SL", "SG", "SK", "SI", "SB", "SO", "ZA", "KR", "ES", "LK", "SH", "VC", "SR", "SE", "CH", "TW", "TJ", "TZ", "TH", "TL", "TG", "TO", "TT", "TN", "TR", "TM", "VI", "UG", "UA", "AE", "GB", "US", "UY", "UZ", "VU", "VE", "VN", "ZM", "ZW".
                            fields (list | str): parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.

                    Returns:
                            list: json result

            See: https://app.outscraper.com/api-docs#tag/Google/paths/~1maps~1reviews-v3/get
        '''
        response = requests.get(f'{self._api_url}/maps/reviews-v2', params={
            'query': as_list(query),
            'reviewsLimit': reviews_limit,
            'limit': limit,
            'sort': sort,
            'skip': skip,
            'start': start,
            'cutoff': cutoff,
            'cutoffRating': cutoff_rating,
            'ignoreEmpty': ignore_empty,
            'coordinates': coordinates,
            'language': language,
            'region': region,
            'fields': parse_fields(fields),
        }, headers=self._api_headers)

        if 199 < response.status_code < 300:
            return self._wait_request_archive(response.json()['id']).get('data', [])

        raise Exception(f'Response status code: {response.status_code}')

    def google_maps_reviews(self, query: Union[list, str], reviews_limit: int = 10, limit: int = 1, sort: str = 'most_relevant',
        start: int = None, cutoff: int = None, cutoff_rating: int = None, ignore_empty: bool = False, language: str = 'en',
        region: str = None, reviews_query: str = None, last_pagination_id: str = None, fields: Union[list, str] = None, async_request: bool = False,
        ui: bool = None, webhook: bool = None
    ) -> Union[list, dict]:
        '''
            Get Google Maps Reviews V3 (speed optimized endpoint for real time data)

            Returns Google Maps reviews from places when using search queries (e.g., restaurants, Manhattan, NY, USA) or from a single place when using Google IDs or names (e.g., NoMad Restaurant, NY, USA, 0x886916e8bc273979:0x5141fcb11460b226).
            Places information will be returned as well in the case at least one review is found.
            This endpoint is optimized for fast responses and can be used as real time API. Set the reviews_limit parameter to 10 to achieve the maximum response speed.

                    Parameters:
                            query (list | str): parameter defines the query you want to search. You can use anything that you would use on a regular Google Maps site. Additionally, you can use google_id, place_id or urls to Google Maps places. Using a lists allows multiple queries (up to 50) to be sent in one request and save on network latency time.
                            reviews_limit (int): parameter specifies the limit of reviews to extract from one place (0 - unlimited).
                            limit (str): parameter specifies the limit of places to take from one query search.
                            sort (str): parameter specifies one of the sorting types. Available values: "most_relevant", "newest", "highest_rating", "lowest_rating".
                            start (int): parameter specifies the start timestamp value for reviews (newest review). The current timestamp is used when the value is not provided. Using the start parameter overwrites sort parameter to newest.
                            cutoff (int): parameter specifies the maximum timestamp value for reviews (oldest review). Using the cutoff parameter overwrites sort parameter to newest.
                            cutoff_rating (int): parameter specifies the maximum (for lowest_rating sorting) or minimum (for highest_rating sorting) rating for reviews. Using the cutoffRating requires sorting to be set to "lowest_rating" or "highest_rating".
                            ignore_empty (bool): parameter specifies whether to ignore reviews without text or not.
                            last_pagination_id (str): parameter specifies the review_pagination_id of the last item. It's commonly used in pagination.
                            reviews_query (str): parameter specifies the query to search among the reviews (e.g. wow, amazing, horrible place).
                            coordinates (str): parameter defines the coordinates of the location where you want your query to be applied. It has to be constructed in the next sequence: "@" + "latitude" + "," + "longitude" + "," + "zoom" (e.g. "@41.3954381,2.1628662,15.1z").
                            language (str): parameter specifies the language to use for Google. Available values: "en", "de", "es", "es-419", "fr", "hr", "it", "nl", "pl", "pt-BR", "pt-PT", "vi", "tr", "ru", "ar", "th", "ko", "zh-CN", "zh-TW", "ja", "ach", "af", "ak", "ig", "az", "ban", "ceb", "xx-bork", "bs", "br", "ca", "cs", "sn", "co", "cy", "da", "yo", "et", "xx-elmer", "eo", "eu", "ee", "tl", "fil", "fo", "fy", "gaa", "ga", "gd", "gl", "gn", "xx-hacker", "ht", "ha", "haw", "bem", "rn", "id", "ia", "xh", "zu", "is", "jw", "rw", "sw", "tlh", "kg", "mfe", "kri", "la", "lv", "to", "lt", "ln", "loz", "lua", "lg", "hu", "mg", "mt", "mi", "ms", "pcm", "no", "nso", "ny", "nn", "uz", "oc", "om", "xx-pirate", "ro", "rm", "qu", "nyn", "crs", "sq", "sk", "sl", "so", "st", "sr-ME", "sr-Latn", "su", "fi", "sv", "tn", "tum", "tk", "tw", "wo", "el", "be", "bg", "ky", "kk", "mk", "mn", "sr", "tt", "tg", "uk", "ka", "hy", "yi", "iw", "ug", "ur", "ps", "sd", "fa", "ckb", "ti", "am", "ne", "mr", "hi", "bn", "pa", "gu", "or", "ta", "te", "kn", "ml", "si", "lo", "my", "km", "chr".
                            region (str): parameter specifies the region to use for Google. Available values: "AF", "AL", "DZ", "AS", "AD", "AO", "AI", "AG", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BY", "BE", "BZ", "BJ", "BT", "BO", "BA", "BW", "BR", "VG", "BN", "BG", "BF", "BI", "KH", "CM", "CA", "CV", "CF", "TD", "CL", "CN", "CO", "CG", "CD", "CK", "CR", "CI", "HR", "CU", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "EE", "ET", "FJ", "FI", "FR", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GT", "GG", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KW", "KG", "LA", "LV", "LB", "LS", "LY", "LI", "LT", "LU", "MG", "MW", "MY", "MV", "ML", "MT", "MU", "MX", "FM", "MD", "MN", "ME", "MS", "MA", "MZ", "MM", "NA", "NR", "NP", "NL", "NZ", "NI", "NE", "NG", "NU", "MK", "NO", "OM", "PK", "PS", "PA", "PG", "PY", "PE", "PH", "PN", "PL", "PT", "PR", "QA", "RO", "RU", "RW", "WS", "SM", "ST", "SA", "SN", "RS", "SC", "SL", "SG", "SK", "SI", "SB", "SO", "ZA", "KR", "ES", "LK", "SH", "VC", "SR", "SE", "CH", "TW", "TJ", "TZ", "TH", "TL", "TG", "TO", "TT", "TN", "TR", "TM", "VI", "UG", "UA", "AE", "GB", "US", "UY", "UZ", "VU", "VE", "VN", "ZM", "ZW".
                            fields (list | str): parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.
                            async_request (bool): parameter defines the way you want to submit your task to Outscraper. It can be set to `False` (default) to send a task and wait until you got your results, or `True` to submit your task and retrieve the results later using a request ID with `get_request_archive`. Each response is available for `2` hours after a request has been completed.
                            ui (bool): parameter defines whether a task will be executed as a UI task. This is commonly used when you want to create a regular platform task with API. Using this parameter overwrites the async_request parameter to `True`.

                    Returns:
                            list: json result

            See: https://app.outscraper.com/api-docs#tag/Google/paths/~1maps~1reviews-v3/get
        '''
        queries = as_list(query)
        wait_async = async_request or reviews_limit > 499 or reviews_limit == 0 or len(queries) > 10

        response = requests.get(f'{self._api_url}/maps/reviews-v3', params={
            'query': queries,
            'reviewsLimit': reviews_limit,
            'limit': limit,
            'sort': sort,
            'start': start,
            'cutoff': cutoff,
            'reviewsQuery': reviews_query,
            'lastPaginationId': last_pagination_id,
            'cutoffRating': cutoff_rating,
            'ignoreEmpty': ignore_empty,
            'language': language,
            'region': region,
            'async': wait_async,
            'fields': parse_fields(fields),
            'ui': ui,
            'webhook': webhook,
        }, headers=self._api_headers)

        return self._handle_response(response, wait_async, async_request)

    def google_maps_photos(self, query: Union[list, str], photosLimit: int = 100, limit: int = 1, tag: str = None,
        language: str = 'en', region: str = None, fields: Union[list, str] = None
    ) -> list:
        '''
            Get reviews from Google Maps

                    Parameters:
                            query (list | str): parameter defines the query you want to search. You can use anything that you would use on a regular Google Maps site. Additionally, you can use google_id, place_id or urls to Google Maps places. Using a lists allows multiple queries (up to 50) to be sent in one request and save on network latency time.
                            photosLimit (int): parameter specifies the limit of photos to extract from one place.
                            limit (str): parameter specifies the limit of places to take from one query search.
                            tag (str): parameter specifies one of the filtering types. Available values: "all", "latest", "menu", "by_owner".
                            language (str): parameter specifies the language to use for Google. Available values: "en", "de", "es", "es-419", "fr", "hr", "it", "nl", "pl", "pt-BR", "pt-PT", "vi", "tr", "ru", "ar", "th", "ko", "zh-CN", "zh-TW", "ja", "ach", "af", "ak", "ig", "az", "ban", "ceb", "xx-bork", "bs", "br", "ca", "cs", "sn", "co", "cy", "da", "yo", "et", "xx-elmer", "eo", "eu", "ee", "tl", "fil", "fo", "fy", "gaa", "ga", "gd", "gl", "gn", "xx-hacker", "ht", "ha", "haw", "bem", "rn", "id", "ia", "xh", "zu", "is", "jw", "rw", "sw", "tlh", "kg", "mfe", "kri", "la", "lv", "to", "lt", "ln", "loz", "lua", "lg", "hu", "mg", "mt", "mi", "ms", "pcm", "no", "nso", "ny", "nn", "uz", "oc", "om", "xx-pirate", "ro", "rm", "qu", "nyn", "crs", "sq", "sk", "sl", "so", "st", "sr-ME", "sr-Latn", "su", "fi", "sv", "tn", "tum", "tk", "tw", "wo", "el", "be", "bg", "ky", "kk", "mk", "mn", "sr", "tt", "tg", "uk", "ka", "hy", "yi", "iw", "ug", "ur", "ps", "sd", "fa", "ckb", "ti", "am", "ne", "mr", "hi", "bn", "pa", "gu", "or", "ta", "te", "kn", "ml", "si", "lo", "my", "km", "chr".
                            region (str): parameter specifies the region to use for Google. Available values: "AF", "AL", "DZ", "AS", "AD", "AO", "AI", "AG", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BY", "BE", "BZ", "BJ", "BT", "BO", "BA", "BW", "BR", "VG", "BN", "BG", "BF", "BI", "KH", "CM", "CA", "CV", "CF", "TD", "CL", "CN", "CO", "CG", "CD", "CK", "CR", "CI", "HR", "CU", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "EE", "ET", "FJ", "FI", "FR", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GT", "GG", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KW", "KG", "LA", "LV", "LB", "LS", "LY", "LI", "LT", "LU", "MG", "MW", "MY", "MV", "ML", "MT", "MU", "MX", "FM", "MD", "MN", "ME", "MS", "MA", "MZ", "MM", "NA", "NR", "NP", "NL", "NZ", "NI", "NE", "NG", "NU", "MK", "NO", "OM", "PK", "PS", "PA", "PG", "PY", "PE", "PH", "PN", "PL", "PT", "PR", "QA", "RO", "RU", "RW", "WS", "SM", "ST", "SA", "SN", "RS", "SC", "SL", "SG", "SK", "SI", "SB", "SO", "ZA", "KR", "ES", "LK", "SH", "VC", "SR", "SE", "CH", "TW", "TJ", "TZ", "TH", "TL", "TG", "TO", "TT", "TN", "TR", "TM", "VI", "UG", "UA", "AE", "GB", "US", "UY", "UZ", "VU", "VE", "VN", "ZM", "ZW".
                            fields (list | str): parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.

                    Returns:
                            list: json result

            See: https://app.outscraper.com/api-docs#tag/Google/paths/~1maps~1photos-v3/get
        '''
        response = requests.get(f'{self._api_url}/maps/photos-v3', params={
            'query': as_list(query),
            'photosLimit': photosLimit,
            'limit': limit,
            'tag': tag,
            'language': language,
            'region': region,
            'fields': parse_fields(fields),
        }, headers=self._api_headers)

        if 199 < response.status_code < 300:
            return self._wait_request_archive(response.json()['id']).get('data', [])

        raise Exception(f'Response status code: {response.status_code}')

    def google_maps_business_reviews(self, *args, **kwargs) -> list: # deprecated
        return self.google_maps_reviews(*args, **kwargs)

    def google_play_reviews(self, query: Union[list, str], reviews_limit: int = 100, sort: str = 'most_relevant', cutoff: int = None,
        rating: int = None, language: str = 'en', fields: Union[list, str] = None
    ) -> list:
        '''
            Returns reviews from any app/book/movie in the Google Play store.

                    Parameters:
                            query (list | str): you can use app IDs or direct links (e.g., https://play.google.com/store/apps/details?id=com.facebook.katana, com.facebook.katana). Using a lists allows multiple queries (up to 50) to be sent in one request and save on network latency time.
                            reviews_limit (int): parameter specifies the limit of reviews to extract from one query.
                            sort (str): parameter specifies one of the sorting types. Available values: "most_relevant", "newest", "rating".
                            cutoff (int): parameter specifies the maximum timestamp value for reviews. Using the cutoff parameter overwrites sort parameter to "newest".
                            rating (int): Filter by a specific rating. Works only with "sort=rating".
                            language (str): parameter specifies the language to use for Google. Available values: "en", "de", "es", "es-419", "fr", "hr", "it", "nl", "pl", "pt-BR", "pt-PT", "vi", "tr", "ru", "ar", "th", "ko", "zh-CN", "zh-TW", "ja", "ach", "af", "ak", "ig", "az", "ban", "ceb", "xx-bork", "bs", "br", "ca", "cs", "sn", "co", "cy", "da", "yo", "et", "xx-elmer", "eo", "eu", "ee", "tl", "fil", "fo", "fy", "gaa", "ga", "gd", "gl", "gn", "xx-hacker", "ht", "ha", "haw", "bem", "rn", "id", "ia", "xh", "zu", "is", "jw", "rw", "sw", "tlh", "kg", "mfe", "kri", "la", "lv", "to", "lt", "ln", "loz", "lua", "lg", "hu", "mg", "mt", "mi", "ms", "pcm", "no", "nso", "ny", "nn", "uz", "oc", "om", "xx-pirate", "ro", "rm", "qu", "nyn", "crs", "sq", "sk", "sl", "so", "st", "sr-ME", "sr-Latn", "su", "fi", "sv", "tn", "tum", "tk", "tw", "wo", "el", "be", "bg", "ky", "kk", "mk", "mn", "sr", "tt", "tg", "uk", "ka", "hy", "yi", "iw", "ug", "ur", "ps", "sd", "fa", "ckb", "ti", "am", "ne", "mr", "hi", "bn", "pa", "gu", "or", "ta", "te", "kn", "ml", "si", "lo", "my", "km", "chr".
                            fields (list | str): parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.

                    Returns:
                            list: json result

            See: https://app.outscraper.com/api-docs#tag/Google-Play/paths/~1google-play~1reviews/get
        '''
        response = requests.get(f'{self._api_url}/google-play/reviews', params={
            'query': as_list(query),
            'limit': reviews_limit,
            'sort': sort,
            'cutoff': cutoff,
            'rating': rating,
            'language': language,
            'fields': parse_fields(fields),
        }, headers=self._api_headers)

        if 199 < response.status_code < 300:
            return self._wait_request_archive(response.json()['id']).get('data', [])

        raise Exception(f'Response status code: {response.status_code}')

    def emails_and_contacts(self, query: Union[list, str], fields: Union[list, str] = None) -> list:
        '''
            Return email addresses, social links and phones from domains in seconds.

                    Parameters:
                            query (list | str): Domains or links (e.g., outscraper.com).
                            fields (list | str): Parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.

                    Returns:
                            list: json result

            See: https://app.outscraper.com/api-docs#tag/Email-Related/paths/~1emails-and-contacts/get
        '''
        response = requests.get(f'{self._api_url}/emails-and-contacts', params={
            'query': as_list(query),
            'fields': parse_fields(fields),
        }, headers=self._api_headers)

        if 199 < response.status_code < 300:
            return self._wait_request_archive(response.json()['id']).get('data', [])

        raise Exception(f'Response status code: {response.status_code}')

    def phones_enricher(self, query: Union[list, str], fields: Union[list, str] = None) -> list:
        '''
            Returns phones carrier data (name/type), validates phones, ensures messages deliverability.

                    Parameters:
                            query (list | str): Phone number (e.g., +1 281 236 8208).
                            fields (list | str): parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.

                    Returns:
                            list: json result

            See: https://app.outscraper.com/api-docs#tag/Phone-Related/paths/~1phones-enricher/get
        '''
        response = requests.get(f'{self._api_url}/phones-enricher', params={
            'query': as_list(query),
            'fields': parse_fields(fields),
        }, headers=self._api_headers)

        if 199 < response.status_code < 300:
            return self._wait_request_archive(response.json()['id']).get('data', [])

        raise Exception(f'Response status code: {response.status_code}')

    def amazon_products(self, query: Union[list, str], limit: int = 24, fields: Union[list, str] = None, async_request: bool = False,
        ui: bool = None, webhook: bool = None
    ) -> Union[list, dict]:
        '''
            Amazon Products V2 (speed optimized)

            Returns information about products on Amazon.

                    Parameters:
                            query (list | str): Amazon product or summary pages URLs.
                            limit (int): The parameter specifies the limit of products to get from one query (in case of using summary pages).
                            fields (list | str): Parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.
                            async_request (bool): Parameter defines the way you want to submit your task to Outscraper. It can be set to `False` (default) to send a task and wait until you got your results, or `True` to submit your task and retrieve the results later using a request ID with `get_request_archive`. Each response is available for `2` hours after a request has been completed.
                            ui (bool): Parameter defines whether a task will be executed as a UI task. This is commonly used when you want to create a regular platform task with API. Using this parameter overwrites the async_request parameter to `True`.

                    Returns:
                            list: json result

            See: https://app.outscraper.com/api-docs#tag/Amazon/paths/~1amazon~1products-v2/get
        '''
        queries = as_list(query)
        wait_async = async_request or (len(queries) > 1 and limit > 1)

        response = requests.get(f'{self._api_url}/amazon/products-v2', params={
            'query': queries,
            'limit': limit,
            'async': wait_async,
            'fields': parse_fields(fields),
            'ui': ui,
            'webhook': webhook,
        }, headers=self._api_headers)

        return self._handle_response(response, wait_async, async_request)

    def amazon_reviews(self, query: Union[list, str], limit: int = 10, sort: str = 'helpful', filter_by_reviewer: str = 'all_reviews',
        filter_by_star: str = 'all_stars', fields: Union[list, str] = None, async_request: bool = False, ui: bool = None, webhook: bool = None
    ) -> Union[list, dict]:
        '''
            Returns reviews from Amazon products.

                    Parameters:
                            query (list | str): You can use URLs or ASINs from Amazon products (e.g., https://www.amazon.com/dp/1612680194, 1612680194, etc.).
                            limit (int): Parameter specifies the limit of reviews to get from one query.
                            sort (str): Parameter specifies one of the sorting types. Available values: "helpful", and "recent".
                            filter_by_reviewer (str): The parameter specifies one of the reviewer filter types (All reviewers / Verified purchase only). Available values: "all_reviews", and "avp_only_reviews".
                            filter_by_star (str): The parameter specifies one of the filter types by stars. Available values: "all_stars", "five_star", "four_star", "three_star", "two_star", "one_star", "positive", and "critical".
                            fields (list | str): Parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.
                            async_request (bool): Parameter defines the way you want to submit your task to Outscraper. It can be set to `False` (default) to send a task and wait until you got your results, or `True` to submit your task and retrieve the results later using a request ID with `get_request_archive`. Each response is available for `2` hours after a request has been completed.
                            ui (bool): Parameter defines whether a task will be executed as a UI task. This is commonly used when you want to create a regular platform task with API. Using this parameter overwrites the async_request parameter to `True`.

                    Returns:
                            list: json result

            See: https://app.outscraper.com/api-docs#tag/Amazon/paths/~1amazon~1reviews/get
        '''
        queries = as_list(query)
        wait_async = async_request or (len(queries) > 1 and limit > 10)

        response = requests.get(f'{self._api_url}/amazon/reviews', params={
            'query': queries,
            'limit': limit,
            'sort': sort,
            'filterByReviewer': filter_by_reviewer,
            'filterByStar': filter_by_star,
            'async': wait_async,
            'fields': parse_fields(fields),
            'ui': ui,
            'webhook': webhook,
        }, headers=self._api_headers)

        return self._handle_response(response, wait_async, async_request)

    def yelp_search(self, query: Union[list, str], limit: int = 100,
        fields: Union[list, str] = None, async_request: bool = False, ui: bool = None, webhook: bool = None
    ) -> Union[list, dict]:
        '''
            Yelp

            Return search results from Yelp.

                    Parameters:
                            query (list | str): parameter defines search links with search parameters (e.g., "https://www.yelp.com/search?find_desc=Restaurants&find_loc=San+Francisco%2C+CA"). Using a lists allows multiple queries (up to 50) to be sent in one request and save on network latency time.
                            limit (int): parameter specifies the limit of items to get from one query.
                            fields (list | str): parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.
                            async_request (bool): parameter defines the way you want to submit your task to Outscraper. It can be set to `False` (default) to send a task and wait until you got your results, or `True` to submit your task and retrieve the results later using a request ID with `get_request_archive`. Each response is available for `2` hours after a request has been completed.
                            ui (bool): parameter defines whether a task will be executed as a UI task. This is commonly used when you want to create a regular platform task with API. Using this parameter overwrites the async_request parameter to `True`.

                    Returns:
                            list: json result

            See: https://app.outscraper.com/api-docs#tag/Others/paths/~1yelp-search/get
        '''
        queries = as_list(query)
        wait_async = async_request or len(queries) > 10

        response = requests.get(f'{self._api_url}/yelp-search', params={
            'query': queries,
            'limit': limit,
            'async': wait_async,
            'fields': parse_fields(fields),
            'ui': ui,
            'webhook': webhook,
        }, headers=self._api_headers)

        return self._handle_response(response, wait_async, async_request)

    def yelp_reviews(self, query: Union[list, str], limit: int = 100, sort: str = 'relevance_desc', cutoff: int = None,
        fields: Union[list, str] = None, async_request: bool = False, ui: bool = None, webhook: bool = None
    ) -> Union[list, dict]:
        '''
            Yelp Reviews

            Returns reviews from Yelp businesses.

                    Parameters:
                            query (list | str): parameter defines direct links, or IDs of any Yelp business (e.g., "https://www.yelp.com/biz/cancha-boutique-gastrobar-san-francisco", "eggcellent-waffles-san-francisco", "iXoLJWjbcXCO43RT-H0uQQ"). Using a lists allows multiple queries (up to 50) to be sent in one request and save on network latency time.
                            limit (int): parameter specifies the limit of reviews to get from one query.
                            sort (str): parameter specifies one of the sorting types. Available values: "relevance_desc", "date_desc", "date_asc", "rating_desc", "rating_asc", "elites_desc".
                            cutoff (int): parameter specifies the maximum timestamp value for reviews (oldest review). Using the "cutoff" parameter overwrites "sort" parameter to "date_desc".
                            fields (list | str): parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.
                            async_request (bool): parameter defines the way you want to submit your task to Outscraper. It can be set to `False` (default) to send a task and wait until you got your results, or `True` to submit your task and retrieve the results later using a request ID with `get_request_archive`. Each response is available for `2` hours after a request has been completed.
                            ui (bool): parameter defines whether a task will be executed as a UI task. This is commonly used when you want to create a regular platform task with API. Using this parameter overwrites the async_request parameter to `True`.

                    Returns:
                            list: json result

            See: https://app.outscraper.com/api-docs#tag/Reviews-and-Comments/paths/~1yelp~1reviews/get
        '''
        queries = as_list(query)
        wait_async = async_request or limit > 499 or len(queries) > 10

        response = requests.get(f'{self._api_url}/yelp/reviews', params={
            'query': queries,
            'limit': limit,
            'sort': sort,
            'cutoff': cutoff,
            'async': wait_async,
            'fields': parse_fields(fields),
            'ui': ui,
            'webhook': webhook,
        }, headers=self._api_headers)

        return self._handle_response(response, wait_async, async_request)

    def tripadvisor_reviews(self, query: Union[list, str], limit: int = 100, cutoff: int = None,
        fields: Union[list, str] = None, async_request: bool = False, ui: bool = None, webhook: bool = None
    ) -> Union[list, dict]:
        '''
            Tripadvisor Reviews

            Returns reviews from Tripadvisor businesses.

                    Parameters:
                            query (list | str): parameter defines links to Tripadvisor pages (e.g., "https://www.tripadvisor.com/Restaurant_Review-g187147-d12947099-Reviews-Mayfair_Garden-Paris_Ile_de_France.html"). Using a lists allows multiple queries (up to 50) to be sent in one request and save on network latency time.
                            limit (int): parameter specifies the limit of reviews to get from one query.
                            fields (list | str): parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.
                            async_request (bool): parameter defines the way you want to submit your task to Outscraper. It can be set to `False` (default) to send a task and wait until you got your results, or `True` to submit your task and retrieve the results later using a request ID with `get_request_archive`. Each response is available for `2` hours after a request has been completed.
                            ui (bool): parameter defines whether a task will be executed as a UI task. This is commonly used when you want to create a regular platform task with API. Using this parameter overwrites the async_request parameter to `True`.

                    Returns:
                            list: json result

            See: https://app.outscraper.com/api-docs#tag/Reviews-and-Comments/paths/~1trustpilot~1reviews/get
        '''
        queries = as_list(query)
        wait_async = async_request or limit > 499 or len(queries) > 10

        response = requests.get(f'{self._api_url}/tripadvisor/reviews', params={
            'query': queries,
            'limit': limit,
            'cutoff': cutoff,
            'async': wait_async,
            'fields': parse_fields(fields),
            'ui': ui,
            'webhook': webhook,
        }, headers=self._api_headers)

        return self._handle_response(response, wait_async, async_request)

    def apple_store_reviews(self, query: Union[list, str], limit: int = 100, sort: str = 'mosthelpful', cutoff: int = None,
        fields: Union[list, str] = None, async_request: bool = False, ui: bool = None, webhook: bool = None
    ) -> list:
        '''
            Returns reviews from AppStore apps.

                    Parameters:
                            query (list | str): you can use direct links, and IDs of any AppStore app (e.g., https://apps.apple.com/us/app/telegram-messenger/id686449807, id686449807). Using a lists allows multiple queries (up to 250) to be sent in one request and save on network latency time.
                            limit (int): parameter specifies the limit of reviews to extract from one query.
                            sort (str): parameter specifies one of the sorting types. Available values: "mosthelpful", "mostrecent".
                            cutoff (int): parameter specifies the maximum timestamp value for reviews. Using the cutoff parameter overwrites sort parameter to "newest".
                            fields (list | str): parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.
                            async_request (bool): parameter defines the way you want to submit your task to Outscraper. It can be set to `False` (default) to send a task and wait until you got your results, or `True` to submit your task and retrieve the results later using a request ID with `get_request_archive`. Each response is available for `2` hours after a request has been completed.
                            ui (bool): parameter defines whether a task will be executed as a UI task. This is commonly used when you want to create a regular platform task with API. Using this parameter overwrites the async_request parameter to `True`.

                    Returns:
                            list: json result

            See: https://app.outscraper.com/api-docs#tag/Reviews-and-Comments/paths/~1appstore~1reviews/get
        '''

        queries = as_list(query)
        wait_async = async_request or limit > 499 or len(queries) > 10

        response = requests.get(f'{self._api_url}/appstore/reviews', params={
            'query': queries,
            'limit': limit,
            'sort': sort,
            'cutoff': cutoff,
            'async': wait_async,
            'fields': parse_fields(fields),
            'ui': ui,
            'webhook': webhook,
        }, headers=self._api_headers)

        return self._handle_response(response, wait_async, async_request)
