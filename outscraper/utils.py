from typing import Union

QUERY_DELIMITER = '    '

def as_list(value: Union[list, str]) -> list:
    if isinstance(value, list):
        return value
    else:
        return [value]


def parse_fields(fields: Union[list, str]) -> str:
    if isinstance(fields, list):
        return ','.join(fields)
    else:
        return fields


def format_direction_queries(q: Union[list, str]) -> list[str]:
    if isinstance(q, list):
        if all(isinstance(i, list) for i in q):
            return [QUERY_DELIMITER.join(pair) for pair in q]
        return q
    return [q]