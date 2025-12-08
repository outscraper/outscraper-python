import requests
from typing import Union, Tuple, Optional

from .transport import OutscraperTransport
from .utils import as_list, parse_fields, format_direction_queries


class OutscraperClient(object):
    '''OutscraperClient - Python SDK that allows using Outscraper's services and Outscraper's API.
    ```python
    from outscraper import OutscraperClient
    client = OutscraperClient(api_key='SECRET_API_KEY')
    maps_results = client.google_maps_search('restaurants brooklyn usa')
    search_results = client.google_search('bitcoin')
    ```
    https://github.com/outscraper/outscraper-python
    '''


    def __init__(self, api_key: str, requests_pause: int = 5) -> None:
        self._transport = OutscraperTransport(api_key=api_key)
        self._transport._requests_pause = requests_pause

    def _request(self, method: str, path: str, *, wait_async: bool = False, async_request: bool = False, use_handle_response: bool = True, **kwargs):
        return self._transport.api_request(
            method,
            path,
            wait_async=wait_async,
            async_request=async_request,
            use_handle_response=use_handle_response,
            **kwargs,
        )

    def get_tasks(self, query: str = '', last_id: str = '', page_size: int = 10) -> Tuple[list, bool]:
        '''
            Fetch user UI tasks.

                    Parameters:
                            query (str): parameter specifies the search query (tag).
                            last_id (str): parameter specifies the last task ID. It's commonly used in pagination.
                            page_size (int): parameter specifies the number of items to return.

                    Returns:
                            tuple[list, bool]: (tasks, has_more)

            See: https://app.outscraper.com/api-docs#tag/Outscraper-Platform-UI/paths/~1tasks/get
        '''

        params = {
            'query': query,
            'lastId': last_id,
            'pageSize': page_size,
        }
        response: requests.Response = self._request('GET', '/tasks', use_handle_response=False, params=params)

        if 199 < response.status_code < 300:
            data = response.json()

            if 'errorMessage' in data:
                raise Exception(f'Error: {data["errorMessage"]}')

            return data['tasks'], data['has_more']

        raise Exception(f'Response status code: {response.status_code}')

    def get_requests_history(self, type: str = 'running', skip: int = 0, page_size: int = 25) -> list:
        '''
            Fetch recent requests (up to 100, depending on page_size).

                Parameters:
                    type (str): parameter allows you to filter requests by type (running/finished).
                    skip (int): skip first N records. It's commonly used in pagination.
                    page_size (int): parameter specifies the number of items to return.

                Returns:
                        list: requests history

            See: https://app.outscraper.com/api-docs#tag/Requests/paths/~1requests/get
        '''

        params = {
            'type': type,
            'skip': skip,
            'pageSize': page_size,
        }
        response: requests.Response = self._request('GET', '/requests', use_handle_response=False, params=params)

        if 199 < response.status_code < 300:
            return response.json()

        raise Exception(f'Response status code: {response.status_code}')

    def get_request_archive(self, request_id: str) -> dict:
        '''
            Fetch request data from the archive

                Parameters:
                    request_id (str): unique id for the request provided by ['id']

                Returns:
                    dict: result from the archive

            See: https://app.outscraper.com/api-docs#tag/Requests/paths/~1requests~1{requestId}/get
        '''

        response = self._request('GET', f'/requests/{request_id}',  use_handle_response=False)

        if 199 < response.status_code < 300:
            return response.json()

        raise Exception(f'Response status code: {response.status_code}')

    def google_search(self, query: Union[list, str], pages_per_query: int = 1, uule: str = None, language: str = 'en', region: str = None,
        fields: Union[list, str] = None, async_request: bool = False, ui: bool = None, webhook: str = None
    ) -> Union[list, dict]:
        '''
            Get data from Google search

                    Parameters:
                            query (list | str): parameter defines the query or queries you want to search on Google. Using a lists allows multiple queries (up to 250) to be sent in one request and save on network latency time.
                            pages_per_query (int): parameter specifies the limit of pages to return from one query.
                            uule (str): Google UULE parameter is used to encode a place or an exact location (with latitude and longitude) into a code. By using it you can see a Google result page like someone located at the specified location.
                            language (str): parameter specifies the language to use for Google. Available values: "en", "de", "es", "es-419", "fr", "hr", "it", "nl", "pl", "pt-BR", "pt-PT", "vi", "tr", "ru", "ar", "th", "ko", "zh-CN", "zh-TW", "ja", "ach", "af", "ak", "ig", "az", "ban", "ceb", "xx-bork", "bs", "br", "ca", "cs", "sn", "co", "cy", "da", "yo", "et", "xx-elmer", "eo", "eu", "ee", "tl", "fil", "fo", "fy", "gaa", "ga", "gd", "gl", "gn", "xx-hacker", "ht", "ha", "haw", "bem", "rn", "id", "ia", "xh", "zu", "is", "jw", "rw", "sw", "tlh", "kg", "mfe", "kri", "la", "lv", "to", "lt", "ln", "loz", "lua", "lg", "hu", "mg", "mt", "mi", "ms", "pcm", "no", "nso", "ny", "nn", "uz", "oc", "om", "xx-pirate", "ro", "rm", "qu", "nyn", "crs", "sq", "sk", "sl", "so", "st", "sr-ME", "sr-Latn", "su", "fi", "sv", "tn", "tum", "tk", "tw", "wo", "el", "be", "bg", "ky", "kk", "mk", "mn", "sr", "tt", "tg", "uk", "ka", "hy", "yi", "iw", "ug", "ur", "ps", "sd", "fa", "ckb", "ti", "am", "ne", "mr", "hi", "bn", "pa", "gu", "or", "ta", "te", "kn", "ml", "si", "lo", "my", "km", "chr".
                            region (str): parameter specifies the region to use for Google. Available values: "AF", "AL", "DZ", "AS", "AD", "AO", "AI", "AG", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BY", "BE", "BZ", "BJ", "BT", "BO", "BA", "BW", "BR", "VG", "BN", "BG", "BF", "BI", "KH", "CM", "CA", "CV", "CF", "TD", "CL", "CN", "CO", "CG", "CD", "CK", "CR", "CI", "HR", "CU", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "EE", "ET", "FJ", "FI", "FR", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GT", "GG", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KW", "KG", "LA", "LV", "LB", "LS", "LY", "LI", "LT", "LU", "MG", "MW", "MY", "MV", "ML", "MT", "MU", "MX", "FM", "MD", "MN", "ME", "MS", "MA", "MZ", "MM", "NA", "NR", "NP", "NL", "NZ", "NI", "NE", "NG", "NU", "MK", "NO", "OM", "PK", "PS", "PA", "PG", "PY", "PE", "PH", "PN", "PL", "PT", "PR", "QA", "RO", "RU", "RW", "WS", "SM", "ST", "SA", "SN", "RS", "SC", "SL", "SG", "SK", "SI", "SB", "SO", "ZA", "KR", "ES", "LK", "SH", "VC", "SR", "SE", "CH", "TW", "TJ", "TZ", "TH", "TL", "TG", "TO", "TT", "TN", "TR", "TM", "VI", "UG", "UA", "AE", "GB", "US", "UY", "UZ", "VU", "VE", "VN", "ZM", "ZW".
                            fields (list | str): parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.
                            async_request (bool): parameter defines the way you want to submit your task to Outscraper. It can be set to `False` (default) to send a task and wait until you got your results, or `True` to submit your task and retrieve the results later using a request ID with `get_request_archive`. Each response is available for `2` hours after a request has been completed.
                            ui (bool): parameter defines whether a task will be executed as a UI task. This is commonly used when you want to create a regular platform task with API. Using this parameter overwrites the async_request parameter to `True`.
                            webhook (str): parameter defines the URL address (callback) to which Outscraper will create a POST request with a JSON body once a task/request is finished. Using this parameter overwrites the webhook from integrations.

                    Returns:
                            list|dict: JSON result

            See: https://app.outscraper.com/api-docs#tag/Google/paths/~1google-search-v3/get
        '''

        queries = as_list(query)
        wait_async = async_request or (len(queries) > 1 or pages_per_query > 1)
        params = {
            'query': queries,
            'pagesPerQuery': pages_per_query,
            'uule': uule,
            'language': language,
            'region': region,
            'async': async_request,
            'fields': parse_fields(fields),
            'ui': ui,
            'webhook': webhook,
        }

        return self._request('GET', '/google-search-v3', wait_async=wait_async, async_request=async_request, params=params)

    def google_search_news(self, query: Union[list, str], pages_per_query: int = 1, uule: str = None, tbs: str = None, language: str = 'en',
        region: str = None, fields: Union[list, str] = None, async_request: bool = False, ui: bool = None, webhook: str = None
    ) -> list:
        '''
            Returns search results from Google based on a given search query (or many queries).

                    Parameters:
                            query (list | str): parameter defines the query or queries you want to search news on Google. Using a lists allows multiple queries (up to 250) to be sent in one request and save on network latency time.
                            pages_per_query (int): parameter specifies the limit of pages to return from one query.
                            uule (str): Google UULE parameter is used to encode a place or an exact location (with latitude and longitude) into a code. By using it you can see a Google result page like someone located at the specified location.
                            tbs: parameter specifies the date range of the results (h - past hour, d - past 24 hours, w - past week, m - past month, 'y' - past year).
                            language (str): parameter specifies the language to use for Google. Available values: "en", "de", "es", "es-419", "fr", "hr", "it", "nl", "pl", "pt-BR", "pt-PT", "vi", "tr", "ru", "ar", "th", "ko", "zh-CN", "zh-TW", "ja", "ach", "af", "ak", "ig", "az", "ban", "ceb", "xx-bork", "bs", "br", "ca", "cs", "sn", "co", "cy", "da", "yo", "et", "xx-elmer", "eo", "eu", "ee", "tl", "fil", "fo", "fy", "gaa", "ga", "gd", "gl", "gn", "xx-hacker", "ht", "ha", "haw", "bem", "rn", "id", "ia", "xh", "zu", "is", "jw", "rw", "sw", "tlh", "kg", "mfe", "kri", "la", "lv", "to", "lt", "ln", "loz", "lua", "lg", "hu", "mg", "mt", "mi", "ms", "pcm", "no", "nso", "ny", "nn", "uz", "oc", "om", "xx-pirate", "ro", "rm", "qu", "nyn", "crs", "sq", "sk", "sl", "so", "st", "sr-ME", "sr-Latn", "su", "fi", "sv", "tn", "tum", "tk", "tw", "wo", "el", "be", "bg", "ky", "kk", "mk", "mn", "sr", "tt", "tg", "uk", "ka", "hy", "yi", "iw", "ug", "ur", "ps", "sd", "fa", "ckb", "ti", "am", "ne", "mr", "hi", "bn", "pa", "gu", "or", "ta", "te", "kn", "ml", "si", "lo", "my", "km", "chr".
                            region (str): parameter specifies the region to use for Google. Available values: "AF", "AL", "DZ", "AS", "AD", "AO", "AI", "AG", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BY", "BE", "BZ", "BJ", "BT", "BO", "BA", "BW", "BR", "VG", "BN", "BG", "BF", "BI", "KH", "CM", "CA", "CV", "CF", "TD", "CL", "CN", "CO", "CG", "CD", "CK", "CR", "CI", "HR", "CU", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "EE", "ET", "FJ", "FI", "FR", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GT", "GG", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KW", "KG", "LA", "LV", "LB", "LS", "LY", "LI", "LT", "LU", "MG", "MW", "MY", "MV", "ML", "MT", "MU", "MX", "FM", "MD", "MN", "ME", "MS", "MA", "MZ", "MM", "NA", "NR", "NP", "NL", "NZ", "NI", "NE", "NG", "NU", "MK", "NO", "OM", "PK", "PS", "PA", "PG", "PY", "PE", "PH", "PN", "PL", "PT", "PR", "QA", "RO", "RU", "RW", "WS", "SM", "ST", "SA", "SN", "RS", "SC", "SL", "SG", "SK", "SI", "SB", "SO", "ZA", "KR", "ES", "LK", "SH", "VC", "SR", "SE", "CH", "TW", "TJ", "TZ", "TH", "TL", "TG", "TO", "TT", "TN", "TR", "TM", "VI", "UG", "UA", "AE", "GB", "US", "UY", "UZ", "VU", "VE", "VN", "ZM", "ZW".
                            fields (list | str): parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.

                    Returns:
                            list|dict: JSON result

            See: https://app.outscraper.com/api-docs#tag/Google/paths/~1google-search-news/get
        '''

        queries = as_list(query)
        wait_async = async_request or (len(queries) > 1 or pages_per_query > 1)
        params = {
            'query': queries,
            'pagesPerQuery': pages_per_query,
            'uule': uule,
            'tbs': tbs,
            'language': language,
            'region': region,
            'async': async_request,
            'fields': parse_fields(fields),
            'ui': ui,
            'webhook': webhook,
        }

        return self._request('GET', '/google-search-news', wait_async=wait_async, async_request=async_request, params=params)

    def google_maps_search_v1(self, query: Union[list, str], limit: int = 500, extract_contacts: bool = False, drop_duplicates: bool = False,
        coordinates: str = None, language: str = 'en', region: str = None, fields: Union[list, str] = None) -> list:
        '''
            Get Google Maps Data (old version)

            Returns places from Google Maps based on a given search query (or many queries).
            The results from searches are the same as you would see by visiting a regular Google Maps site. However, in most cases, it's recommended to use locations inside queries (e.g., bars, NY, USA) as the IP addresses of Outscraper's servers might be located in different countries.

                Parameters:
                    query (list | str): parameter defines the query you want to search. You can use anything that you would use on a regular Google Maps site. Additionally, you can use google_id, place_id or urls to Google Maps places. Using a lists allows multiple queries (up to 250) to be sent in one request and save on network latency time.
                    limit (int): parameter specifies the limit of places to take from one query search. The same as on Google Maps site, there are no more than 400 organizations per one query search. Use more precise categories (e.g., Asian restaurant, Italian restaurant) and/or locations (e.g., restaurants, Brooklyn 11211, restaurants, Brooklyn 11215) to overcome this limitation.
                    extract_contacts (bool): parameter specifies whether the bot will scrape additional data (emails, social links, site keywords…) from companies’ websites. It increases the time of the extraction.
                    drop_duplicates (bool): parameter specifies whether the bot will drop the same organizations from different queries. Using the parameter combines results from each query inside one big array.
                    coordinates (str): parameter defines the coordinates to use along with the query. Example: "@41.3954381,2.1628662,15.1z".
                    language (str): parameter specifies the language to use for Google. Available values: "en", "de", "es", "es-419", "fr", "hr", "it", "nl", "pl", "pt-BR", "pt-PT", "vi", "tr", "ru", "ar", "th", "ko", "zh-CN", "zh-TW", "ja", "ach", "af", "ak", "ig", "az", "ban", "ceb", "xx-bork", "bs", "br", "ca", "cs", "sn", "co", "cy", "da", "yo", "et", "xx-elmer", "eo", "eu", "ee", "tl", "fil", "fo", "fy", "gaa", "ga", "gd", "gl", "gn", "xx-hacker", "ht", "ha", "haw", "bem", "rn", "id", "ia", "xh", "zu", "is", "jw", "rw", "sw", "tlh", "kg", "mfe", "kri", "la", "lv", "to", "lt", "ln", "loz", "lua", "lg", "hu", "mg", "mt", "mi", "ms", "pcm", "no", "nso", "ny", "nn", "uz", "oc", "om", "xx-pirate", "ro", "rm", "qu", "nyn", "crs", "sq", "sk", "sl", "so", "st", "sr-ME", "sr-Latn", "su", "fi", "sv", "tn", "tum", "tk", "tw", "wo", "el", "be", "bg", "ky", "kk", "mk", "mn", "sr", "tt", "tg", "uk", "ka", "hy", "yi", "iw", "ug", "ur", "ps", "sd", "fa", "ckb", "ti", "am", "ne", "mr", "hi", "bn", "pa", "gu", "or", "ta", "te", "kn", "ml", "si", "lo", "my", "km", "chr".
                    region (str): parameter specifies the region to use for Google. Available values: "AF", "AL", "DZ", "AS", "AD", "AO", "AI", "AG", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BY", "BE", "BZ", "BJ", "BT", "BO", "BA", "BW", "BR", "VG", "BN", "BG", "BF", "BI", "KH", "CM", "CA", "CV", "CF", "TD", "CL", "CN", "CO", "CG", "CD", "CK", "CR", "CI", "HR", "CU", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "EE", "ET", "FJ", "FI", "FR", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GT", "GG", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KW", "KG", "LA", "LV", "LB", "LS", "LY", "LI", "LT", "LU", "MG", "MW", "MY", "MV", "ML", "MT", "MU", "MX", "FM", "MD", "MN", "ME", "MS", "MA", "MZ", "MM", "NA", "NR", "NP", "NL", "NZ", "NI", "NE", "NG", "NU", "MK", "NO", "OM", "PK", "PS", "PA", "PG", "PY", "PE", "PH", "PN", "PL", "PT", "PR", "QA", "RO", "RU", "RW", "WS", "SM", "ST", "SA", "SN", "RS", "SC", "SL", "SG", "SK", "SI", "SB", "SO", "ZA", "KR", "ES", "LK", "SH", "VC", "SR", "SE", "CH", "TW", "TJ", "TZ", "TH", "TL", "TG", "TO", "TT", "TN", "TR", "TM", "VI", "UG", "UA", "AE", "GB", "US", "UY", "UZ", "VU", "VE", "VN", "ZM", "ZW".
                    fields (list | str): parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.

                Returns:
                    list|dict: JSON result

            See: https://app.outscraper.com/api-docs#tag/Google/paths/~1maps~1search/get
        '''

        params = {
            'query': as_list(query),
            'coordinates': coordinates,
            'language': language,
            'region': region,
            'organizationsPerQueryLimit': limit,
            'extractContacts': extract_contacts,
            'dropDuplicates': drop_duplicates,
            'fields': parse_fields(fields),
        }

        return self._request('GET', '/maps/search', wait_async=True, params=params)

    def google_maps_search(self, query: Union[list, str], limit: int = 20, drop_duplicates: bool = False, language: str = 'en',
       region: Optional[str] = None, skip: int = 0, coordinates: str = '', enrichment: Optional[list] = None, fields: Union[list, str] = None,
        async_request: bool = False, ui: bool = False, webhook: str = '') -> Union[list, dict]:
        '''
            Get Google Maps Data (speed-optimized endpoint for real-time data)

            Returns places from Google Maps based on a given search query (or many queries).
            The results from searches are the same as you would see by visiting a regular Google Maps site. However, in most cases, it's recommended
            to use locations inside queries (e.g., bars, NY, USA) as the IP addresses of Outscraper's servers might be located in different countries.
            This endpoint is optimized for fast responses and can be used as a real-time API.
            Set the limit parameter to 20 to achieve the maximum response speed.

                Parameters:
                    query (list | str): parameter defines the query you want to search. You can use anything that you would use on a regular Google Maps site. Additionally, you can use google_id. The example of valid queries: Real estate agency, Rome, Italy, The NoMad Restaurant, NY, USA, restaurants, Brooklyn 11203, 0x886916e8bc273979:0x5141fcb11460b226, etc. Using a lists allows multiple queries (up to 250) to be sent in one request and save on network latency time.
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
                    webhook (str): parameter defines the URL address (callback) to which Outscraper will create a POST request with a JSON body once a task/request is finished. Using this parameter overwrites the webhook from integrations.

                Returns:
                    list|dict: JSON result

            See: https://app.outscraper.com/api-docs#tag/Google/paths/~1google-maps-search/get
        '''

        queries = as_list(query)
        queries_len = len(queries)
        wait_async = async_request or (queries_len > 10 and limit > 1) or queries_len > 50
        payload = {
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
        }

        return self._request('POST', '/google-maps-search', wait_async=wait_async, async_request=async_request, json=payload)

    def google_maps_directions(self, query: Union[list, str], departure_time: int = None, finish_time: int = None, interval: int = 60, travel_mode: str = 'best',
        language: str = 'en', region: str = None, fields: Union[list, str] = None, async_request: bool = False,
        ui: bool = None, webhook: str = None
    ) -> list:
        '''
            Get Google Maps Directions

            Returns directions between two points from Google Maps.

                    Parameters:
                            query (list | str): parameter defines the query that should contains "<origin> + <4 spaces> + <destination>". Using a lists allows multiple queries (up to 250) to be sent in one request and save on network latency time.
                            departure_time (int): parameter specifies the departure timestamp. The current timestamp is used when the value is not provided.
                            finish_time (int): parameter specifies the end departure timestamp. Using this parameter requires using the interval parameter.
                            interval (int): parameter specifies the interval to use between departure_time and finish_time.
                            language (str): parameter specifies the language to use for Google. Available values: "en", "de", "es", "es-419", "fr", "hr", "it", "nl", "pl", "pt-BR", "pt-PT", "vi", "tr", "ru", "ar", "th", "ko", "zh-CN", "zh-TW", "ja", "ach", "af", "ak", "ig", "az", "ban", "ceb", "xx-bork", "bs", "br", "ca", "cs", "sn", "co", "cy", "da", "yo", "et", "xx-elmer", "eo", "eu", "ee", "tl", "fil", "fo", "fy", "gaa", "ga", "gd", "gl", "gn", "xx-hacker", "ht", "ha", "haw", "bem", "rn", "id", "ia", "xh", "zu", "is", "jw", "rw", "sw", "tlh", "kg", "mfe", "kri", "la", "lv", "to", "lt", "ln", "loz", "lua", "lg", "hu", "mg", "mt", "mi", "ms", "pcm", "no", "nso", "ny", "nn", "uz", "oc", "om", "xx-pirate", "ro", "rm", "qu", "nyn", "crs", "sq", "sk", "sl", "so", "st", "sr-ME", "sr-Latn", "su", "fi", "sv", "tn", "tum", "tk", "tw", "wo", "el", "be", "bg", "ky", "kk", "mk", "mn", "sr", "tt", "tg", "uk", "ka", "hy", "yi", "iw", "ug", "ur", "ps", "sd", "fa", "ckb", "ti", "am", "ne", "mr", "hi", "bn", "pa", "gu", "or", "ta", "te", "kn", "ml", "si", "lo", "my", "km", "chr".
                            travel_mode (str):  parameter specifies one of the travel modes. Available values: "best", "car", "transit", "walk", "bike", "flight".
                            region (str): parameter specifies the region to use for Google. Available values: "AF", "AL", "DZ", "AS", "AD", "AO", "AI", "AG", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BY", "BE", "BZ", "BJ", "BT", "BO", "BA", "BW", "BR", "VG", "BN", "BG", "BF", "BI", "KH", "CM", "CA", "CV", "CF", "TD", "CL", "CN", "CO", "CG", "CD", "CK", "CR", "CI", "HR", "CU", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "EE", "ET", "FJ", "FI", "FR", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GT", "GG", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KW", "KG", "LA", "LV", "LB", "LS", "LY", "LI", "LT", "LU", "MG", "MW", "MY", "MV", "ML", "MT", "MU", "MX", "FM", "MD", "MN", "ME", "MS", "MA", "MZ", "MM", "NA", "NR", "NP", "NL", "NZ", "NI", "NE", "NG", "NU", "MK", "NO", "OM", "PK", "PS", "PA", "PG", "PY", "PE", "PH", "PN", "PL", "PT", "PR", "QA", "RO", "RU", "RW", "WS", "SM", "ST", "SA", "SN", "RS", "SC", "SL", "SG", "SK", "SI", "SB", "SO", "ZA", "KR", "ES", "LK", "SH", "VC", "SR", "SE", "CH", "TW", "TJ", "TZ", "TH", "TL", "TG", "TO", "TT", "TN", "TR", "TM", "VI", "UG", "UA", "AE", "GB", "US", "UY", "UZ", "VU", "VE", "VN", "ZM", "ZW".
                            fields (list | str): parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.
                            async_request (bool): parameter defines the way you want to submit your task to Outscraper. It can be set to `False` (default) to send a task and wait until you got your results, or `True` to submit your task and retrieve the results later using a request ID with `get_request_archive`. Each response is available for `2` hours after a request has been completed.
                            ui (bool): parameter defines whether a task will be executed as a UI task. This is commonly used when you want to create a regular platform task with API. Using this parameter overwrites the async_request parameter to `True`.
                            webhook (str): parameter defines the URL address (callback) to which Outscraper will create a POST request with a JSON body once a task/request is finished. Using this parameter overwrites the webhook from integrations.

                    Returns:
                            list|dict: JSON result

            See: https://app.outscraper.com/api-docs#tag/Google/paths/~1maps~1directions/get
        '''

        queries = format_direction_queries(query)
        wait_async = async_request or len(queries) > 10
        params = {
            'query': queries,
            'departure_time': departure_time,
            'interval': interval,
            'finish_time': finish_time,
            'travel_mode': travel_mode,
            'language': language,
            'region': region,
            'async': wait_async,
            'fields': parse_fields(fields),
            'ui': ui,
            'webhook': webhook,
        }

        return self._request('GET', '/maps/directions', wait_async=wait_async, async_request=async_request, params=params)

    def google_maps_reviews_v2(self, query: Union[list, str], reviews_limit: int = 100, limit: int = 1, sort: str = 'most_relevant',
        skip: int = 0, start: int = None, cutoff: int = None, cutoff_rating: int = None, ignore_empty: bool = False,
        coordinates: str = None, language: str = 'en', region: str = None, fields: Union[list, str] = None
    ) -> list:
        '''
            Get Google Maps Reviews (old version)

            Returns Google Maps reviews from places when using search queries (e.g., restaurants, Manhattan, NY, USA) or from a single place when using IDs or names (e.g., NoMad Restaurant, NY, USA, 0x886916e8bc273979:0x5141fcb11460b226, ChIJu7bMNFV-54gR-lrHScvPRX4).
            Places information will be returned as well in the case at least one review is found.

                    Parameters:
                            query (list | str): parameter defines the query you want to search. You can use anything that you would use on a regular Google Maps site. Additionally, you can use google_id, place_id or urls to Google Maps places. Using a list allows multiple queries (up to 250) to be sent in one request and save on network latency time.
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
                            list|dict: JSON result

            See: https://app.outscraper.com/api-docs#tag/Google/paths/~1maps~1reviews-v3/get
        '''

        params = {
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
        },

        return self._request('GET', '/maps/reviews-v2', wait_async=True, params=params)

    def google_maps_reviews(self, query: Union[list, str], reviews_limit: int = 10, limit: int = 1, sort: str = 'most_relevant',
        start: int = None, cutoff: int = None, cutoff_rating: int = None, ignore_empty: bool = False, language: str = 'en',
        region: str = None, reviews_query: str = None, source: str = None, last_pagination_id: str = None, fields: Union[list, str] = None, async_request: bool = False,
        ui: bool = None, webhook: str = None
    ) -> Union[list, dict]:
        '''
            Get Google Maps Reviews V3 (speed optimized endpoint for real time data)

            Returns Google Maps reviews from places when using search queries (e.g., restaurants, Manhattan, NY, USA) or from a single place when using Google IDs or names (e.g., NoMad Restaurant, NY, USA, 0x886916e8bc273979:0x5141fcb11460b226).
            Places information will be returned as well in the case at least one review is found.
            This endpoint is optimized for fast responses and can be used as real time API. Set the reviews_limit parameter to 10 to achieve the maximum response speed.

                    Parameters:
                            query (list | str): parameter defines the query you want to search. You can use anything that you would use on a regular Google Maps site. Additionally, you can use google_id, place_id or urls to Google Maps places. Using a lists allows multiple queries (up to 250) to be sent in one request and save on network latency time.
                            reviews_limit (int): parameter specifies the limit of reviews to extract from one place (0 - unlimited).
                            limit (str): parameter specifies the limit of places to take from one query search.
                            sort (str): parameter specifies one of the sorting types. Available values: "most_relevant", "newest", "highest_rating", "lowest_rating".
                            start (int): parameter specifies the start timestamp value for reviews (newest review). The current timestamp is used when the value is not provided. Using the start parameter overwrites sort parameter to newest.
                            cutoff (int): parameter specifies the maximum timestamp value for reviews (oldest review). Using the cutoff parameter overwrites sort parameter to newest.
                            cutoff_rating (int): parameter specifies the maximum (for lowest_rating sorting) or minimum (for highest_rating sorting) rating for reviews. Using the cutoffRating requires sorting to be set to "lowest_rating" or "highest_rating".
                            ignore_empty (bool): parameter specifies whether to ignore reviews without text or not.
                            last_pagination_id (str): parameter specifies the review_pagination_id of the last item. It's commonly used in pagination.
                            reviews_query (str): parameter specifies the query to search among the reviews (e.g. wow, amazing, horrible place).
                            source (str): parameter specifies source filter. This commonly used for hotels where you can find reviews from other sources like Booking.com, Expedia, etc.
                            coordinates (str): parameter defines the coordinates of the location where you want your query to be applied. It has to be constructed in the next sequence: "@" + "latitude" + "," + "longitude" + "," + "zoom" (e.g. "@41.3954381,2.1628662,15.1z").
                            language (str): parameter specifies the language to use for Google. Available values: "en", "de", "es", "es-419", "fr", "hr", "it", "nl", "pl", "pt-BR", "pt-PT", "vi", "tr", "ru", "ar", "th", "ko", "zh-CN", "zh-TW", "ja", "ach", "af", "ak", "ig", "az", "ban", "ceb", "xx-bork", "bs", "br", "ca", "cs", "sn", "co", "cy", "da", "yo", "et", "xx-elmer", "eo", "eu", "ee", "tl", "fil", "fo", "fy", "gaa", "ga", "gd", "gl", "gn", "xx-hacker", "ht", "ha", "haw", "bem", "rn", "id", "ia", "xh", "zu", "is", "jw", "rw", "sw", "tlh", "kg", "mfe", "kri", "la", "lv", "to", "lt", "ln", "loz", "lua", "lg", "hu", "mg", "mt", "mi", "ms", "pcm", "no", "nso", "ny", "nn", "uz", "oc", "om", "xx-pirate", "ro", "rm", "qu", "nyn", "crs", "sq", "sk", "sl", "so", "st", "sr-ME", "sr-Latn", "su", "fi", "sv", "tn", "tum", "tk", "tw", "wo", "el", "be", "bg", "ky", "kk", "mk", "mn", "sr", "tt", "tg", "uk", "ka", "hy", "yi", "iw", "ug", "ur", "ps", "sd", "fa", "ckb", "ti", "am", "ne", "mr", "hi", "bn", "pa", "gu", "or", "ta", "te", "kn", "ml", "si", "lo", "my", "km", "chr".
                            region (str): parameter specifies the region to use for Google. Available values: "AF", "AL", "DZ", "AS", "AD", "AO", "AI", "AG", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BY", "BE", "BZ", "BJ", "BT", "BO", "BA", "BW", "BR", "VG", "BN", "BG", "BF", "BI", "KH", "CM", "CA", "CV", "CF", "TD", "CL", "CN", "CO", "CG", "CD", "CK", "CR", "CI", "HR", "CU", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "EE", "ET", "FJ", "FI", "FR", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GT", "GG", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KW", "KG", "LA", "LV", "LB", "LS", "LY", "LI", "LT", "LU", "MG", "MW", "MY", "MV", "ML", "MT", "MU", "MX", "FM", "MD", "MN", "ME", "MS", "MA", "MZ", "MM", "NA", "NR", "NP", "NL", "NZ", "NI", "NE", "NG", "NU", "MK", "NO", "OM", "PK", "PS", "PA", "PG", "PY", "PE", "PH", "PN", "PL", "PT", "PR", "QA", "RO", "RU", "RW", "WS", "SM", "ST", "SA", "SN", "RS", "SC", "SL", "SG", "SK", "SI", "SB", "SO", "ZA", "KR", "ES", "LK", "SH", "VC", "SR", "SE", "CH", "TW", "TJ", "TZ", "TH", "TL", "TG", "TO", "TT", "TN", "TR", "TM", "VI", "UG", "UA", "AE", "GB", "US", "UY", "UZ", "VU", "VE", "VN", "ZM", "ZW".
                            fields (list | str): parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.
                            async_request (bool): parameter defines the way you want to submit your task to Outscraper. It can be set to `False` (default) to send a task and wait until you got your results, or `True` to submit your task and retrieve the results later using a request ID with `get_request_archive`. Each response is available for `2` hours after a request has been completed.
                            ui (bool): parameter defines whether a task will be executed as a UI task. This is commonly used when you want to create a regular platform task with API. Using this parameter overwrites the async_request parameter to `True`.
                            webhook (str): parameter defines the URL address (callback) to which Outscraper will create a POST request with a JSON body once a task/request is finished. Using this parameter overwrites the webhook from integrations.

                    Returns:
                            list|dict: JSON result

            See: https://app.outscraper.com/api-docs#tag/Google/paths/~1maps~1reviews-v3/get
        '''

        queries = as_list(query)
        wait_async = async_request or reviews_limit > 499 or reviews_limit == 0 or len(queries) > 10
        params = {
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
            'source': source,
            'language': language,
            'region': region,
            'async': wait_async,
            'fields': parse_fields(fields),
            'ui': ui,
            'webhook': webhook,
        }

        return self._request('GET', '/maps/reviews-v3', wait_async=wait_async, async_request=async_request, params=params)

    def google_maps_photos(self, query: Union[list, str], photosLimit: int = 100, limit: int = 1, tag: str = None, language: str = 'en',
        region: str = None, fields: Union[list, str] = None, async_request: bool = False, ui: bool = None, webhook: str = None
    ) -> list:
        '''
            Get reviews from Google Maps

                    Parameters:
                            query (list | str): parameter defines the query you want to search. You can use anything that you would use on a regular Google Maps site. Additionally, you can use google_id, place_id or urls to Google Maps places. Using a lists allows multiple queries (up to 250) to be sent in one request and save on network latency time.
                            photosLimit (int): parameter specifies the limit of photos to extract from one place.
                            limit (str): parameter specifies the limit of places to take from one query search.
                            tag (str): parameter specifies one of the filtering types. Available values: "all", "latest", "menu", "by_owner".
                            language (str): parameter specifies the language to use for Google. Available values: "en", "de", "es", "es-419", "fr", "hr", "it", "nl", "pl", "pt-BR", "pt-PT", "vi", "tr", "ru", "ar", "th", "ko", "zh-CN", "zh-TW", "ja", "ach", "af", "ak", "ig", "az", "ban", "ceb", "xx-bork", "bs", "br", "ca", "cs", "sn", "co", "cy", "da", "yo", "et", "xx-elmer", "eo", "eu", "ee", "tl", "fil", "fo", "fy", "gaa", "ga", "gd", "gl", "gn", "xx-hacker", "ht", "ha", "haw", "bem", "rn", "id", "ia", "xh", "zu", "is", "jw", "rw", "sw", "tlh", "kg", "mfe", "kri", "la", "lv", "to", "lt", "ln", "loz", "lua", "lg", "hu", "mg", "mt", "mi", "ms", "pcm", "no", "nso", "ny", "nn", "uz", "oc", "om", "xx-pirate", "ro", "rm", "qu", "nyn", "crs", "sq", "sk", "sl", "so", "st", "sr-ME", "sr-Latn", "su", "fi", "sv", "tn", "tum", "tk", "tw", "wo", "el", "be", "bg", "ky", "kk", "mk", "mn", "sr", "tt", "tg", "uk", "ka", "hy", "yi", "iw", "ug", "ur", "ps", "sd", "fa", "ckb", "ti", "am", "ne", "mr", "hi", "bn", "pa", "gu", "or", "ta", "te", "kn", "ml", "si", "lo", "my", "km", "chr".
                            region (str): parameter specifies the region to use for Google. Available values: "AF", "AL", "DZ", "AS", "AD", "AO", "AI", "AG", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BY", "BE", "BZ", "BJ", "BT", "BO", "BA", "BW", "BR", "VG", "BN", "BG", "BF", "BI", "KH", "CM", "CA", "CV", "CF", "TD", "CL", "CN", "CO", "CG", "CD", "CK", "CR", "CI", "HR", "CU", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "EE", "ET", "FJ", "FI", "FR", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GT", "GG", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KW", "KG", "LA", "LV", "LB", "LS", "LY", "LI", "LT", "LU", "MG", "MW", "MY", "MV", "ML", "MT", "MU", "MX", "FM", "MD", "MN", "ME", "MS", "MA", "MZ", "MM", "NA", "NR", "NP", "NL", "NZ", "NI", "NE", "NG", "NU", "MK", "NO", "OM", "PK", "PS", "PA", "PG", "PY", "PE", "PH", "PN", "PL", "PT", "PR", "QA", "RO", "RU", "RW", "WS", "SM", "ST", "SA", "SN", "RS", "SC", "SL", "SG", "SK", "SI", "SB", "SO", "ZA", "KR", "ES", "LK", "SH", "VC", "SR", "SE", "CH", "TW", "TJ", "TZ", "TH", "TL", "TG", "TO", "TT", "TN", "TR", "TM", "VI", "UG", "UA", "AE", "GB", "US", "UY", "UZ", "VU", "VE", "VN", "ZM", "ZW".
                            fields (list | str): parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.
                            ui (bool): parameter defines whether a task will be executed as a UI task. This is commonly used when you want to create a regular platform task with API. Using this parameter overwrites the async_request parameter to `True`.
                            webhook (str): parameter defines the URL address (callback) to which Outscraper will create a POST request with a JSON body once a task/request is finished. Using this parameter overwrites the webhook from integrations.

                    Returns:
                            list|dict: JSON result

            See: https://app.outscraper.com/api-docs#tag/Google/paths/~1maps~1photos-v3/get
        '''

        queries = as_list(query)
        wait_async = async_request or photosLimit > 499 or photosLimit == 0 or len(queries) > 10
        params = {
            'query': queries,
            'photosLimit': photosLimit,
            'limit': limit,
            'tag': tag,
            'language': language,
            'region': region,
            'async': wait_async,
            'fields': parse_fields(fields),
            'ui': ui,
            'webhook': webhook,
        }

        return self._request('GET', '/maps/photos-v3', wait_async=wait_async, async_request=async_request, params=params)

    def google_maps_business_reviews(self, *args, **kwargs) -> list: # deprecated
        return self.google_maps_reviews(*args, **kwargs)

    def google_play_reviews(self, query: Union[list, str], reviews_limit: int = 100, sort: str = 'most_relevant', cutoff: int = None,
        rating: int = None, language: str = 'en', fields: Union[list, str] = None, async_request: bool = False, ui: bool = None, webhook: str = None
    ) -> list:
        '''
            Returns reviews from any app/book/movie in the Google Play store.

                    Parameters:
                            query (list | str): you can use app IDs or direct links (e.g., https://play.google.com/store/apps/details?id=com.facebook.katana, com.facebook.katana). Using a lists allows multiple queries (up to 250) to be sent in one request and save on network latency time.
                            reviews_limit (int): parameter specifies the limit of reviews to extract from one query.
                            sort (str): parameter specifies one of the sorting types. Available values: "most_relevant", "newest", "rating".
                            cutoff (int): parameter specifies the maximum timestamp value for reviews. Using the cutoff parameter overwrites sort parameter to "newest".
                            rating (int): Filter by a specific rating. Works only with "sort=rating".
                            language (str): parameter specifies the language to use for Google. Available values: "en", "de", "es", "es-419", "fr", "hr", "it", "nl", "pl", "pt-BR", "pt-PT", "vi", "tr", "ru", "ar", "th", "ko", "zh-CN", "zh-TW", "ja", "ach", "af", "ak", "ig", "az", "ban", "ceb", "xx-bork", "bs", "br", "ca", "cs", "sn", "co", "cy", "da", "yo", "et", "xx-elmer", "eo", "eu", "ee", "tl", "fil", "fo", "fy", "gaa", "ga", "gd", "gl", "gn", "xx-hacker", "ht", "ha", "haw", "bem", "rn", "id", "ia", "xh", "zu", "is", "jw", "rw", "sw", "tlh", "kg", "mfe", "kri", "la", "lv", "to", "lt", "ln", "loz", "lua", "lg", "hu", "mg", "mt", "mi", "ms", "pcm", "no", "nso", "ny", "nn", "uz", "oc", "om", "xx-pirate", "ro", "rm", "qu", "nyn", "crs", "sq", "sk", "sl", "so", "st", "sr-ME", "sr-Latn", "su", "fi", "sv", "tn", "tum", "tk", "tw", "wo", "el", "be", "bg", "ky", "kk", "mk", "mn", "sr", "tt", "tg", "uk", "ka", "hy", "yi", "iw", "ug", "ur", "ps", "sd", "fa", "ckb", "ti", "am", "ne", "mr", "hi", "bn", "pa", "gu", "or", "ta", "te", "kn", "ml", "si", "lo", "my", "km", "chr".
                            fields (list | str): parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.
                            ui (bool): parameter defines whether a task will be executed as a UI task. This is commonly used when you want to create a regular platform task with API. Using this parameter overwrites the async_request parameter to `True`.
                            webhook (str): parameter defines the URL address (callback) to which Outscraper will create a POST request with a JSON body once a task/request is finished. Using this parameter overwrites the webhook from integrations.

                    Returns:
                            list|dict: JSON result

            See: https://app.outscraper.com/api-docs#tag/Google-Play/paths/~1google-play~1reviews/get
        '''

        queries = as_list(query)
        wait_async = async_request or reviews_limit > 499 or reviews_limit == 0 or len(queries) > 10
        params = {
            'query': as_list(query),
            'limit': reviews_limit,
            'sort': sort,
            'cutoff': cutoff,
            'rating': rating,
            'language': language,
            'async': wait_async,
            'fields': parse_fields(fields),
            'ui': ui,
            'webhook': webhook,
        }

        return self._request('GET', '/google-play/reviews', wait_async=wait_async, async_request=async_request, params=params)

    def contacts_and_leads(self, query: Union[list, str], preferred_contacts: Optional[Union[list, str]] = None, contacts_per_company: int = 3,
       emails_per_contact: int = 1, skip_contacts: int = 0, general_emails: bool = False, fields: Union[list, str] = None,
       async_request: bool = False, ui: bool = False, webhook: Optional[str] = None) -> list:
        '''
            Contacts and Leads Scraper

            Returns emails, social links, phones, and other contacts from websites based on domain names, URLs.
            It supports batching by sending arrays with up to 250 queries.
            It allows multiple queries to be sent in one request and to save on network latency time.

                Parameters:
                    query (list | str): Company domains, URLs (e.g., 'outscraper.com', ['tesla.com', 'microsoft.com']).
                    fields (list | str): Defines which fields to include in each returned item.
                        By default, all fields are returned.
                    async_request (bool): The parameter defines the way you want to submit your task. It can be set to `True`
                        to submit your requests to Outscraper and retrieve them later with the Request Results endpoint, or `False` (default)
                        to open an HTTP connection and keep it open until you got your results.
                        Default: False.
                    preferred_contacts (list | str): Contact roles you want to prioritize
                        (e.g., 'influencers', 'technical', ['decision makers', 'sales']).
                        Default: None.
                    contacts_per_company (int): The parameter specifies the number of Contacts per one company.
                        Default: 3.
                    emails_per_contact (int): The parameter specifies the number of email addresses per one contact.
                        Default: 1.
                    skip_contacts (int): The parameter specifies the number of contacts to skip. It's commonly used in pagination.
                        Default: 0.
                    general_emails (bool): The parameter specifies whether to include only general email (info@, support@, etc.)
                        or only not general email (paul@, john@, etc.).
                        Default: False.
                    ui (bool): Execute as a UI task. Overrides async_request to True.
                        Default: False.
                    webhook (str): URL for callback notifications when a task completes.
                        Default: None.

                Returns:
                    list|dict: JSON result

            See: https://app.outscraper.com/api-docs#tag/Email-Related/paths/~1contacts-and-leads/get
        '''

        queries = as_list(query)
        wait_async = async_request or len(queries) > 1
        params = {
            'query': queries,
            'fields': parse_fields(fields),
            'async': wait_async,
            'preferred_contacts': as_list(preferred_contacts) if preferred_contacts else None,
            'contacts_per_company': contacts_per_company,
            'emails_per_contact': emails_per_contact,
            'skip_contacts': skip_contacts,
            'general_emails': general_emails,
            'ui': ui,
            'webhook': webhook
        }

        return self._request('GET', '/contacts-and-leads', wait_async=wait_async, async_request=async_request, params=params)

    def emails_and_contacts(self, query: Union[list, str], fields: Union[list, str] = None) -> list:
        '''
            Return email addresses, social links and phones from domains in seconds.

                    Parameters:
                            query (list | str): Domains or links (e.g., outscraper.com).
                            fields (list | str): Parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.

                    Returns:
                            list|dict: JSON result

            See: https://app.outscraper.com/api-docs#tag/Email-Related/paths/~1emails-and-contacts/get
        '''

        params = {
            'query': as_list(query),
            'fields': parse_fields(fields),
        }

        return self._request('GET', '/emails-and-contacts', wait_async=True, params=params)

    def phones_enricher(self, query: Union[list, str], fields: Union[list, str] = None) -> list:
        '''
            Returns phones carrier data (name/type), validates phones, ensures messages deliverability.

                    Parameters:
                            query (list | str): Phone number (e.g., +1 281 236 8208).
                            fields (list | str): parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.

                    Returns:
                            list|dict: JSON result

            See: https://app.outscraper.com/api-docs#tag/Phone-Related/paths/~1phones-enricher/get
        '''

        params = {
            'query': as_list(query),
            'fields': parse_fields(fields),
        }

        return self._request('GET', '/phones-enricher', wait_async=True, params=params)

    def amazon_products(self, query: Union[list, str], limit: int = 24, domain: str = 'amazon.com', postal_code: str = '11201', fields: Union[list, str] = None, async_request: bool = False,
        ui: bool = None, webhook: str = None
    ) -> Union[list, dict]:
        '''
            Amazon Products V2 (speed optimized)

            Returns information about products on Amazon.

                    Parameters:
                            query (list | str): Amazon product or summary pages URLs.
                            limit (int): The parameter specifies the limit of products to get from one query (in case of using summary pages).
                            domain (str): The parameter specifies Amazon domain to use ("amazon.com", "amazon.co.uk", "amazon.ca", "amazon.de", "amazon.es", "amazon.fr", "amazon.it", "amazon.in", "amazon.nl", "amazon.se", "amazon.sa", "amazon.com.mx", "amazon.com.br", "amazon.co.jp", "amazon.pl").
                            postal_code (str): The parameter specifies the postal code for delivery.
                            fields (list | str): Parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.
                            async_request (bool): Parameter defines the way you want to submit your task to Outscraper. It can be set to `False` (default) to send a task and wait until you got your results, or `True` to submit your task and retrieve the results later using a request ID with `get_request_archive`. Each response is available for `2` hours after a request has been completed.
                            ui (bool): Parameter defines whether a task will be executed as a UI task. This is commonly used when you want to create a regular platform task with API. Using this parameter overwrites the async_request parameter to `True`.
                            webhook (str): parameter defines the URL address (callback) to which Outscraper will create a POST request with a JSON body once a task/request is finished. Using this parameter overwrites the webhook from integrations.

                    Returns:
                            list|dict: JSON result

            See: https://app.outscraper.com/api-docs#tag/Amazon/paths/~1amazon~1products-v2/get
        '''

        queries = as_list(query)
        wait_async = async_request or (len(queries) > 1 and limit > 1)
        params = {
            'query': queries,
            'limit': limit,
            'domain': domain,
            'postal_code': postal_code,
            'async': wait_async,
            'fields': parse_fields(fields),
            'ui': ui,
            'webhook': webhook,
        }

        return self._request('GET', '/amazon/products-v2', wait_async=wait_async, async_request=async_request, params=params)

    def amazon_reviews(self, query: Union[list, str], limit: int = 10, sort: str = 'helpful', filter_by_reviewer: str = 'all_reviews',
        filter_by_star: str = 'all_stars', domain: str = None, fields: Union[list, str] = None, async_request: bool = False, ui: bool = None, webhook: str = None
    ) -> Union[list, dict]:
        '''
            Returns reviews from Amazon products.

                    Parameters:
                            query (list | str): You can use URLs or ASINs from Amazon products (e.g., https://www.amazon.com/dp/1612680194, 1612680194, etc.).
                            limit (int): Parameter specifies the limit of reviews to get from one query.
                            sort (str): Parameter specifies one of the sorting types. Available values: "helpful", and "recent".
                            filter_by_reviewer (str): The parameter specifies one of the reviewer filter types (All reviewers / Verified purchase only). Available values: "all_reviews", and "avp_only_reviews".
                            filter_by_star (str): The parameter specifies one of the filter types by stars. Available values: "all_stars", "five_star", "four_star", "three_star", "two_star", "one_star", "positive", and "critical".
                            domain (str): The parameter specifies Amazon domain to use ("amazon.com", "amazon.co.uk", "amazon.ca", "amazon.de", "amazon.es", "amazon.fr", "amazon.it", "amazon.in", "amazon.nl", "amazon.se", "amazon.sa", "amazon.com.mx", "amazon.com.br", "amazon.co.jp", "amazon.pl").
                            fields (list | str): Parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.
                            async_request (bool): Parameter defines the way you want to submit your task to Outscraper. It can be set to `False` (default) to send a task and wait until you got your results, or `True` to submit your task and retrieve the results later using a request ID with `get_request_archive`. Each response is available for `2` hours after a request has been completed.
                            ui (bool): Parameter defines whether a task will be executed as a UI task. This is commonly used when you want to create a regular platform task with API. Using this parameter overwrites the async_request parameter to `True`.
                            webhook (str): parameter defines the URL address (callback) to which Outscraper will create a POST request with a JSON body once a task/request is finished. Using this parameter overwrites the webhook from integrations.

                    Returns:
                            list|dict: JSON result

            See: https://app.outscraper.com/api-docs#tag/Amazon/paths/~1amazon~1reviews/get
        '''

        queries = as_list(query)
        wait_async = async_request or (len(queries) > 1 and limit > 10)
        params = {
            'query': queries,
            'limit': limit,
            'sort': sort,
            'filterByReviewer': filter_by_reviewer,
            'filterByStar': filter_by_star,
            'domain': domain,
            'async': wait_async,
            'fields': parse_fields(fields),
            'ui': ui,
            'webhook': webhook,
        }

        return self._request('GET', '/amazon/reviews', wait_async=wait_async, async_request=async_request, params=params)

    def yelp_search(self, query: Union[list, str], limit: int = 100,
        fields: Union[list, str] = None, async_request: bool = False, ui: bool = None, webhook: str = None
    ) -> Union[list, dict]:
        '''
            Yelp Search

            Return search results from Yelp.

                    Parameters:
                            query (list | str): parameter defines search links with search parameters (e.g., "https://www.yelp.com/search?find_desc=Restaurants&find_loc=San+Francisco%2C+CA"). Using a lists allows multiple queries (up to 250) to be sent in one request and save on network latency time.
                            limit (int): parameter specifies the limit of items to get from one query.
                            fields (list | str): parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.
                            async_request (bool): parameter defines the way you want to submit your task to Outscraper. It can be set to `False` (default) to send a task and wait until you got your results, or `True` to submit your task and retrieve the results later using a request ID with `get_request_archive`. Each response is available for `2` hours after a request has been completed.
                            ui (bool): parameter defines whether a task will be executed as a UI task. This is commonly used when you want to create a regular platform task with API. Using this parameter overwrites the async_request parameter to `True`.
                            webhook (str): parameter defines the URL address (callback) to which Outscraper will create a POST request with a JSON body once a task/request is finished. Using this parameter overwrites the webhook from integrations.

                    Returns:
                            list|dict: JSON result

            See: https://app.outscraper.com/api-docs#tag/Others/paths/~1yelp-search/get
        '''

        queries = as_list(query)
        wait_async = async_request or len(queries) > 10
        params = {
            'query': queries,
            'limit': limit,
            'async': wait_async,
            'fields': parse_fields(fields),
            'ui': ui,
            'webhook': webhook,
        }

        return self._request('GET', '/yelp-search', wait_async=wait_async, async_request=async_request, params=params)

    def yelp_reviews(self, query: Union[list, str], limit: int = 100, sort: str = 'relevance_desc', cutoff: int = None,
        fields: Union[list, str] = None, async_request: bool = False, ui: bool = None, webhook: str = None
    ) -> Union[list, dict]:
        '''
            Yelp Reviews

            Returns reviews from Yelp businesses.

                    Parameters:
                            query (list | str): parameter defines direct links, or IDs of any Yelp business (e.g., "https://www.yelp.com/biz/cancha-boutique-gastrobar-san-francisco", "eggcellent-waffles-san-francisco", "iXoLJWjbcXCO43RT-H0uQQ"). Using a lists allows multiple queries (up to 250) to be sent in one request and save on network latency time.
                            limit (int): parameter specifies the limit of reviews to get from one query.
                            sort (str): parameter specifies one of the sorting types. Available values: "relevance_desc", "date_desc", "date_asc", "rating_desc", "rating_asc", "elites_desc".
                            cutoff (int): parameter specifies the maximum timestamp value for reviews (oldest review). Using the "cutoff" parameter overwrites "sort" parameter to "date_desc".
                            fields (list | str): parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.
                            async_request (bool): parameter defines the way you want to submit your task to Outscraper. It can be set to `False` (default) to send a task and wait until you got your results, or `True` to submit your task and retrieve the results later using a request ID with `get_request_archive`. Each response is available for `2` hours after a request has been completed.
                            ui (bool): parameter defines whether a task will be executed as a UI task. This is commonly used when you want to create a regular platform task with API. Using this parameter overwrites the async_request parameter to `True`.
                            webhook (str): parameter defines the URL address (callback) to which Outscraper will create a POST request with a JSON body once a task/request is finished. Using this parameter overwrites the webhook from integrations.

                    Returns:
                            list|dict: JSON result

            See: https://app.outscraper.com/api-docs#tag/Reviews-and-Comments/paths/~1yelp~1reviews/get
        '''

        queries = as_list(query)
        wait_async = async_request or limit > 499 or len(queries) > 10
        params = {
            'query': queries,
            'limit': limit,
            'sort': sort,
            'cutoff': cutoff,
            'async': wait_async,
            'fields': parse_fields(fields),
            'ui': ui,
            'webhook': webhook,
        }

        return self._request('GET', '/yelp/reviews', wait_async=wait_async, async_request=async_request, params=params)

    def tripadvisor_reviews(self, query: Union[list, str], limit: int = 100, cutoff: int = None,
        fields: Union[list, str] = None, async_request: bool = False, ui: bool = None, webhook: str = None
    ) -> Union[list, dict]:
        '''
            Tripadvisor Reviews

            Returns reviews from Tripadvisor businesses.

                    Parameters:
                            query (list | str): parameter defines links to Tripadvisor pages (e.g., "https://www.tripadvisor.com/Restaurant_Review-g187147-d12947099-Reviews-Mayfair_Garden-Paris_Ile_de_France.html"). Using a lists allows multiple queries (up to 250) to be sent in one request and save on network latency time.
                            limit (int): parameter specifies the limit of reviews to get from one query.
                            fields (list | str): parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.
                            async_request (bool): parameter defines the way you want to submit your task to Outscraper. It can be set to `False` (default) to send a task and wait until you got your results, or `True` to submit your task and retrieve the results later using a request ID with `get_request_archive`. Each response is available for `2` hours after a request has been completed.
                            ui (bool): parameter defines whether a task will be executed as a UI task. This is commonly used when you want to create a regular platform task with API. Using this parameter overwrites the async_request parameter to `True`.
                            webhook (str): parameter defines the URL address (callback) to which Outscraper will create a POST request with a JSON body once a task/request is finished. Using this parameter overwrites the webhook from integrations.

                    Returns:
                            list|dict: JSON result

            See: https://app.outscraper.com/api-docs#tag/Reviews-and-Comments/paths/~1trustpilot~1reviews/get
        '''

        queries = as_list(query)
        wait_async = async_request or limit > 499 or len(queries) > 10
        params = {
            'query': queries,
            'limit': limit,
            'cutoff': cutoff,
            'async': wait_async,
            'fields': parse_fields(fields),
            'ui': ui,
            'webhook': webhook,
        }

        return self._request('GET', '/tripadvisor/reviews', wait_async=wait_async, async_request=async_request, params=params)

    def apple_store_reviews(self, query: Union[list, str], limit: int = 100, sort: str = 'mosthelpful', cutoff: int = None,
        fields: Union[list, str] = None, async_request: bool = False, ui: bool = None, webhook: str = None
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
                            webhook (str): parameter defines the URL address (callback) to which Outscraper will create a POST request with a JSON body once a task/request is finished. Using this parameter overwrites the webhook from integrations.

                    Returns:
                            list|dict: JSON result

            See: https://app.outscraper.com/api-docs#tag/Reviews-and-Comments/paths/~1appstore~1reviews/get
        '''

        queries = as_list(query)
        wait_async = async_request or limit > 499 or len(queries) > 10
        params = {
            'query': queries,
            'limit': limit,
            'sort': sort,
            'cutoff': cutoff,
            'async': wait_async,
            'fields': parse_fields(fields),
            'ui': ui,
            'webhook': webhook,
        }

        return self._request('GET', '/appstore/reviews', wait_async=wait_async, async_request=async_request, params=params)

    def youtube_comments(self, query: Union[list, str], per_query: int = 100, language: str = 'en', region: str = None,
        fields: Union[list, str] = None, async_request: bool = False, ui: bool = None, webhook: str = None
    ) -> list:
        '''
            Returns comments from YouTube videos.

                    Parameters:
                            query (list | str): video links or video IDs (e.g., https://www.youtube.com/watch?v=ph5pHgklaZ0, ph5pHgklaZ0). Using a lists allows multiple queries (up to 250) to be sent in one request and save on network latency time.
                            per_query (int): parameter specifies the limit of items to return from one query.
                            language (str): parameter specifies the language to use. Available values: "en", "de", "es", "es-419", "fr", "hr", "it", "nl", "pl", "pt-BR", "pt-PT", "vi", "tr", "ru", "ar", "th", "ko", "zh-CN", "zh-TW", "ja", "ach", "af", "ak", "ig", "az", "ban", "ceb", "xx-bork", "bs", "br", "ca", "cs", "sn", "co", "cy", "da", "yo", "et", "xx-elmer", "eo", "eu", "ee", "tl", "fil", "fo", "fy", "gaa", "ga", "gd", "gl", "gn", "xx-hacker", "ht", "ha", "haw", "bem", "rn", "id", "ia", "xh", "zu", "is", "jw", "rw", "sw", "tlh", "kg", "mfe", "kri", "la", "lv", "to", "lt", "ln", "loz", "lua", "lg", "hu", "mg", "mt", "mi", "ms", "pcm", "no", "nso", "ny", "nn", "uz", "oc", "om", "xx-pirate", "ro", "rm", "qu", "nyn", "crs", "sq", "sk", "sl", "so", "st", "sr-ME", "sr-Latn", "su", "fi", "sv", "tn", "tum", "tk", "tw", "wo", "el", "be", "bg", "ky", "kk", "mk", "mn", "sr", "tt", "tg", "uk", "ka", "hy", "yi", "iw", "ug", "ur", "ps", "sd", "fa", "ckb", "ti", "am", "ne", "mr", "hi", "bn", "pa", "gu", "or", "ta", "te", "kn", "ml", "si", "lo", "my", "km", "chr".
                            region (str): parameter specifies the region to use. Available values: "AF", "AL", "DZ", "AS", "AD", "AO", "AI", "AG", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BY", "BE", "BZ", "BJ", "BT", "BO", "BA", "BW", "BR", "VG", "BN", "BG", "BF", "BI", "KH", "CM", "CA", "CV", "CF", "TD", "CL", "CN", "CO", "CG", "CD", "CK", "CR", "CI", "HR", "CU", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "EE", "ET", "FJ", "FI", "FR", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GT", "GG", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KW", "KG", "LA", "LV", "LB", "LS", "LY", "LI", "LT", "LU", "MG", "MW", "MY", "MV", "ML", "MT", "MU", "MX", "FM", "MD", "MN", "ME", "MS", "MA", "MZ", "MM", "NA", "NR", "NP", "NL", "NZ", "NI", "NE", "NG", "NU", "MK", "NO", "OM", "PK", "PS", "PA", "PG", "PY", "PE", "PH", "PN", "PL", "PT", "PR", "QA", "RO", "RU", "RW", "WS", "SM", "ST", "SA", "SN", "RS", "SC", "SL", "SG", "SK", "SI", "SB", "SO", "ZA", "KR", "ES", "LK", "SH", "VC", "SR", "SE", "CH", "TW", "TJ", "TZ", "TH", "TL", "TG", "TO", "TT", "TN", "TR", "TM", "VI", "UG", "UA", "AE", "GB", "US", "UY", "UZ", "VU", "VE", "VN", "ZM", "ZW".
                            fields (list | str): parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.
                            async_request (bool): parameter defines the way you want to submit your task to Outscraper. It can be set to `False` (default) to send a task and wait until you got your results, or `True` to submit your task and retrieve the results later using a request ID with `get_request_archive`. Each response is available for `2` hours after a request has been completed.
                            ui (bool): parameter defines whether a task will be executed as a UI task. This is commonly used when you want to create a regular platform task with API. Using this parameter overwrites the async_request parameter to `True`.
                            webhook (str): parameter defines the URL address (callback) to which Outscraper will create a POST request with a JSON body once a task/request is finished. Using this parameter overwrites the webhook from integrations.

                    Returns:
                            list|dict: JSON result

            See: https://app.outscraper.com/api-docs#tag/YouTube/paths/~1youtube-comments/get
        '''

        queries = as_list(query)
        wait_async = async_request or per_query > 499 or len(queries) > 10
        params = {
            'query': queries,
            'perQuery': per_query,
            'language': language,
            'region': region,
            'async': wait_async,
            'fields': parse_fields(fields),
            'ui': ui,
            'webhook': webhook,
        }

        return self._request('GET', '/youtube-comments', wait_async=wait_async, async_request=async_request, params=params)

    def g2_reviews(self, query: Union[list, str], limit: int = 100, sort: str = 'g2_default', cutoff: int = None,
        fields: Union[list, str] = None, async_request: bool = False, ui: bool = None, webhook: str = None
    ) -> list:
        '''
            Returns reviews from a list of products.

                    Parameters:
                            query (list | str): Links to G2 products (e.g., https://www.g2.com/products/outscraper). Using a lists allows multiple queries (up to 250) to be sent in one request and save on network latency time.
                            limit (int): parameter specifies the limit of reviews to get from one query.
                            sort (str): parameter specifies one of the sorting types. Available values: "g2_default", "most_recent", "most_helpful", "highest_rated", "lowest_rated".
                            cutoff (int): parameter specifies the oldest timestamp value for items. Using the cutoff parameter overwrites sort parameter to most recent.
                            fields (list | str): parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.
                            async_request (bool): parameter defines the way you want to submit your task to Outscraper. It can be set to `False` (default) to send a task and wait until you got your results, or `True` to submit your task and retrieve the results later using a request ID with `get_request_archive`. Each response is available for `2` hours after a request has been completed.
                            ui (bool): parameter defines whether a task will be executed as a UI task. This is commonly used when you want to create a regular platform task with API. Using this parameter overwrites the async_request parameter to `True`.
                            webhook (str): parameter defines the URL address (callback) to which Outscraper will create a POST request with a JSON body once a task/request is finished. Using this parameter overwrites the webhook from integrations.

                    Returns:
                            list|dict: JSON result

            See: https://app.outscraper.com/api-docs#tag/YouTube/paths/~1g2~1reviews/get
        '''

        queries = as_list(query)
        wait_async = async_request or limit > 499 or len(queries) > 10
        params = {
            'query': queries,
            'limit': limit,
            'sort': sort,
            'cutoff': cutoff,
            'async': wait_async,
            'fields': parse_fields(fields),
            'ui': ui,
            'webhook': webhook,
        }

        return self._request('GET', '/g2/reviews', wait_async=wait_async, async_request=async_request, params=params)

    def trustpilot_reviews(self, query: Union[list, str], limit: int = 100, languages: str = 'default', sort: str = '',
        cutoff: int = None, fields: Union[list, str] = None, async_request: bool = False, ui: bool = None, webhook: str = None
    ) -> list:
        '''
            Returns reviews from Trustpilot businesses. In case no reviews were found by your search criteria, your search request will consume the usage of one review.

                    Parameters:
                            query (list | str): Links to Trustpilot pages or domain names (e.g., outscraper.com, https://www.trustpilot.com/review/outscraper.com).
                            limit (int): parameter specifies the limit of reviews to get from one query.
                            languages (str): parameter specifies one of the language filters. Available values: "default", "all", "en", "es", "de".
                            sort (str): parameter specifies one of the sorting types. Available values: "recency".
                            cutoff (int): parameter specifies the oldest timestamp value for items. Using the cutoff parameter overwrites sort parameter. Therefore, the latest records will be at the beginning (newest first).
                            fields (list | str): parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.
                            async_request (bool): parameter defines the way you want to submit your task to Outscraper. It can be set to `False` (default) to send a task and wait until you got your results, or `True` to submit your task and retrieve the results later using a request ID with `get_request_archive`. Each response is available for `2` hours after a request has been completed.
                            ui (bool): parameter defines whether a task will be executed as a UI task. This is commonly used when you want to create a regular platform task with API. Using this parameter overwrites the async_request parameter to `True`.
                            webhook (str): parameter defines the URL address (callback) to which Outscraper will create a POST request with a JSON body once a task/request is finished. Using this parameter overwrites the webhook from integrations.

                    Returns:
                            list|dict: JSON result

            See: https://app.outscraper.com/api-docs#tag/Trustpilot/paths/~1trustpilot~1reviews/get
        '''

        queries = as_list(query)
        wait_async = async_request or limit > 499 or len(queries) > 10
        params = {
            'query': queries,
            'limit': limit,
            'languages': languages,
            'sort': sort,
            'cutoff': cutoff,
            'async': wait_async,
            'fields': parse_fields(fields),
            'ui': ui,
            'webhook': webhook,
        }

        return self._request('GET', '/trustpilot/reviews', wait_async=wait_async, async_request=async_request, params=params)

    def glassdoor_reviews(self, query: Union[list, str], limit: int = 100, sort: str = 'DATE', cutoff: int = None,
        fields: Union[list, str] = None, async_request: bool = False, ui: bool = None, webhook: str = None
    ) -> list:
        '''
            Returns reviews from Glassdoor companies.

                    Parameters:
                            query (list | str): Direct links to any Glassdoor company (e.g., 'https://www.glassdoor.com/Reviews/Amazon-Reviews-E6036.htm). Using a lists allows multiple queries (up to 250) to be sent in one request and save on network latency time.
                            limit (int): parameter specifies the limit of reviews to get from one query.
                            sort (str): parameter specifies one of the sorting types. Available values: "DATE", "RELEVANCE".
                            cutoff (int): parameter specifies the oldest timestamp value for items. Using the cutoff parameter overwrites sort parameter. Therefore, the latest records will be at the beginning (newest first).
                            fields (list | str): parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.
                            async_request (bool): parameter defines the way you want to submit your task to Outscraper. It can be set to `False` (default) to send a task and wait until you got your results, or `True` to submit your task and retrieve the results later using a request ID with `get_request_archive`. Each response is available for `2` hours after a request has been completed.
                            ui (bool): parameter defines whether a task will be executed as a UI task. This is commonly used when you want to create a regular platform task with API. Using this parameter overwrites the async_request parameter to `True`.
                            webhook (str): parameter defines the URL address (callback) to which Outscraper will create a POST request with a JSON body once a task/request is finished. Using this parameter overwrites the webhook from integrations.

                    Returns:
                            list|dict: JSON result

            See: https://app.outscraper.com/api-docs#tag/Others/paths/~1glassdoor~1reviews/get
        '''

        queries = as_list(query)
        wait_async = async_request or limit > 499 or len(queries) > 10
        params = {
            'query': queries,
            'limit': limit,
            'sort': sort,
            'cutoff': cutoff,
            'async': wait_async,
            'fields': parse_fields(fields),
            'ui': ui,
            'webhook': webhook,
        }

        return self._request('GET', '/glassdoor/reviews', wait_async=wait_async, async_request=async_request, params=params)

    def capterra_reviews(self, query: Union[list, str], limit: int = 100, sort: str = 'MOST_HELPFUL', cutoff: int = None,
        language: str = 'en', region: str = None, fields: Union[list, str] = None, async_request: bool = False,
        ui: bool = None, webhook: str = None
    ) -> list:
        '''
            Returns reviews from Capterra.

                    Parameters:
                            query (list | str): Links to Capterra product pages (e.g., 'https://www.capterra.com/p/228041/Google-Maps-scraper/). Using a lists allows multiple queries (up to 250) to be sent in one request and save on network latency time.
                            limit (int): parameter specifies the limit of reviews to get from one query.
                            sort (str): parameter specifies one of the sorting types. Available values: "MOST_HELPFUL", "MOST_RECENT", "HIGHEST_RATING", "LOWEST_RATING".
                            cutoff (int): parameter specifies the oldest timestamp value for items. Using the cutoff parameter overwrites sort parameter. Therefore, the latest records will be at the beginning (newest first).
                            language (str): parameter specifies the language to use for website. Available values: "en", "de", "es", "es-419", "fr", "hr", "it", "nl", "pl", "pt-BR", "pt-PT", "vi", "tr", "ru", "ar", "th", "ko", "zh-CN", "zh-TW", "ja", "ach", "af", "ak", "ig", "az", "ban", "ceb", "xx-bork", "bs", "br", "ca", "cs", "sn", "co", "cy", "da", "yo", "et", "xx-elmer", "eo", "eu", "ee", "tl", "fil", "fo", "fy", "gaa", "ga", "gd", "gl", "gn", "xx-hacker", "ht", "ha", "haw", "bem", "rn", "id", "ia", "xh", "zu", "is", "jw", "rw", "sw", "tlh", "kg", "mfe", "kri", "la", "lv", "to", "lt", "ln", "loz", "lua", "lg", "hu", "mg", "mt", "mi", "ms", "pcm", "no", "nso", "ny", "nn", "uz", "oc", "om", "xx-pirate", "ro", "rm", "qu", "nyn", "crs", "sq", "sk", "sl", "so", "st", "sr-ME", "sr-Latn", "su", "fi", "sv", "tn", "tum", "tk", "tw", "wo", "el", "be", "bg", "ky", "kk", "mk", "mn", "sr", "tt", "tg", "uk", "ka", "hy", "yi", "iw", "ug", "ur", "ps", "sd", "fa", "ckb", "ti", "am", "ne", "mr", "hi", "bn", "pa", "gu", "or", "ta", "te", "kn", "ml", "si", "lo", "my", "km", "chr".
                            region (str): parameter specifies the country to use for website. It's recommended to use it for a better search experience. Available values: "AF", "AL", "DZ", "AS", "AD", "AO", "AI", "AG", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BY", "BE", "BZ", "BJ", "BT", "BO", "BA", "BW", "BR", "VG", "BN", "BG", "BF", "BI", "KH", "CM", "CA", "CV", "CF", "TD", "CL", "CN", "CO", "CG", "CD", "CK", "CR", "CI", "HR", "CU", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "EE", "ET", "FJ", "FI", "FR", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GT", "GG", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KW", "KG", "LA", "LV", "LB", "LS", "LY", "LI", "LT", "LU", "MG", "MW", "MY", "MV", "ML", "MT", "MU", "MX", "FM", "MD", "MN", "ME", "MS", "MA", "MQ", "MZ", "MM", "NA", "NR", "NP", "NL", "NZ", "NI", "NE", "NG", "NU", "MK", "NO", "OM", "PK", "PS", "PA", "PG", "PY", "PE", "PH", "PN", "PL", "PT", "PR", "QA", "RO", "RU", "RW", "WS", "SM", "ST", "SA", "SN", "RS", "SC", "SL", "SG", "SK", "SI", "SB", "SO", "ZA", "KR", "ES", "LK", "SH", "VC", "SR", "SE", "CH", "TW", "TJ", "TZ", "TH", "TL", "TG", "TO", "TT", "TN", "TR", "TM", "VI", "UG", "UA", "AE", "GB", "US", "UY", "UZ", "VU", "VE", "VN", "ZM", "ZW".
                            fields (list | str): parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.
                            async_request (bool): parameter defines the way you want to submit your task to Outscraper. It can be set to `False` (default) to send a task and wait until you got your results, or `True` to submit your task and retrieve the results later using a request ID with `get_request_archive`. Each response is available for `2` hours after a request has been completed.
                            ui (bool): parameter defines whether a task will be executed as a UI task. This is commonly used when you want to create a regular platform task with API. Using this parameter overwrites the async_request parameter to `True`.
                            webhook (str): parameter defines the URL address (callback) to which Outscraper will create a POST request with a JSON body once a task/request is finished. Using this parameter overwrites the webhook from integrations.

                    Returns:
                            list|dict: JSON result

            See: https://app.outscraper.com/api-docs#tag/Capterra/paths/~1capterra-reviews/get
        '''

        queries = as_list(query)
        wait_async = async_request or limit > 499 or len(queries) > 10
        params = {
            'query': queries,
            'limit': limit,
            'sort': sort,
            'cutoff': cutoff,
            'language': language,
            'region': region,
            'async': wait_async,
            'fields': parse_fields(fields),
            'ui': ui,
            'webhook': webhook,
        }

        return self._request('GET', '/capterra-reviews', wait_async=wait_async, async_request=async_request, params=params)

    def geocoding(self, query: Union[list, str], fields: Union[list, str] = None, async_request: bool = False, ui: bool = None, webhook: str = None) -> list:
        '''
            Translates human-readable addresses into locations on the map (latitude, longitude).

                    Parameters:
                            query (list | str): addresses specifying the location for which you want to get the coordinates (e.g., 321 California Ave, Palo Alto, CA 94306, Central Park, NY). Using a lists allows multiple queries (up to 250) to be sent in one request and save on network latency time.
                            fields (list | str): parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.
                            async_request (bool): parameter defines the way you want to submit your task to Outscraper. It can be set to `False` (default) to send a task and wait until you got your results, or `True` to submit your task and retrieve the results later using a request ID with `get_request_archive`. Each response is available for `2` hours after a request has been completed.
                            ui (bool): parameter defines whether a task will be executed as a UI task. This is commonly used when you want to create a regular platform task with API. Using this parameter overwrites the async_request parameter to `True`.
                            webhook (str): parameter defines the URL address (callback) to which Outscraper will create a POST request with a JSON body once a task/request is finished. Using this parameter overwrites the webhook from integrations.

                    Returns:
                            list|dict: JSON result

            See: https://app.outscraper.com/api-docs#tag/Other-Services/paths/~1geocoding/get
        '''

        queries = as_list(query)
        wait_async = async_request or len(queries) > 50
        params = {
            'query': queries,
            'async': wait_async,
            'fields': parse_fields(fields),
            'ui': ui,
            'webhook': webhook,
        }

        return self._request('GET', '/geocoding', wait_async=wait_async, async_request=async_request, params=params)

    def reverse_geocoding(self, query: Union[list, str], fields: Union[list, str] = None, async_request: bool = False, ui: bool = None, webhook: str = None) -> list:
        '''
            Translate locations on the map into human-readable addresses.

                    Parameters:
                            query (list | str): the latitude and longitude coordinates specifying the location for which you want the closest, human-readable address (e.g., 40.7624284 -73.973794, 37.427074,-122.1439166). Using a lists allows multiple queries (up to 250) to be sent in one request and save on network latency time.
                            fields (list | str): parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.
                            async_request (bool): parameter defines the way you want to submit your task to Outscraper. It can be set to `False` (default) to send a task and wait until you got your results, or `True` to submit your task and retrieve the results later using a request ID with `get_request_archive`. Each response is available for `2` hours after a request has been completed.
                            ui (bool): parameter defines whether a task will be executed as a UI task. This is commonly used when you want to create a regular platform task with API. Using this parameter overwrites the async_request parameter to `True`.
                            webhook (str): parameter defines the URL address (callback) to which Outscraper will create a POST request with a JSON body once a task/request is finished. Using this parameter overwrites the webhook from integrations.

                    Returns:
                            list|dict: JSON result

            See: https://app.outscraper.com/api-docs#tag/Other-Services/paths/~1reverse-geocoding/get
        '''

        queries = as_list(query)
        wait_async = async_request or len(queries) > 50
        params = {
            'query': queries,
            'async': wait_async,
            'fields': parse_fields(fields),
            'ui': ui,
            'webhook': webhook,
        }

        return self._request('GET', '/reverse-geocoding', wait_async=wait_async, async_request=async_request, params=params)

    def whitepages_phones(self, query: Union[list, str], fields: Union[list, str] = None, async_request: bool = False, ui: bool = None, webhook: str = None) -> Union[list, dict]:
        '''
            Phone Identity Finder (Whitepages)

            Returns insights about phone number owners (name, address, etc.) from Whitepages by phone number(s).

                    Parameters:
                            query (list | str): phone number(s), e.g. "+1 281 236 8208".
                            fields (list | str): parameter defines which fields you want to include with each item in the response. By default, it returns all fields.
                            async_request (bool): defines the way you want to submit your task to Outscraper. It can be set to `False` to send a task and wait for the results, or `True` to submit a task and retrieve results later using a request ID with `get_request_archive`.
                            ui (bool): parameter defines whether a task will be executed as a UI task. This is commonly used when you want to create a regular platform task with API. Using this parameter overwrites the async_request parameter to `True`.
                            webhook (str): defines the callback URL to which Outscraper will send a POST request with JSON once the task is finished.

                    Returns:
                            list|dict: JSON result

            See: https://app.outscraper.com/api-docs#tag/WhitePages/paths/~1whitepages-phones/get
        '''

        queries = as_list(query)
        wait_async = async_request or len(queries) > 1
        params = {
            'query': queries,
            'async': wait_async,
            'fields': parse_fields(fields),
            'ui': ui,
            'webhook': webhook,
        }

        return self._request('GET', '/whitepages-phones', wait_async=wait_async, async_request=async_request, params=params)

    def whitepages_addresses(self, query: Union[list, str], fields: Union[list, str] = None, async_request: bool = False, ui: bool = None, webhook: str = None) -> Union[list, dict]:
        '''
            Whitepages Addresses Scraper

            Returns insights about addresses and their residents.

                    Parameters:
                            query (list | str): address(es), e.g. "321 California Ave, Palo Alto, CA 94306".
                            fields (list | str): parameter defines which fields you want to include with each item in the response. By default, it returns all fields.
                            async_request (bool): defines the way you want to submit your task to Outscraper. It can be set to `False` to send a task and wait for the results, or `True` to submit a task and retrieve results later using a request ID with `get_request_archive`.
                            ui (bool): parameter defines whether a task will be executed as a UI task. This is commonly used when you want to create a regular platform task with API. Using this parameter overwrites the async_request parameter to `True`.
                            webhook (str): defines the callback URL to which Outscraper will send a POST request with JSON once the task is finished.

                    Returns:
                            list|dict: JSON result

            See: https://app.outscraper.com/api-docs#tag/WhitePages/paths/~1whitepages-addresses/get
        '''

        queries = as_list(query)
        wait_async = async_request or len(queries) > 1
        params = {
            'query': queries,
            'async': wait_async,
            'fields': parse_fields(fields),
            'ui': ui,
            'webhook': webhook,
        }

        return self._request('GET', '/whitepages-addresses', wait_async=wait_async, async_request=async_request, params=params)

    def company_insights(self, query: Union[list, str], fields: Union[list, str] = None, async_request: bool = False, enrichment: list = None)  -> Union[list, dict]:
        '''
            Company Insights Data

            Finds company details such as revenue, size, founding year, public status, etc.

                    Parameters:
                            query (list | str): Domains or websites (e.g., dominopark.com, https://www.esbnyc.com/).
                            fields (list | str): The parameter defines an enrichment or enrichments (e.g., enrichment=enrichment1&enrichment=enrichment2&enrichment=enrichment3) you want to apply to the results. Available values: domains_service, emails_validator_service, disposable_email_checker, company_insights_service, whatsapp_checker, phones_enricher_service, trustpilot_service, companies_data.
                            async_request (bool): defines the way you want to submit your task to Outscraper. It can be set to `False` to send a task and wait for the results, or `True` to submit a task and retrieve results later using a request ID with `get_request_archive`.
                            enrichment (list | str): The parameter defines an enrichment or enrichments (e.g., enrichment=enrichment1&enrichment=enrichment2&enrichment=enrichment3) you want to apply to the results. Available values: domains_service, emails_validator_service, disposable_email_checker, company_insights_service, whatsapp_checker, phones_enricher_service, trustpilot_service, companies_data.

                    Returns:
                            list|dict: JSON result

            See: https://app.outscraper.com/api-docs#tag/Other-Services/paths/~1company-insights/get
        '''

        queries = as_list(query)
        wait_async = async_request or len(queries) > 1
        params = {
            'query': queries,
            'fields': parse_fields(fields),
            'enrichment': as_list(enrichment) if enrichment else '',
            'async': wait_async,
        }

        return self._request('GET', '/company-insights', wait_async=wait_async, async_request=async_request, params=params)

    def validate_emails(self, query: Union[list, str], async_request: bool = False) -> Union[list, dict]:
        '''
            Email Address Verifier

            Allows to validate email addresses. Checks if emails are deliverable.

                    Parameters:
                            query (list | str): Email address (e.g., support@outscraper.com).
                            async_request (bool): defines the way you want to submit your task to Outscraper. It can be set to `False` to send a task and wait for the results, or `True` to submit a task and retrieve results later using a request ID with `get_request_archive`.

                    Returns:
                            list|dict: JSON result

            See: https://app.outscraper.com/api-docs#tag/Email-Related/paths/~1email-validator/get
        '''
        queries = as_list(query)
        wait_async = async_request or len(queries) > 1
        params = {
            'query': queries,
            'async': wait_async,
        }

        return self._request('GET', '/email-validator', wait_async=wait_async, async_request=async_request, params=params)

    def trustpilot_search(self, query: Union[list, str], limit: int = 100, skip: int = 0, enrichment: list = None, fields: Union[list, str] = None,  async_request: bool = False, ui: bool = None, webhook: str = None) -> Union[list, dict]:
        '''
            Trustpilot Search

            Returns search results from Trustpilot.

                    Parameters:
                            query (list | str): Company or category to search on Trustpilot (e.g., real estate).
                            limit (int): The parameter specifies the limit of items to get from one query.
                            skip (int): The parameter specifies the number of items to skip. It's commonly used in pagination.
                            enrichment (list | str): The parameter defines an enrichment or enrichments (e.g., enrichment=enrichment1&enrichment=enrichment2&enrichment=enrichment3) you want to apply to the results. Available values: domains_service, emails_validator_service, disposable_email_checker, company_insights_service, whatsapp_checker, phones_enricher_service, trustpilot_service, companies_data.
                            fields (list | str): The parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields. Use &fields=query,name to return only the specific ones.
                            async_request (bool): defines the way you want to submit your task to Outscraper. It can be set to `False` to send a task and wait for the results, or `True` to submit a task and retrieve results later using a request ID with `get_request_archive`.
                            ui (bool): parameter defines whether a task will be executed as a UI task. This is commonly used when you want to create a regular platform task with API. Using this parameter overwrites the async_request parameter to `True`.
                            webhook (str): defines the callback URL to which Outscraper will send a POST request with JSON once the task is finished.

                    Returns:
                            list|dict: JSON result

            See: https://app.outscraper.com/api-docs#tag/Businesses-and-POI/paths/~1trustpilot~1search/get
        '''

        queries = as_list(query)
        wait_async = async_request or len(queries) > 1
        params = {
            'query': queries,
            'limit': limit,
            'skip': skip,
            'enrichment': as_list(enrichment) if enrichment else '',
            'fields': parse_fields(fields),
            'async': wait_async,
            'ui': ui,
            'webhook': webhook
        }

        return self._request('GET', '/trustpilot', wait_async=wait_async, async_request=async_request, params=params)

    def trustpilot(self, query: Union[list, str], enrichment: list = None, fields: Union[list, str] = None, async_request: bool = False, ui: bool = None, webhook: str = None) -> Union[list, dict]:
        '''
            Trustpilot

            Returns data from Trustpilot businesses.

                    Parameters:
                            query (str | list): Links to Trustpilot pages or domain names (e.g., outscraper.com, https://www.trustpilot.com/review/outscraper.com).
                            enrichment (str | list): The parameter defines an enrichment or enrichments (e.g., enrichment=enrichment1&enrichment=enrichment2&enrichment=enrichment3) you want to apply to the results. Available values: domains_service, emails_validator_service, disposable_email_checker, company_insights_service, whatsapp_checker, phones_enricher_service, trustpilot_service, companies_data.
                            fields (str): The parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields. Use &fields=query,name to return only the specific ones..
                            async_request (bool): defines the way you want to submit your task to Outscraper. It can be set to `False` to send a task and wait for the results, or `True` to submit a task and retrieve results later using a request ID with `get_request_archive`.
                            ui (bool): parameter defines whether a task will be executed as a UI task. This is commonly used when you want to create a regular platform task with API. Using this parameter overwrites the async_request parameter to `True`.
                            webhook (str): defines the callback URL to which Outscraper will send a POST request with JSON once the task is finished.

                    Returns:
                            list|dict: JSON result

            See: https://app.outscraper.com/api-docs#tag/Trustpilot/paths/~1trustpilot/get
        '''

        queries = as_list(query)
        wait_async = async_request or len(queries) > 1
        params = {
            'query': queries,
            'enrichment': as_list(enrichment) if enrichment else '',
            'fields': parse_fields(fields),
            'async': wait_async,
            'ui': ui,
            'webhook': webhook
        }

        return self._request('GET', '/trustpilot', wait_async=wait_async, async_request=async_request, params=params)

    def similarweb(self, query: Union[list, str], fields: Union[list, str] = None, async_request: bool = False, ui: bool = None, webhook: str = None) -> Union[list, dict]:
        '''
            Similarweb

            Returns data from Similarweb businesses.

                    Parameters:
                            query (str | list): Domains or websites (e.g., apple.com, https://www.google.com/). It supports batching by sending arrays with up to 250 queries (e.g., query=text1&query=text2&query=text3). It allows multiple queries to be sent in one request and to save on network latency time.
                            fields (str): The parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields. Use &fields=query,name to return only the specific ones.
                            async_request (bool): defines the way you want to submit your task to Outscraper. It can be set to `False` to send a task and wait for the results, or `True` to submit a task and retrieve results later using a request ID with `get_request_archive`.
                            ui (bool): parameter defines whether a task will be executed as a UI task. This is commonly used when you want to create a regular platform task with API. Using this parameter overwrites the async_request parameter to `True`.
                            webhook (str): defines the callback URL to which Outscraper will send a POST request with JSON once the task is finished.

                    Returns:
                            list|dict: JSON result

            See: https://app.outscraper.com/api-docs#tag/Domain-Related/paths/~1similarweb/get
        '''

        queries = as_list(query)
        wait_async = async_request or len(queries) > 1
        params = {
            'query': queries,
            'fields': parse_fields(fields),
            'async': wait_async,
            'ui': ui,
            'webhook': webhook
        }

        return self._request('GET', '/similarweb', wait_async=wait_async, async_request=async_request, params=params)

    def company_websites_finder(self, query: Union[list, str], fields: Union[list, str] = None, async_request: bool = False, ui: bool = None, webhook: str = None) -> Union[list, dict]:
        '''
            Company Website Finder

            Returns data from Company Website Finder businesses.

                    Parameters:
                            query (str | list): Business names (e.g., Apple Inc, Microsoft Corporation, Tesla Motors). It supports batching by sending arrays with up to 250 queries (e.g., query=text1&query=text2&query=text3). It allows multiple queries to be sent in one request and to save on network latency time
                            fields (str): The parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields. Use &fields=query,name to return only the specific ones.
                            async_request (bool): defines the way you want to submit your task to Outscraper. It can be set to `False` to send a task and wait for the results, or `True` to submit a task and retrieve results later using a request ID with `get_request_archive`.
                            ui (bool): parameter defines whether a task will be executed as a UI task. This is commonly used when you want to create a regular platform task with API. Using this parameter overwrites the async_request parameter to `True`.
                            webhook (str): defines the callback URL to which Outscraper will send a POST request with JSON once the task is finished.

                    Returns:
                            list|dict: JSON result

            See: https://app.outscraper.com/api-docs#tag/Domain-Related/paths/~1company-website-finder/get
        '''

        queries = as_list(query)
        wait_async = async_request or len(queries) > 1
        params = {
            'query': queries,
            'fields': parse_fields(fields),
            'async': wait_async,
            'ui': ui,
            'webhook': webhook
        }

        return self._request('GET', '/company-website-finder', wait_async=wait_async, async_request=async_request, params=params)

    def yellowpages_search(self, query: Union[list, str], location: str = 'New York, NY', limit: int = 100, region: str = None,
        enrichment: list = None, fields: Union[list, str] = None, async_request: bool = True, ui: bool = None, webhook: str = None
    ) -> Union[list, dict]:
        '''
            Yellow Pages Search

            Returns search results from Yellow Pages.

                    Parameters:
                            query (list | str): Categories to search for (e.g., bars, restaurants, dentists). It supports batching by sending arrays with up to 250 queries (e.g., query=text1&query=text2&query=text3). It allows multiple queries to be sent in one request and to save on network latency time.
                            location (str): The parameter specifies where to search (e.g., New York, NY). Default: "New York, NY".
                            limit (int): The parameter specifies the limit of items to get from one query. Default: 100.
                            region (str): The parameter specifies the country to use for website. It's recommended to use it for a better search experience. Available values: "AF", "AL", "DZ", "AS", "AD", "AO", "AI", "AG", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BY", "BE", "BZ", "BJ", "BT", "BO", "BA", "BW", "BR", "VG", "BN", "BG", "BF", "BI", "KH", "CM", "CA", "CV", "CF", "TD", "CL", "CN", "CO", "CG", "CD", "CK", "CR", "CI", "HR", "CU", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "EE", "ET", "FJ", "FI", "FR", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GT", "GG", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KW", "KG", "LA", "LV", "LB", "LS", "LY", "LI", "LT", "LU", "MG", "MW", "MY", "MV", "ML", "MT", "MU", "MX", "FM", "MD", "MN", "ME", "MS", "MA", "MQ", "MZ", "MM", "NA", "NR", "NP", "NL", "NZ", "NI", "NE", "NG", "NU", "MK", "NO", "OM", "PK", "PS", "PA", "PG", "PY", "PE", "PH", "PN", "PL", "PT", "PR", "QA", "RO", "RU", "RW", "WS", "SM", "ST", "SA", "SN", "RS", "SC", "SL", "SG", "SK", "SI", "SB", "SO", "ZA", "KR", "ES", "LK", "SH", "VC", "SR", "SE", "CH", "TW", "TJ", "TZ", "TH", "TL", "TG", "TO", "TT", "TN", "TR", "TM", "VI", "UG", "UA", "AE", "GB", "US", "UY", "UZ", "VU", "VE", "VN", "ZM", "ZW".
                            enrichment (list): The parameter defines an enrichment or enrichments you want to apply to the results. Available values: "domains_service" (Emails & Contacts Scraper), "emails_validator_service" (Email Address Verifier), "company_websites_finder" (Company Website Finder), "disposable_email_checker" (Disposable Emails Checker), "company_insights_service" (Company Insights), "phones_enricher_service" (Phone Numbers Enricher), "trustpilot_service" (Trustpilot Scraper), "whitepages_phones" (Phone Identity Finder), "ai_chain_info" (Chain Info). Using enrichments increases the time of the response.
                            fields (list | str): The parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields.
                            async_request (bool): The parameter defines the way you want to submit your task to Outscraper. It can be set to `False` to open an HTTP connection and keep it open until you got your results, or `True` (default) to just submit your requests to Outscraper and retrieve them later with the Request Results endpoint. Default: True.
                            ui (bool): The parameter defines whether a task will be executed as a UI task. This is commonly used when you want to create a regular platform task with API. Using this parameter overwrites the async_request parameter to `True`. Default: False.
                            webhook (str): The parameter defines the URL address (callback) to which Outscraper will create a POST request with a JSON body once a task/request is finished. Using this parameter overwrites the webhook from integrations.

                    Returns:
                            list|dict: JSON result

            See: https://app.outscraper.com/api-docs#tag/Others/paths/~1yellowpages-search/get
        '''

        queries = as_list(query)
        wait_async = async_request or len(queries) > 10
        params = {
            'query': queries,
            'location': location,
            'limit': limit,
            'region': region,
            'enrichment': as_list(enrichment) if enrichment else '',
            'fields': parse_fields(fields),
            'async': wait_async,
            'ui': ui,
            'webhook': webhook,
        }

        return self._request('GET', '/yellowpages-search', wait_async=wait_async, async_request=async_request, params=params)
