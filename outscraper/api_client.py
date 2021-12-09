import requests
from time import sleep

from .utils import as_list


VERSION = '1.3.1'


class ApiClient(object):
    """Outscraper ApiClient - Python SDK that allows using Outscraper's services and Outscraper's API.
    ```python
    from outscraper import ApiClient
    api_cliet = ApiClient(api_key='SECRET_API_KEY')
    maps_result = api_cliet.google_maps_search('restaurants brooklyn usa')
    search_result = api_cliet.google_search('bitcoin')
    ```
    https://github.com/outscraper/google-maps-scraper-pyhton
    """

    _api_url = 'https://api.app.outscraper.com'
    _api_headers = {}

    _max_ttl = 60 * 12
    _requests_pause = 5

    def __init__(self, api_key: str, requests_pause: int = 5) -> None:
        self._api_headers = {
            'X-API-KEY': api_key,
            'client': f'Python SDK {VERSION}'
        }
        self._requests_pause = requests_pause

    def get_requests_history(self) -> list:
        '''
            Fetch up to 100 of your last requests.

                    Parameters:

                    Returns:
                            list: requests history
        '''
        response = requests.get(f'{self._api_url}/requests', headers=self._api_headers)

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
        '''
        response = requests.get(f'{self._api_url}/requests/{request_id}')

        if 199 < response.status_code < 300:
            return response.json()

        raise Exception(f'Response status code: {response.status_code}')

    def _wait_request_archive(self, request_id: str) -> dict:
        ttl = self._max_ttl / self._requests_pause

        while ttl > 0:
            ttl -= 1

            sleep(self._requests_pause)

            result = self.get_request_archive(request_id)
            if result['status'] != 'Pending': return result

        raise Exception('Timeout exceeded')

    def google_search(self, query: list, language: str = 'en', region: str = None) -> list:
        '''
            Get data from Google search

                    Parameters:
                            query (list | str): parameter defines the query or queries you want to search on Google. Using a lists allows multiple queries (up to 25) to be sent in one request and save on network latency time.
                            language (str): parameter specifies the language to use for Google. Available values: "en", "de", "es", "es-419", "fr", "hr", "it", "nl", "pl", "pt-BR", "pt-PT", "vi", "tr", "ru", "ar", "th", "ko", "zh-CN", "zh-TW", "ja", "ach", "af", "ak", "ig", "az", "ban", "ceb", "xx-bork", "bs", "br", "ca", "cs", "sn", "co", "cy", "da", "yo", "et", "xx-elmer", "eo", "eu", "ee", "tl", "fil", "fo", "fy", "gaa", "ga", "gd", "gl", "gn", "xx-hacker", "ht", "ha", "haw", "bem", "rn", "id", "ia", "xh", "zu", "is", "jw", "rw", "sw", "tlh", "kg", "mfe", "kri", "la", "lv", "to", "lt", "ln", "loz", "lua", "lg", "hu", "mg", "mt", "mi", "ms", "pcm", "no", "nso", "ny", "nn", "uz", "oc", "om", "xx-pirate", "ro", "rm", "qu", "nyn", "crs", "sq", "sk", "sl", "so", "st", "sr-ME", "sr-Latn", "su", "fi", "sv", "tn", "tum", "tk", "tw", "wo", "el", "be", "bg", "ky", "kk", "mk", "mn", "sr", "tt", "tg", "uk", "ka", "hy", "yi", "iw", "ug", "ur", "ps", "sd", "fa", "ckb", "ti", "am", "ne", "mr", "hi", "bn", "pa", "gu", "or", "ta", "te", "kn", "ml", "si", "lo", "my", "km", "chr".
                            region (str): parameter specifies the region to use for Google. Available values: "AF", "AL", "DZ", "AS", "AD", "AO", "AI", "AG", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BY", "BE", "BZ", "BJ", "BT", "BO", "BA", "BW", "BR", "VG", "BN", "BG", "BF", "BI", "KH", "CM", "CA", "CV", "CF", "TD", "CL", "CN", "CO", "CG", "CD", "CK", "CR", "CI", "HR", "CU", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "EE", "ET", "FJ", "FI", "FR", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GT", "GG", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KW", "KG", "LA", "LV", "LB", "LS", "LY", "LI", "LT", "LU", "MG", "MW", "MY", "MV", "ML", "MT", "MU", "MX", "FM", "MD", "MN", "ME", "MS", "MA", "MZ", "MM", "NA", "NR", "NP", "NL", "NZ", "NI", "NE", "NG", "NU", "MK", "NO", "OM", "PK", "PS", "PA", "PG", "PY", "PE", "PH", "PN", "PL", "PT", "PR", "QA", "RO", "RU", "RW", "WS", "SM", "ST", "SA", "SN", "RS", "SC", "SL", "SG", "SK", "SI", "SB", "SO", "ZA", "KR", "ES", "LK", "SH", "VC", "SR", "SE", "CH", "TW", "TJ", "TZ", "TH", "TL", "TG", "TO", "TT", "TN", "TR", "TM", "VI", "UG", "UA", "AE", "GB", "US", "UY", "UZ", "VU", "VE", "VN", "ZM", "ZW".

                    Returns:
                            list: json result
        '''
        response = requests.get(f'{self._api_url}/search', params={
            'query': as_list(query),
            'language': language,
            'region': region,
        }, headers=self._api_headers)

        if 199 < response.status_code < 300:
            return self._wait_request_archive(response.json()['id']).get('data', [])

        raise Exception(f'Response status code: {response.status_code}')

    def google_maps_search(self, query: list, limit: int = 500, extract_contacts: bool = False, drop_duplicates: bool = False,
        coordinates: str = None, language: str = 'en', region: str = None
    ) -> list:
        '''
            Get Google Maps Data

            Returns places from Google Maps based on a given search query (or many queries).
            The results from searches are the same as you would see by visiting a regular Google Maps site. However, in most cases, it's recommended to use locations inside queries (e.g., bars, NY, USA) as the IP addresses of Outscraper's servers might be located in different countries.

                    Parameters:
                            query (list | str): parameter defines the query you want to search. You can use anything that you would use on a regular Google Maps site. Additionally, you can use google_id, place_id or urls to Google Maps places. Using a lists allows multiple queries (up to 25) to be sent in one request and save on network latency time.
                            limit (int): parameter specifies the limit of places to take from one query search. The same as on Google Maps site, there are no more than 400 organizations per one query search. Use more precise categories (e.g., Asian restaurant, Italian restaurant) and/or locations (e.g., restaurants, Brooklyn 11211, restaurants, Brooklyn 11215) to overcome this limitation.
                            extract_contacts (bool): parameter specifies whether the bot will scrape additional data (emails, social links, site keywords…) from companies’ websites. It increases the time of the extraction.
                            drop_duplicates (bool): parameter specifies whether the bot will drop the same organizations from different queries. Using the parameter combines results from each query inside one big array.
                            coordinates (str): parameter defines the coordinates to use along with the query. Example: "@41.3954381,2.1628662,15.1z".
                            language (str): parameter specifies the language to use for Google. Available values: "en", "de", "es", "es-419", "fr", "hr", "it", "nl", "pl", "pt-BR", "pt-PT", "vi", "tr", "ru", "ar", "th", "ko", "zh-CN", "zh-TW", "ja", "ach", "af", "ak", "ig", "az", "ban", "ceb", "xx-bork", "bs", "br", "ca", "cs", "sn", "co", "cy", "da", "yo", "et", "xx-elmer", "eo", "eu", "ee", "tl", "fil", "fo", "fy", "gaa", "ga", "gd", "gl", "gn", "xx-hacker", "ht", "ha", "haw", "bem", "rn", "id", "ia", "xh", "zu", "is", "jw", "rw", "sw", "tlh", "kg", "mfe", "kri", "la", "lv", "to", "lt", "ln", "loz", "lua", "lg", "hu", "mg", "mt", "mi", "ms", "pcm", "no", "nso", "ny", "nn", "uz", "oc", "om", "xx-pirate", "ro", "rm", "qu", "nyn", "crs", "sq", "sk", "sl", "so", "st", "sr-ME", "sr-Latn", "su", "fi", "sv", "tn", "tum", "tk", "tw", "wo", "el", "be", "bg", "ky", "kk", "mk", "mn", "sr", "tt", "tg", "uk", "ka", "hy", "yi", "iw", "ug", "ur", "ps", "sd", "fa", "ckb", "ti", "am", "ne", "mr", "hi", "bn", "pa", "gu", "or", "ta", "te", "kn", "ml", "si", "lo", "my", "km", "chr".
                            region (str): parameter specifies the region to use for Google. Available values: "AF", "AL", "DZ", "AS", "AD", "AO", "AI", "AG", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BY", "BE", "BZ", "BJ", "BT", "BO", "BA", "BW", "BR", "VG", "BN", "BG", "BF", "BI", "KH", "CM", "CA", "CV", "CF", "TD", "CL", "CN", "CO", "CG", "CD", "CK", "CR", "CI", "HR", "CU", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "EE", "ET", "FJ", "FI", "FR", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GT", "GG", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KW", "KG", "LA", "LV", "LB", "LS", "LY", "LI", "LT", "LU", "MG", "MW", "MY", "MV", "ML", "MT", "MU", "MX", "FM", "MD", "MN", "ME", "MS", "MA", "MZ", "MM", "NA", "NR", "NP", "NL", "NZ", "NI", "NE", "NG", "NU", "MK", "NO", "OM", "PK", "PS", "PA", "PG", "PY", "PE", "PH", "PN", "PL", "PT", "PR", "QA", "RO", "RU", "RW", "WS", "SM", "ST", "SA", "SN", "RS", "SC", "SL", "SG", "SK", "SI", "SB", "SO", "ZA", "KR", "ES", "LK", "SH", "VC", "SR", "SE", "CH", "TW", "TJ", "TZ", "TH", "TL", "TG", "TO", "TT", "TN", "TR", "TM", "VI", "UG", "UA", "AE", "GB", "US", "UY", "UZ", "VU", "VE", "VN", "ZM", "ZW".

                    Returns:
                            list: json result
        '''
        response = requests.get(f'{self._api_url}/maps/search', params={
            'query': as_list(query),
            'coordinates': coordinates,
            'language': language,
            'region': region,
            'organizationsPerQueryLimit': limit,
            'extractContacts': extract_contacts,
            'dropDuplicates': drop_duplicates,
        }, headers=self._api_headers)

        if 199 < response.status_code < 300:
            return self._wait_request_archive(response.json()['id']).get('data', [])

        raise Exception(f'Response status code: {response.status_code}')

    def google_maps_search_v2(self, query: list, limit: int = 20, drop_duplicates: bool = False,
        language: str = 'en', region: str = None
    ) -> list:
        '''
            Get Google Maps Data V2 (speed optimized endpoint for real time data)

            Returns places from Google Maps based on a given search query (or many queries).
            The results from searches are the same as you would see by visiting a regular Google Maps site. However, in most cases, it's recommended to use locations inside queries (e.g., bars, NY, USA) as the IP addresses of Outscraper's servers might be located in different countries.
            This endpoint is optimized for fast responses and can be used as real time API. Set the limit parameter to 20 to achieve the maximum response speed.

                    Parameters:
                            query (list | str): parameter defines the query you want to search. You can use anything that you would use on a regular Google Maps site. Additionally, you can use google_id. The example of valid queries: Real estate agency, Rome, Italy, The NoMad Restaurant, NY, USA, restaurants, Brooklyn 11203, 0x886916e8bc273979:0x5141fcb11460b226, etc. Using a lists allows multiple queries (up to 25) to be sent in one request and save on network latency time.
                            limit (int): parameter specifies the limit of places to take from one query search. The same as on Google Maps site, there are no more than 400 organizations per one query search. Use more precise categories (e.g., Asian restaurant, Italian restaurant) and/or locations (e.g., restaurants, Brooklyn 11211, restaurants, Brooklyn 11215) to overcome this limitation.
                            drop_duplicates (bool): parameter specifies whether the bot will drop the same organizations from different queries. Using the parameter combines results from each query inside one big array.
                            language (str): parameter specifies the language to use for Google. Available values: "en", "de", "es", "es-419", "fr", "hr", "it", "nl", "pl", "pt-BR", "pt-PT", "vi", "tr", "ru", "ar", "th", "ko", "zh-CN", "zh-TW", "ja", "ach", "af", "ak", "ig", "az", "ban", "ceb", "xx-bork", "bs", "br", "ca", "cs", "sn", "co", "cy", "da", "yo", "et", "xx-elmer", "eo", "eu", "ee", "tl", "fil", "fo", "fy", "gaa", "ga", "gd", "gl", "gn", "xx-hacker", "ht", "ha", "haw", "bem", "rn", "id", "ia", "xh", "zu", "is", "jw", "rw", "sw", "tlh", "kg", "mfe", "kri", "la", "lv", "to", "lt", "ln", "loz", "lua", "lg", "hu", "mg", "mt", "mi", "ms", "pcm", "no", "nso", "ny", "nn", "uz", "oc", "om", "xx-pirate", "ro", "rm", "qu", "nyn", "crs", "sq", "sk", "sl", "so", "st", "sr-ME", "sr-Latn", "su", "fi", "sv", "tn", "tum", "tk", "tw", "wo", "el", "be", "bg", "ky", "kk", "mk", "mn", "sr", "tt", "tg", "uk", "ka", "hy", "yi", "iw", "ug", "ur", "ps", "sd", "fa", "ckb", "ti", "am", "ne", "mr", "hi", "bn", "pa", "gu", "or", "ta", "te", "kn", "ml", "si", "lo", "my", "km", "chr".
                            region (str): parameter specifies the region to use for Google. Available values: "AF", "AL", "DZ", "AS", "AD", "AO", "AI", "AG", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BY", "BE", "BZ", "BJ", "BT", "BO", "BA", "BW", "BR", "VG", "BN", "BG", "BF", "BI", "KH", "CM", "CA", "CV", "CF", "TD", "CL", "CN", "CO", "CG", "CD", "CK", "CR", "CI", "HR", "CU", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "EE", "ET", "FJ", "FI", "FR", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GT", "GG", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KW", "KG", "LA", "LV", "LB", "LS", "LY", "LI", "LT", "LU", "MG", "MW", "MY", "MV", "ML", "MT", "MU", "MX", "FM", "MD", "MN", "ME", "MS", "MA", "MZ", "MM", "NA", "NR", "NP", "NL", "NZ", "NI", "NE", "NG", "NU", "MK", "NO", "OM", "PK", "PS", "PA", "PG", "PY", "PE", "PH", "PN", "PL", "PT", "PR", "QA", "RO", "RU", "RW", "WS", "SM", "ST", "SA", "SN", "RS", "SC", "SL", "SG", "SK", "SI", "SB", "SO", "ZA", "KR", "ES", "LK", "SH", "VC", "SR", "SE", "CH", "TW", "TJ", "TZ", "TH", "TL", "TG", "TO", "TT", "TN", "TR", "TM", "VI", "UG", "UA", "AE", "GB", "US", "UY", "UZ", "VU", "VE", "VN", "ZM", "ZW".

                    Returns:
                            list: json result
        '''
        response = requests.get(f'{self._api_url}/maps/search-v2', params={
            'query': as_list(query),
            'language': language,
            'region': region,
            'organizationsPerQueryLimit': limit,
            'dropDuplicates': drop_duplicates,
            'async': False,
        }, headers=self._api_headers)

        if 199 < response.status_code < 300:
            return response.json().get('data', [])

        raise Exception(f'Response status code: {response.status_code}')

    def google_maps_directions(self, query: list, departure_time: int = None, finish_time: int = None, interval: int = 60,
        language: str = 'en', region: str = None, async_request: bool = False
    ) -> list:
        '''
            Get Google Maps Directions

            Returns directions between two points from Google Maps.

                    Parameters:
                            query (list | str): parameter defines the query that should contains "<origin> + <4 spaces> + <destination>". Using a lists allows multiple queries (up to 25) to be sent in one request and save on network latency time.
                            departure_time (int): parameter specifies the departure timestamp. The current timestamp is used when the value is not provided.
                            finish_time (int): parameter specifies the end departure timestamp. Using this parameter requires using the interval parameter.
                            interval (int): parameter specifies the interval to use between departure_time and finish_time.
                            language (str): parameter specifies the language to use for Google. Available values: "en", "de", "es", "es-419", "fr", "hr", "it", "nl", "pl", "pt-BR", "pt-PT", "vi", "tr", "ru", "ar", "th", "ko", "zh-CN", "zh-TW", "ja", "ach", "af", "ak", "ig", "az", "ban", "ceb", "xx-bork", "bs", "br", "ca", "cs", "sn", "co", "cy", "da", "yo", "et", "xx-elmer", "eo", "eu", "ee", "tl", "fil", "fo", "fy", "gaa", "ga", "gd", "gl", "gn", "xx-hacker", "ht", "ha", "haw", "bem", "rn", "id", "ia", "xh", "zu", "is", "jw", "rw", "sw", "tlh", "kg", "mfe", "kri", "la", "lv", "to", "lt", "ln", "loz", "lua", "lg", "hu", "mg", "mt", "mi", "ms", "pcm", "no", "nso", "ny", "nn", "uz", "oc", "om", "xx-pirate", "ro", "rm", "qu", "nyn", "crs", "sq", "sk", "sl", "so", "st", "sr-ME", "sr-Latn", "su", "fi", "sv", "tn", "tum", "tk", "tw", "wo", "el", "be", "bg", "ky", "kk", "mk", "mn", "sr", "tt", "tg", "uk", "ka", "hy", "yi", "iw", "ug", "ur", "ps", "sd", "fa", "ckb", "ti", "am", "ne", "mr", "hi", "bn", "pa", "gu", "or", "ta", "te", "kn", "ml", "si", "lo", "my", "km", "chr".
                            region (str): parameter specifies the region to use for Google. Available values: "AF", "AL", "DZ", "AS", "AD", "AO", "AI", "AG", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BY", "BE", "BZ", "BJ", "BT", "BO", "BA", "BW", "BR", "VG", "BN", "BG", "BF", "BI", "KH", "CM", "CA", "CV", "CF", "TD", "CL", "CN", "CO", "CG", "CD", "CK", "CR", "CI", "HR", "CU", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "EE", "ET", "FJ", "FI", "FR", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GT", "GG", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KW", "KG", "LA", "LV", "LB", "LS", "LY", "LI", "LT", "LU", "MG", "MW", "MY", "MV", "ML", "MT", "MU", "MX", "FM", "MD", "MN", "ME", "MS", "MA", "MZ", "MM", "NA", "NR", "NP", "NL", "NZ", "NI", "NE", "NG", "NU", "MK", "NO", "OM", "PK", "PS", "PA", "PG", "PY", "PE", "PH", "PN", "PL", "PT", "PR", "QA", "RO", "RU", "RW", "WS", "SM", "ST", "SA", "SN", "RS", "SC", "SL", "SG", "SK", "SI", "SB", "SO", "ZA", "KR", "ES", "LK", "SH", "VC", "SR", "SE", "CH", "TW", "TJ", "TZ", "TH", "TL", "TG", "TO", "TT", "TN", "TR", "TM", "VI", "UG", "UA", "AE", "GB", "US", "UY", "UZ", "VU", "VE", "VN", "ZM", "ZW".

                    Returns:
                            list: json result
        '''
        response = requests.get(f'{self._api_url}/maps/directions', params={
            'query': as_list(query),
            'departure_time': departure_time,
            'finish_time': finish_time,
            'language': language,
            'region': region,
            'async': async_request,
        }, headers=self._api_headers)

        if 199 < response.status_code < 300:
            if async_request:
                return response.json()

            return self._wait_request_archive(response.json()['id']).get('data', [])

        raise Exception(f'Response status code: {response.status_code}')

    def google_maps_reviews(self, query: list, reviewsLimit: int = 100, limit: int = 1, sort: str = 'most_relevant',
        skip: int = 0, start: int = None, cutoff: int = None, cutoff_rating: int = None, ignore_empty: bool = False,
        coordinates: str = None, language: str = 'en', region: str = None
    ) -> list:
        '''
            Get Google Maps Reviews

            Returns Google Maps reviews from places when using search queries (e.g., restaurants, Manhattan, NY, USA) or from a single place when using IDs or names (e.g., NoMad Restaurant, NY, USA, 0x886916e8bc273979:0x5141fcb11460b226, ChIJu7bMNFV-54gR-lrHScvPRX4).
            Places information will be returned as well in the case at least one review is found.

                    Parameters:
                            query (list | str): parameter defines the query you want to search. You can use anything that you would use on a regular Google Maps site. Additionally, you can use google_id, place_id or urls to Google Maps places. Using a lists allows multiple queries (up to 25) to be sent in one request and save on network latency time.
                            reviewsLimit (int): parameter specifies the limit of reviews to extract from one place.
                            limit (str): parameter specifies the limit of places to take from one query search.
                            sort (str): parameter specifies one of the sorting types. Available values: "most_relevant", "newest", "highest_rating", "lowest_rating".
                            skip (int): parameter specifies the number of items to skip. It's commonly used in pagination.
                            start (int): parameter specifies the start timestamp value for reviews. Using the start parameter overwrites sort parameter to newest.
                            cutoff (int): parameter specifies the maximum timestamp value for reviews. Using the cutoff parameter overwrites sort parameter to newest.
                            cutoff_rating (int): parameter specifies the maximum (for lowest_rating sorting) or minimum (for highest_rating sorting) rating for reviews. Using the cutoffRating requires sorting to be set to "lowest_rating" or "highest_rating".
                            ignore_empty (bool): parameter specifies whether to ignore reviews without text or not.
                            coordinates (str): parameter defines the coordinates of the location where you want your query to be applied. It has to be constructed in the next sequence: "@" + "latitude" + "," + "longitude" + "," + "zoom" (e.g. "@41.3954381,2.1628662,15.1z").
                            language (str): parameter specifies the language to use for Google. Available values: "en", "de", "es", "es-419", "fr", "hr", "it", "nl", "pl", "pt-BR", "pt-PT", "vi", "tr", "ru", "ar", "th", "ko", "zh-CN", "zh-TW", "ja", "ach", "af", "ak", "ig", "az", "ban", "ceb", "xx-bork", "bs", "br", "ca", "cs", "sn", "co", "cy", "da", "yo", "et", "xx-elmer", "eo", "eu", "ee", "tl", "fil", "fo", "fy", "gaa", "ga", "gd", "gl", "gn", "xx-hacker", "ht", "ha", "haw", "bem", "rn", "id", "ia", "xh", "zu", "is", "jw", "rw", "sw", "tlh", "kg", "mfe", "kri", "la", "lv", "to", "lt", "ln", "loz", "lua", "lg", "hu", "mg", "mt", "mi", "ms", "pcm", "no", "nso", "ny", "nn", "uz", "oc", "om", "xx-pirate", "ro", "rm", "qu", "nyn", "crs", "sq", "sk", "sl", "so", "st", "sr-ME", "sr-Latn", "su", "fi", "sv", "tn", "tum", "tk", "tw", "wo", "el", "be", "bg", "ky", "kk", "mk", "mn", "sr", "tt", "tg", "uk", "ka", "hy", "yi", "iw", "ug", "ur", "ps", "sd", "fa", "ckb", "ti", "am", "ne", "mr", "hi", "bn", "pa", "gu", "or", "ta", "te", "kn", "ml", "si", "lo", "my", "km", "chr".
                            region (str): parameter specifies the region to use for Google. Available values: "AF", "AL", "DZ", "AS", "AD", "AO", "AI", "AG", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BY", "BE", "BZ", "BJ", "BT", "BO", "BA", "BW", "BR", "VG", "BN", "BG", "BF", "BI", "KH", "CM", "CA", "CV", "CF", "TD", "CL", "CN", "CO", "CG", "CD", "CK", "CR", "CI", "HR", "CU", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "EE", "ET", "FJ", "FI", "FR", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GT", "GG", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KW", "KG", "LA", "LV", "LB", "LS", "LY", "LI", "LT", "LU", "MG", "MW", "MY", "MV", "ML", "MT", "MU", "MX", "FM", "MD", "MN", "ME", "MS", "MA", "MZ", "MM", "NA", "NR", "NP", "NL", "NZ", "NI", "NE", "NG", "NU", "MK", "NO", "OM", "PK", "PS", "PA", "PG", "PY", "PE", "PH", "PN", "PL", "PT", "PR", "QA", "RO", "RU", "RW", "WS", "SM", "ST", "SA", "SN", "RS", "SC", "SL", "SG", "SK", "SI", "SB", "SO", "ZA", "KR", "ES", "LK", "SH", "VC", "SR", "SE", "CH", "TW", "TJ", "TZ", "TH", "TL", "TG", "TO", "TT", "TN", "TR", "TM", "VI", "UG", "UA", "AE", "GB", "US", "UY", "UZ", "VU", "VE", "VN", "ZM", "ZW".

                    Returns:
                            list: json result
        '''
        response = requests.get(f'{self._api_url}/maps/reviews-v2', params={
            'query': as_list(query),
            'reviewsLimit': reviewsLimit,
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
        }, headers=self._api_headers)

        if 199 < response.status_code < 300:
            return self._wait_request_archive(response.json()['id']).get('data', [])

        raise Exception(f'Response status code: {response.status_code}')

    def google_maps_reviews_v3(self, query: list, reviewsLimit: int = 10, limit: int = 1, sort: str = 'most_relevant',
        skip: int = 0, start: int = None, cutoff: int = None, cutoff_rating: int = None, ignore_empty: bool = False,
        language: str = 'en', region: str = None
    ) -> list:
        '''
            Get Google Maps Reviews V3 (speed optimized endpoint for real time data)

            Returns Google Maps reviews from places when using search queries (e.g., restaurants, Manhattan, NY, USA) or from a single place when using Google IDs or names (e.g., NoMad Restaurant, NY, USA, 0x886916e8bc273979:0x5141fcb11460b226).
            Places information will be returned as well in the case at least one review is found.
            This endpoint is optimized for fast responses and can be used as real time API. Set the reviewsLimit parameter to 10 to achieve the maximum response speed.

                    Parameters:
                            query (list | str): parameter defines the query you want to search. You can use anything that you would use on a regular Google Maps site. Additionally, you can use google_id, place_id or urls to Google Maps places. Using a lists allows multiple queries (up to 25) to be sent in one request and save on network latency time.
                            reviewsLimit (int): parameter specifies the limit of reviews to extract from one place.
                            limit (str): parameter specifies the limit of places to take from one query search.
                            sort (str): parameter specifies one of the sorting types. Available values: "most_relevant", "newest", "highest_rating", "lowest_rating".
                            skip (int): parameter specifies the number of items to skip. It's commonly used in pagination.
                            start (int): parameter specifies the start timestamp value for reviews. Using the start parameter overwrites sort parameter to newest.
                            cutoff (int): parameter specifies the maximum timestamp value for reviews. Using the cutoff parameter overwrites sort parameter to newest.
                            cutoff_rating (int): parameter specifies the maximum (for lowest_rating sorting) or minimum (for highest_rating sorting) rating for reviews. Using the cutoffRating requires sorting to be set to "lowest_rating" or "highest_rating".
                            ignore_empty (bool): parameter specifies whether to ignore reviews without text or not.
                            coordinates (str): parameter defines the coordinates of the location where you want your query to be applied. It has to be constructed in the next sequence: "@" + "latitude" + "," + "longitude" + "," + "zoom" (e.g. "@41.3954381,2.1628662,15.1z").
                            language (str): parameter specifies the language to use for Google. Available values: "en", "de", "es", "es-419", "fr", "hr", "it", "nl", "pl", "pt-BR", "pt-PT", "vi", "tr", "ru", "ar", "th", "ko", "zh-CN", "zh-TW", "ja", "ach", "af", "ak", "ig", "az", "ban", "ceb", "xx-bork", "bs", "br", "ca", "cs", "sn", "co", "cy", "da", "yo", "et", "xx-elmer", "eo", "eu", "ee", "tl", "fil", "fo", "fy", "gaa", "ga", "gd", "gl", "gn", "xx-hacker", "ht", "ha", "haw", "bem", "rn", "id", "ia", "xh", "zu", "is", "jw", "rw", "sw", "tlh", "kg", "mfe", "kri", "la", "lv", "to", "lt", "ln", "loz", "lua", "lg", "hu", "mg", "mt", "mi", "ms", "pcm", "no", "nso", "ny", "nn", "uz", "oc", "om", "xx-pirate", "ro", "rm", "qu", "nyn", "crs", "sq", "sk", "sl", "so", "st", "sr-ME", "sr-Latn", "su", "fi", "sv", "tn", "tum", "tk", "tw", "wo", "el", "be", "bg", "ky", "kk", "mk", "mn", "sr", "tt", "tg", "uk", "ka", "hy", "yi", "iw", "ug", "ur", "ps", "sd", "fa", "ckb", "ti", "am", "ne", "mr", "hi", "bn", "pa", "gu", "or", "ta", "te", "kn", "ml", "si", "lo", "my", "km", "chr".
                            region (str): parameter specifies the region to use for Google. Available values: "AF", "AL", "DZ", "AS", "AD", "AO", "AI", "AG", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BY", "BE", "BZ", "BJ", "BT", "BO", "BA", "BW", "BR", "VG", "BN", "BG", "BF", "BI", "KH", "CM", "CA", "CV", "CF", "TD", "CL", "CN", "CO", "CG", "CD", "CK", "CR", "CI", "HR", "CU", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "EE", "ET", "FJ", "FI", "FR", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GT", "GG", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KW", "KG", "LA", "LV", "LB", "LS", "LY", "LI", "LT", "LU", "MG", "MW", "MY", "MV", "ML", "MT", "MU", "MX", "FM", "MD", "MN", "ME", "MS", "MA", "MZ", "MM", "NA", "NR", "NP", "NL", "NZ", "NI", "NE", "NG", "NU", "MK", "NO", "OM", "PK", "PS", "PA", "PG", "PY", "PE", "PH", "PN", "PL", "PT", "PR", "QA", "RO", "RU", "RW", "WS", "SM", "ST", "SA", "SN", "RS", "SC", "SL", "SG", "SK", "SI", "SB", "SO", "ZA", "KR", "ES", "LK", "SH", "VC", "SR", "SE", "CH", "TW", "TJ", "TZ", "TH", "TL", "TG", "TO", "TT", "TN", "TR", "TM", "VI", "UG", "UA", "AE", "GB", "US", "UY", "UZ", "VU", "VE", "VN", "ZM", "ZW".

                    Returns:
                            list: json result
        '''
        response = requests.get(f'{self._api_url}/maps/reviews-v3', params={
            'query': as_list(query),
            'reviewsLimit': reviewsLimit,
            'limit': limit,
            'sort': sort,
            'skip': skip,
            'start': start,
            'cutoff': cutoff,
            'cutoffRating': cutoff_rating,
            'ignoreEmpty': ignore_empty,
            'language': language,
            'region': region,
            'async': False,
        }, headers=self._api_headers)

        if 199 < response.status_code < 300:
            return response.json().get('data', [])

        raise Exception(f'Response status code: {response.status_code}')

    def google_maps_photos(self, query: list, photosLimit: int = 100, limit: int = 1, coordinates: str = None, language: str = 'en', region: str = None
    ) -> list:
        '''
            Get reviews from Google Maps

                    Parameters:
                            query (list | str): parameter defines the query you want to search. You can use anything that you would use on a regular Google Maps site. Additionally, you can use google_id, place_id or urls to Google Maps places. Using a lists allows multiple queries (up to 25) to be sent in one request and save on network latency time.
                            photosLimit (int): parameter specifies the limit of photos to extract from one place.
                            limit (str): parameter specifies the limit of places to take from one query search.
                            coordinates (str): parameter defines the coordinates of the location where you want your query to be applied. It has to be constructed in the next sequence: "@" + "latitude" + "," + "longitude" + "," + "zoom" (e.g. "@41.3954381,2.1628662,15.1z").
                            language (str): parameter specifies the language to use for Google. Available values: "en", "de", "es", "es-419", "fr", "hr", "it", "nl", "pl", "pt-BR", "pt-PT", "vi", "tr", "ru", "ar", "th", "ko", "zh-CN", "zh-TW", "ja", "ach", "af", "ak", "ig", "az", "ban", "ceb", "xx-bork", "bs", "br", "ca", "cs", "sn", "co", "cy", "da", "yo", "et", "xx-elmer", "eo", "eu", "ee", "tl", "fil", "fo", "fy", "gaa", "ga", "gd", "gl", "gn", "xx-hacker", "ht", "ha", "haw", "bem", "rn", "id", "ia", "xh", "zu", "is", "jw", "rw", "sw", "tlh", "kg", "mfe", "kri", "la", "lv", "to", "lt", "ln", "loz", "lua", "lg", "hu", "mg", "mt", "mi", "ms", "pcm", "no", "nso", "ny", "nn", "uz", "oc", "om", "xx-pirate", "ro", "rm", "qu", "nyn", "crs", "sq", "sk", "sl", "so", "st", "sr-ME", "sr-Latn", "su", "fi", "sv", "tn", "tum", "tk", "tw", "wo", "el", "be", "bg", "ky", "kk", "mk", "mn", "sr", "tt", "tg", "uk", "ka", "hy", "yi", "iw", "ug", "ur", "ps", "sd", "fa", "ckb", "ti", "am", "ne", "mr", "hi", "bn", "pa", "gu", "or", "ta", "te", "kn", "ml", "si", "lo", "my", "km", "chr".
                            region (str): parameter specifies the region to use for Google. Available values: "AF", "AL", "DZ", "AS", "AD", "AO", "AI", "AG", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BY", "BE", "BZ", "BJ", "BT", "BO", "BA", "BW", "BR", "VG", "BN", "BG", "BF", "BI", "KH", "CM", "CA", "CV", "CF", "TD", "CL", "CN", "CO", "CG", "CD", "CK", "CR", "CI", "HR", "CU", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "EE", "ET", "FJ", "FI", "FR", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GT", "GG", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KW", "KG", "LA", "LV", "LB", "LS", "LY", "LI", "LT", "LU", "MG", "MW", "MY", "MV", "ML", "MT", "MU", "MX", "FM", "MD", "MN", "ME", "MS", "MA", "MZ", "MM", "NA", "NR", "NP", "NL", "NZ", "NI", "NE", "NG", "NU", "MK", "NO", "OM", "PK", "PS", "PA", "PG", "PY", "PE", "PH", "PN", "PL", "PT", "PR", "QA", "RO", "RU", "RW", "WS", "SM", "ST", "SA", "SN", "RS", "SC", "SL", "SG", "SK", "SI", "SB", "SO", "ZA", "KR", "ES", "LK", "SH", "VC", "SR", "SE", "CH", "TW", "TJ", "TZ", "TH", "TL", "TG", "TO", "TT", "TN", "TR", "TM", "VI", "UG", "UA", "AE", "GB", "US", "UY", "UZ", "VU", "VE", "VN", "ZM", "ZW".

                    Returns:
                            list: json result
        '''
        response = requests.get(f'{self._api_url}/maps/photos', params={
            'query': as_list(query),
            'photosLimit': photosLimit,
            'limit': limit,
            'coordinates': coordinates,
            'language': language,
            'region': region,
        }, headers=self._api_headers)

        if 199 < response.status_code < 300:
            return self._wait_request_archive(response.json()['id']).get('data', [])

        raise Exception(f'Response status code: {response.status_code}')

    def google_maps_business_reviews(self, *args, **kwargs) -> list: # deprecated
        return self.google_maps_reviews(*args, **kwargs)

    def google_maps_reviews_v2(self, *args, **kwargs) -> list: # alias
        return self.google_maps_reviews(*args, **kwargs)

    def google_play_reviews(self, query: list, reviewsLimit: int = 100, sort: str = 'most_relevant', cutoff: int = None,
        rating: int = None, language: str = 'en'
    ) -> list:
        '''
            Returns reviews from any app/book/movie in the Google Play store.

                    Parameters:
                            query (list | str): you can use app IDs or direct links (e.g., https://play.google.com/store/apps/details?id=com.facebook.katana, com.facebook.katana). Using a lists allows multiple queries (up to 25) to be sent in one request and save on network latency time.
                            reviewsLimit (int): parameter specifies the limit of reviews to extract from one query.
                            sort (str): parameter specifies one of the sorting types. Available values: "most_relevant", "newest", "rating".
                            cutoff (int): parameter specifies the maximum timestamp value for reviews. Using the cutoff parameter overwrites sort parameter to "newest".
                            rating (int): Filter by a specific rating. Works only with "sort=rating".
                            language (str): parameter specifies the language to use for Google. Available values: "en", "de", "es", "es-419", "fr", "hr", "it", "nl", "pl", "pt-BR", "pt-PT", "vi", "tr", "ru", "ar", "th", "ko", "zh-CN", "zh-TW", "ja", "ach", "af", "ak", "ig", "az", "ban", "ceb", "xx-bork", "bs", "br", "ca", "cs", "sn", "co", "cy", "da", "yo", "et", "xx-elmer", "eo", "eu", "ee", "tl", "fil", "fo", "fy", "gaa", "ga", "gd", "gl", "gn", "xx-hacker", "ht", "ha", "haw", "bem", "rn", "id", "ia", "xh", "zu", "is", "jw", "rw", "sw", "tlh", "kg", "mfe", "kri", "la", "lv", "to", "lt", "ln", "loz", "lua", "lg", "hu", "mg", "mt", "mi", "ms", "pcm", "no", "nso", "ny", "nn", "uz", "oc", "om", "xx-pirate", "ro", "rm", "qu", "nyn", "crs", "sq", "sk", "sl", "so", "st", "sr-ME", "sr-Latn", "su", "fi", "sv", "tn", "tum", "tk", "tw", "wo", "el", "be", "bg", "ky", "kk", "mk", "mn", "sr", "tt", "tg", "uk", "ka", "hy", "yi", "iw", "ug", "ur", "ps", "sd", "fa", "ckb", "ti", "am", "ne", "mr", "hi", "bn", "pa", "gu", "or", "ta", "te", "kn", "ml", "si", "lo", "my", "km", "chr".

                    Returns:
                            list: json result
        '''
        response = requests.get(f'{self._api_url}/google-play/reviews', params={
            'query': as_list(query),
            'limit': reviewsLimit,
            'sort': sort,
            'cutoff': cutoff,
            'rating': rating,
            'language': language,
        }, headers=self._api_headers)

        if 199 < response.status_code < 300:
            return self._wait_request_archive(response.json()['id']).get('data', [])

        raise Exception(f'Response status code: {response.status_code}')

    def emails_and_contacts(self, query: list) -> list:
        '''
            Return email addresses, social links and phones from domains in seconds.

                    Parameters:
                            query (list | str): Domains or links (e.g., outscraper.com).

                    Returns:
                            list: json result
        '''
        response = requests.get(f'{self._api_url}/emails-and-contacts', params={
            'query': as_list(query),
        }, headers=self._api_headers)

        if 199 < response.status_code < 300:
            return self._wait_request_archive(response.json()['id']).get('data', [])

        raise Exception(f'Response status code: {response.status_code}')
