import json


def pretty_print_dict(pydict: dict):
    print(json.dumps(pydict, sort_keys=True, indent=2))
