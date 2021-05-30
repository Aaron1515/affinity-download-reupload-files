from api_keys import *
from file_ids import *
from helper import *

import requests

def create_org(name, domain, api_key):
	data = {
	  'name': name,
	  'domain': domain
	}
	return requests.post('https://api.affinity.co/organizations', data=data, auth=('', api_key))
	
def create_org_no_domain(name, api_key):
	data = {
	  'name': name
	}
	return requests.post('https://api.affinity.co/organizations', data=data, auth=('', api_key))

def search_for_org(str_term, api_key):
	return requests.get('https://api.affinity.co/organizations?term=' + str(str_term), auth=('', api_key))

def get_org_by_id(org_id, api_key):
	return requests.get('https://api.affinity.co/organizations/' + str(org_id), auth=('', api_key))

def get_file_info(file_id, api_key):
	return requests.get('https://api.affinity.co/entity-files/' + str(file_id), auth=('', api_key))

def download_file(file_id, api_key):
	return requests.get('https://api.affinity.co/entity-files/download/' + str(file_id), auth=('', api_key))