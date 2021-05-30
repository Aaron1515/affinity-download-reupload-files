from api_keys import *
from file_ids import *
from helper import *

import requests
import time

total_ids_count = len(file_ids)
current_count = 0

log_file = open("log.csv", "w")
log_file.write("Orginal file ID, File name, Get file info status, Orginal org name, Orginal domain, Get orginal org status, Download file status, New org ID, New org name, New org domain, Get new org status, Upload file status, Upload file note")
log_file.write("\n")


for each_id in file_ids:

	current_count = current_count + 1
	print("ID: " + str(each_id) + " - " + str(current_count) + " / " + str(total_ids_count))
	#1# Get the file info
	response = requests.get('https://api.affinity.co/entity-files/' + str(each_id), auth=('', first_api_key))

	if response.status_code == 200:
		file_name = response.json()['name']
		old_org_id = response.json()['organization_id']
		old_file_header = response.headers['content-type']
		# Write file id, file name, and status code to log
		log_file.write(str(each_id) + ", " + file_name + ", " + str(response.status_code))
	else:
		print("Get file info error - " + response.json())
		break


	#2# Get orginal org info
	orginal_org_response = get_org_by_id(old_org_id, first_api_key)
	# Unsuccessful at finding orginal org - in case the org has moved ID
	if "no longer exists as it has been merged into" in str(orginal_org_response.json()):
		log_file.write(", Org has moved to a new id, , , , , , , , , " + str(orginal_org_response.json()))
		log_file.write("\n")
		continue
	# Successfully org found orginal org info
	elif orginal_org_response.status_code == 200:
		old_org_domain = orginal_org_response.json()['domain']
		old_org_name = orginal_org_response.json()['name']
		# If domain is no present, replace it with empty string
		if not old_org_domain:
			old_org_domain = " "
		# Write org name, org domain, and status code to log
		log_file.write(", " + old_org_name + ", " + old_org_domain + ", " + "200")


		#3# Download and hyrdate the file
		download_file_response = download_file(each_id, first_api_key)
		if download_file_response.status_code == 200:
			old_file_content = download_file_response.content
			# Write status code to log
			log_file.write(", " + str(download_file_response.status_code))
		else:
			# Stop if unable to download file
			print(download_file_response.json())
			break


		#4# Find new org or create new org
		# Search for org without domain, create if not found
		if old_org_domain == " ":
			response = search_for_org(old_org_name, second_api_key)
			# Create org if no result is found
			if response.json()['organizations'] == []:
				print("No org found, create org with name only.")
				create_org_no_domain(old_org_name, second_api_key)
				time.sleep(10)
				response = search_for_org(old_org_name, second_api_key)
		# Search for go with domain, create if not found
		else:
			response = search_for_org(old_org_domain, second_api_key)
			# Create org if no result is found
			if response.json()['organizations'] == []:
				print("No org found, create org with domain and name.")
				create_org(old_org_name, old_org_domain, second_api_key)
				time.sleep(10)
				response = search_for_org(old_org_name, second_api_key)

		# Now that the new org is found, mapping variables
		if response.status_code == 200:
			new_org_id = str(response.json()['organizations'][0]['id'])
			new_org_name = response.json()['organizations'][0]['name']
			new_org_domain = response.json()['organizations'][0]['domain']
			if not new_org_domain:
				new_org_domain = " "
			# Write new org id, new org name, new org domain, and status code to log.
			log_file.write(", " + new_org_id + ", " + new_org_name + ", " + new_org_domain + ", " + "200")
		else:
			print(response.json())
			break

		#5# Upload file
		response = requests.post('https://api.affinity.co/entity-files', auth=('',second_api_key), params=({'organization_id': new_org_id}), files={'file': (file_name, old_file_content, old_file_header)})

		if response.status_code == 200:
			# Write to status code and response to log.
			log_file.write(", " + str(response.status_code) + ", " + str(response.json()))
		elif response.status_code == 422:
			print("File didn't upload. Orginal file ID is " + str(each_id))
			log_file.write(", " + str(response.status_code) + ", " + response.json()[0])
		else:
			print("Something went wrong with uploading the file.")
			print(response.json())
			print(response)
			log_file.write(", " + str(response.status_code) + ", " + response.json()[0])
			break

	elif orginal_org_response.status_code == 422:
		log_file.write(", " + "Unable to find org" + ", " + "Unable to find org" + ", " + str(orginal_org_response.status_code))
		print("422 error: Unable to find org")
		print(orginal_org_response.json())
		
	else:
		print(orginal_org_response.json())
		break

	log_file.write("\n")

print("Done!")
log_file.close()


