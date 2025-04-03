
"""Test json"""

import json
import pprint


def test_json():
    json_file = open('data/cefi_list.json', encoding="utf-8")

    assert json.load(json_file)