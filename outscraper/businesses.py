from __future__ import annotations
from typing import Iterator, Optional, Union, Mapping, Any

from .schema.businesses import BusinessFilters, BusinessSearchResult


FiltersLike = Union[BusinessFilters, Mapping[str, Any], None]
EnrichmentsLike = Optional[Union[
    dict[str, Union[dict[str, Any], None, bool]],
    list[str],
    str,
]]


class BusinessesAPI:
    def __init__(self, client: OutscraperClient) -> None:
        self._client = client

    def search(self, *, filters: FiltersLike = None, limit: int = 10, cursor: Optional[str] = None, include_total: bool = False,
        fields: Optional[list[str]] = None, enrichments: EnrichmentsLike = None, query: str = '') -> BusinessSearchResult:
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
                    enrichments (dict | list[str] | str | None): Optional enrichments to apply.
                        Preferred format is dict with per-enrichment params:
                            {
                                "contacts_n_leads": {
                                    "contacts_per_company": 3,
                                    "emails_per_contact": 1,
                                },
                                "company_insights": {},
                            }
                        Backward-compatible formats are also supported:
                        - ["contacts_n_leads", "company_insights"]
                        - "contacts_n_leads"
                        In those forms, each enrichment is sent with empty params.
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

        normalized_enrichments = self._normalize_enrichments(enrichments=enrichments)

        if normalized_enrichments:
            payload['enrichments'] = normalized_enrichments

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
        include_total: bool = False, fields: Optional[list[str]] = None,
        enrichments: EnrichmentsLike = None, query: str = '') -> Iterator[dict]:
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
                    enrichments (dict | list[str] | str | None): Passed to `search()`.
                        Supports the same formats as `search()`.
                    query (str): Passed to `search()`.

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
                fields=fields,
                enrichments=enrichments,
                query=query)

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

    def _normalize_enrichments(self, enrichments: EnrichmentsLike = None) -> dict[str, dict[str, Any]]:
        normalized_enrichments = {}

        if enrichments is None:
            return normalized_enrichments

        if isinstance(enrichments, str):
            if not enrichments:
                raise ValueError('enrichment name must be a non-empty string')
            normalized_enrichments[enrichments] = {}

        elif isinstance(enrichments, dict):
            for name, params in enrichments.items():
                if not isinstance(name, str) or not name:
                    raise ValueError('enrichment name must be a non-empty string')

                if params is None or params is True:
                    params = {}
                elif params is False:
                    raise ValueError(f'enrichment "{name}" cannot be False; omit it instead')

                if not isinstance(params, dict):
                    raise ValueError(f'params for enrichment "{name}" must be a dict, None or True')

                normalized_enrichments[name] = dict(params)

        elif isinstance(enrichments, list):
            for name in enrichments:
                if not isinstance(name, str) or not name:
                    raise ValueError('enrichment name must be a non-empty string')
                normalized_enrichments[name] = {}
        else:
            raise ValueError('enrichments must be a dict, list[str], string, or None')

        contacts_n_leads = normalized_enrichments.get('contacts_n_leads', {})
        if 'contacts_per_company' in contacts_n_leads:
            contacts_per_company = contacts_n_leads['contacts_per_company']
            if not isinstance(contacts_per_company, int) or contacts_per_company < 1:
                raise ValueError('contacts_per_company must be an int >= 1')

        if 'emails_per_contact' in contacts_n_leads:
            emails_per_contact = contacts_n_leads['emails_per_contact']
            if not isinstance(emails_per_contact, int) or emails_per_contact < 1:
                raise ValueError('emails_per_contact must be an int >= 1')

        return normalized_enrichments
