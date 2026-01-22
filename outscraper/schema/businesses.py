from dataclasses import dataclass, field, fields as dc_fields
from typing import List, Optional, Any, Dict, Generic, TypeVar


T = TypeVar('T')


@dataclass
class BusinessFilters:
    os_ids: List[str] = field(default_factory=list)

    country_code: Optional[str] = None
    states: List[str] = field(default_factory=list)
    cities: List[str] = field(default_factory=list)
    counties: List[str] = field(default_factory=list)
    postal_codes: List[str] = field(default_factory=list)

    name: Optional[str] = None
    name_exclude: Optional[bool] = None

    types: List[str] = field(default_factory=list)
    ignore_types: List[str] = field(default_factory=list)

    rating: Optional[str] = None
    reviews: Optional[str] = None

    has_website: Optional[bool] = None
    domain: Optional[str] = None

    has_phone: Optional[bool] = None
    phone: Optional[str] = None

    business_statuses: List[str] = field(default_factory=list)

    area_service: Optional[bool] = None
    verified: Optional[bool] = None

    geo_filters: List[Dict[str, Any]] = field(default_factory=list)
    attributes: List[str] = field(default_factory=list)

    located_os_id: Optional[str] = None
    broad_match: Optional[bool] = None
    business_only: Optional[bool] = None

    def to_payload(self) -> Dict[str, Any]:
        data = self.__dict__.copy()
        return {k: v for k, v in data.items() if v not in (None, [], {}, '')}


@dataclass
class Business:
    # IDENTIFIERS
    os_id: Optional[str] = None
    place_id: Optional[str] = None
    google_id: Optional[str] = None

    name: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    rating: Optional[float] = None
    reviews: Optional[int] = None
    photo: Optional[str] = None
    types: Optional[List[str]] = None

    extra: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict) -> 'Business':
        allowed = {f.name for f in dc_fields(cls)}
        known = {k: v for k, v in data.items() if k in allowed and k != 'extra'}
        obj = cls(**known)
        obj.extra = data
        return obj

    def to_dict(self, *, include_extra: bool = True) -> Dict[str, Any]:
        result: Dict[str, Any] = {}

        for f in dc_fields(self):
            if f.name == 'extra':
                continue
            value = getattr(self, f.name)
            if value is not None:
                result[f.name] = value

        if include_extra:
            for k, v in self.extra.items():
                result.setdefault(k, v)

        return result


@dataclass
class Page(Generic[T]):
    items: List[T]
    next_cursor: Optional[str] = None
    has_more: bool = False

    @property
    def cursor(self) -> Optional[str]:
        return self.next_cursor


@dataclass
class BusinessSearchResult(Page[Business]):
    pass
