from api_keys import *
from file_ids import *
from helper import *

import requests

def create_org(name, domain, api_key):
	data = {
	  'name': name,
	  'domain': domain,
	}
	return requests.post('https://api.affinity.co/organizations', data=data, auth=('', api_key))

def create_org_no_domain(name, api_key):
	data = {
	  'name': name,
	}
	return requests.post('https://api.affinity.co/organizations', data=data, auth=('', api_key))
