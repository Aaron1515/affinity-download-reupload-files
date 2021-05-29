from api_keys import *
from file_ids import *

import requests

total_ids_count = len(file_ids)
current_count = 0

log_file = open("log.csv", "w")
log_file.write("Orginal file ID, File name, Get file info status, Orginal org name, Orginal domain, Get orginal org status, Download file status, New org ID, New org name, New org domain, Get new org status, Upload file status, Note on uploaded file")
log_file.write("\n")

for each_id in file_ids:

	current_count = current_count + 1


	# Get the file info
	response = requests.get('https://api.affinity.co/entity-files/' + str(each_id), auth=('', first_api_key))

	if response.status_code == 200:
		file_name = response.json()['name']
		old_org_id = response.json()['organization_id']
		old_file_header = response.headers['content-type']
		log_file.write(str(each_id) + ", " + file_name + ", " + str(response.status_code))
	else:
		print(response.json())
		break


	# Get orginal org info
	response = requests.get('https://api.affinity.co/organizations/' + str(old_org_id), auth=('', first_api_key))

	if response.status_code == 200:
		old_org_domain = response.json()['domain']
		old_org_name = response.json()['name']

		# Write to log
		log_file.write(", " + old_org_name + ", " + old_org_domain + ", " + str(response.status_code))
	else:
		print(response.json())
		break




	# Download/hyrdate File
	response = requests.get('https://api.affinity.co/entity-files/download/' + str(each_id), auth=('', first_api_key))

	if response.status_code == 200:
		old_file_content = response.content
		log_file.write(", " + str(response.status_code))
	else:
		print(response.json())
		break



	# Find new org info
	response = requests.get('https://api.affinity.co/organizations?term=' + old_org_domain, auth=('', first_api_key))
	new_org_id = str(response.json()['organizations'][0]['id'])

	if response.status_code == 200:
		log_file.write(", " + str(response.json()['organizations'][0]['id']) + ", " + response.json()['organizations'][0]['name'] + ", " + response.json()['organizations'][0]['domain'] + ", " + str(response.status_code))
	else:
		print(response.json())
		break

	# Upload file
	response = requests.post('https://api.affinity.co/entity-files', auth=('',second_api_key), params=({'organization_id': new_org_id}), files={'file': (file_name, old_file_content, old_file_header)})
	# print(old_file_content)
	if response.status_code == 200:
		log_file.write(", " + str(response.status_code) + ", " + str(response.json()))
	else:
		print("Womething went wrong " + str(each_id))
		log_file.write(", " + str(response.status_code) + ", " + response.json()[0])
		break

	log_file.write("\n")

print("Done!")
log_file.close()


