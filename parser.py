import json


def parse_to_json(data_string):
    lines = data_string.strip().split('\n')
    result = {}

    for line in lines:
        key, value = line.split(': ', 1)
        result[key] = value.strip()

    return json.dumps(result, ensure_ascii=False)
