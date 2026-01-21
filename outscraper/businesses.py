from __future__ import annotations
from typing import Iterator, Optional, Union, Mapping, Any

from .schema.businesses import Business, BusinessFilters, BusinessSearchResult


FiltersLike = Union[BusinessFilters, Mapping[str, Any], None]


class BusinessesAPI:
    def __init__(self, client: OutscraperClient) -> None:
        self._client = client

    def search(self, *, filters: FiltersLike = None, limit: int = 10, cursor: Optional[str] = None, include_total: bool = False,
        fields: Optional[list[str]] = None) -> BusinessSearchResult:

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

        response = self._client._request('POST', '/businesses', use_handle_response=False, json=payload)
        data = response.json()
        if data.get('error'):
            error_message = data.get('errorMessage')
            raise Exception(f'error: {error_message}')
        items = [Business.from_dict(i) for i in (data.get('items') or [])]

        return BusinessSearchResult(
            items=items,
            next_cursor=data.get('next_cursor'),
            has_more=bool(data.get('has_more')) or bool(data.get('next_cursor')),
        )

    def iter_search(self, *, filters: Optional[BusinessFilters] = None, limit: int = 10, start_cursor: Optional[str] = None,
        include_total: bool = False, fields: Optional[list[str]] = None) -> Iterator[Business]:

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

    def get_details(self, business_id: str, *, fields: Optional[list[str]] = None) -> Business:
        params = None
        if fields:
            params = {'fields': ','.join(fields)}

        resp = self._client._request('GET', f'/businesses/{business_id}', use_handle_response=False, params=params)
        data = resp.json()
        if data.get('error'):
            error_message = data.get('errorMessage')
            raise Exception(f'error: {error_message}')

        if not isinstance(data, dict):
            raise Exception(f'Unexpected response for /businesses/{business_id}: {type(data)!r}')

        return Business.from_dict(data)
