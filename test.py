from api_keys import *
from file_ids import *
from helper import *

import requests


test = create_org("test", "testing.com", second_api_key)

test2 = create_org_no_domain("test", second_api_key)

print(test.status_code)
print(test.json())

print(test2.status_code)
print(test2.json())

