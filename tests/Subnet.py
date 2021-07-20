from os import CLD_CONTINUED
import os.path
import json
import re

from tests.Common import Common

class Key(Common):
    path = "subnets"

    json_content = Common.get_json_resource_content(path)

    name = json_content[path][0]["name"]
    id = json_content[path][0]["id"]
    href = json_content[path][0]["href"]