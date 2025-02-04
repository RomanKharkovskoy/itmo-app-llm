import json


def parse_to_json(id, text):
    result = {}
    result["id"] = id
    lines = text.split('\n')

    for line in lines:
        if not line.strip():
            continue
        if ': ' in line:
            key, value = line.split(': ', 1)
            result[key.lower()] = value.strip()

    return json.dumps(result, ensure_ascii=False)
