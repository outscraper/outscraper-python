from __future__ import annotations
from typing import Iterator, Optional, Union, Mapping, Any

from .schema.businesses import BusinessFilters, BusinessSearchResult


FiltersLike = Union[BusinessFilters, Mapping[str, Any], None]


class BusinessesAPI:
    def __init__(self, client: OutscraperClient) -> None:
        self._client = client

    def search(self, *, filters: FiltersLike = None, limit: int = 10, cursor: Optional[str] = None, include_total: bool = False,
        fields: Optional[list[str]] = None, query: str = '') -> BusinessSearchResult:
        '''
            Retrieve business records with optional enrichment data.

            This endpoint provides access to millions of business listings with support for
            pagination and selective data enrichment. Use `cursor` from the previous response
            to fetch the next page.

                Parameters:
                    filters (BusinessFilters | dict | None): Filtering criteria. You can pass either
                        BusinessFilters (recommended) or a raw dict matching the API schema.
                    limit (int): Maximum number of business records to return for this page.
                        Default: 10.
                    cursor (str | None): Cursor for pagination to retrieve the next set of results.
                        Default: None.
                    include_total (bool): Whether to include the total count of matching records in the response. This could increase response time.
                        Default: False.
                    fields (list[str] | None): List of fields to include in the response. If not specified, all fields will be returned.
                    query (str): natural language search.

                Returns:
                        BusinessSearchResult: Page of businesses with pagination info.

            See: https://app.outscraper.com/api-docs
        '''

        if limit < 1 or limit > 1000:
            raise ValueError('limit must be in range [1, 1000]')

        if filters is None:
            filters_payload = {}
        elif isinstance(filters, BusinessFilters):
            filters_payload = filters.to_payload()
        else:
            filters_payload = dict(filters)

        payload = {
            'filters': filters_payload,
            'limit': limit,
            'cursor': cursor,
            'include_total': include_total,
        }
        if fields:
            payload['fields'] = list(fields)

        if query:
            payload['query'] = query

        response = self._client._request('POST', '/businesses', use_handle_response=False, json=payload)
        data = response.json()

        if data.get('error'):
            error_message = data.get('errorMessage')
            raise Exception(f'error: {error_message}')

        return BusinessSearchResult(
            items=data.get('items') or [],
            next_cursor=data.get('next_cursor'),
            has_more=bool(data.get('has_more')) or bool(data.get('next_cursor')),
        )

    def iter_search(self, *, filters: FiltersLike = None, limit: int = 10, start_cursor: Optional[str] = None,
        include_total: bool = False, fields: Optional[list[str]] = None) -> Iterator[dict]:
        '''
            Iterate over businesses across all pages (auto-pagination).

            This is a convenience generator over `search()`:
            - calls search()
            - yields each Business from the returned page
            - continues while next_cursor/has_more indicates more pages

                Parameters:
                    filters (BusinessFilters | dict | None): Same as `search()`.
                    limit (int): Page size per request. Default: 10.
                    start_cursor (str | None): If provided, iteration starts from this cursor.
                        Default: None (start from first page).
                    include_total (bool): Passed to `search()` (if supported by API).
                        Default: False.
                    fields (list[str] | None): Passed to `search()`.

                Yields:
                        item (dict): Each business record from all pages.

            See: https://app.outscraper.com/api-docs
        '''

        cursor = start_cursor

        while True:
            business_search_result = self.search(filters=filters,
                limit=limit,
                cursor=cursor,
                include_total=include_total,
                fields=fields)

            for item in business_search_result.items:
                yield item
            if not business_search_result.next_cursor and not business_search_result.has_more:
                break

            cursor = business_search_result.next_cursor

    def get(self, business_id: str, *, fields: Optional[list[str]] = None) -> dict:
        '''
            Get Business Details

            Retrieves detailed information for a specific business by business_id.
            According to the API docs, business_id can be:
            - os_id
            - place_id
            - google_id

                Parameters:
                    business_id (str): Business identifier (os_id, place_id, or google_id).
                    fields (list[str] | None): List of fields to include in the response.
                        If not provided, API returns all fields.

                Returns:
                        data (dict): business with full details.

            See: https://app.outscraper.com/api-docs
        '''

        params = None
        if fields:
            params = {'fields': ','.join(fields)}

        resp = self._client._request('GET', f'/businesses/{business_id}', use_handle_response=False, params=params)
        data = resp.json()
        if data.get('error'):
            error_message = data.get('errorMessage')
            raise Exception(f'error: {error_message}')

        if not isinstance(data, dict):
            raise Exception(f'Unexpected response for /businesses/{business_id}: {type(data)}')

        return data
