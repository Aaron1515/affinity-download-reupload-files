from api_keys import *
from file_ids import *
from helper import *

import requests

total_ids_count = len(file_ids)
current_count = 0

log_file = open("log.csv", "w")
log_file.write("Orginal file ID, File name, Get file info status, Orginal org name, Orginal domain, Get orginal org status, Download file status, New org ID, New org name, New org domain, Get new org status, Upload file status, Upload file note")
log_file.write("\n")


for each_id in file_ids:

	current_count = current_count + 1
	print("ID: " + str(each_id) + " - " + str(current_count) + " / " + str(total_ids_count))
	## Get the file info
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


	## Get orginal org info
	orginal_org_response = requests.get('https://api.affinity.co/organizations/' + str(old_org_id), auth=('', first_api_key))

	if orginal_org_response.status_code == 200:

		old_org_domain = orginal_org_response.json()['domain']
		old_org_name = orginal_org_response.json()['name']
		
		if old_org_domain:
			print("")
		else:
			old_org_domain = " "

		# Write to org name, org domain, and status code to log
		log_file.write(", " + old_org_name + ", " + old_org_domain + ", " + "200")


		## Download and hyrdate the file
		download_file_response = requests.get('https://api.affinity.co/entity-files/download/' + str(each_id), auth=('', first_api_key))
		if download_file_response.status_code == 200:
			old_file_content = download_file_response.content
			# Write status code to log
			log_file.write(", " + str(download_file_response.status_code))
		else:
			print(download_file_response.json())
			break


		## Find new org info on the new instance
		if old_org_domain == " ":
			response = requests.get('https://api.affinity.co/organizations?term=' + old_org_name, auth=('', second_api_key))
			if response.json()['organizations'] == []:
				print("No org found, no domain found.")
				response = create_org_no_domain(old_org_name, second_api_key)

		else:
			response = requests.get('https://api.affinity.co/organizations?term=' + old_org_domain, auth=('', second_api_key))
			if response.json()['organizations'] == []:
				print("No org found, attempting to create new org.")
				response = create_org(old_org_name, old_org_domain, second_api_key)


		if response.status_code == 200:
			new_org_id = str(response.json()['organizations'][0]['id'])
			new_org_name = response.json()['organizations'][0]['name']
			new_org_domain = response.json()['organizations'][0]['domain']
			if not new_org_domain:
				print("")
			else:
				new_org_domain = "no domain found"
				print(new_org_domain)
		break
			# Write new org id, new org name, new org domain, and status code to log.
			log_file.write(", " + new_org_id + ", " + new_org_name + ", " + new_org_domain + ", " + "200")
		else:
			print(response.json())
			break

		## Upload file
		response = requests.post('https://api.affinity.co/entity-files', auth=('',second_api_key), params=({'organization_id': new_org_id}), files={'file': (file_name, old_file_content, old_file_header)})

		if response.status_code == 200:
			# Write to status code and response to log.
			log_file.write(", " + str(response.status_code) + ", " + str(response.json()))
		elif response.status_code == 422:
			print("File didn't upload. Orginal file ID is " + str(each_id))
			log_file.write(", " + str(response.status_code) + ", " + response.json()[0])
		else:
			print("Something went wrong with uploading the file. Orginal file ID is " + str(each_id))
			print(response.json())
			log_file.write(", " + str(response.status_code) + ", " + response.json()[0])
			break



	elif orginal_org_response.status_code == 422:
		log_file.write(", " + "Unable to find org" + ", " + "Unable to find org" + ", " + str(orginal_org_response.status_code))
		print("422 error: " + orginal_org_response.json())
		break
	else:
		print(orginal_org_response.json())
		break


	log_file.write("\n")

print("Done!")
log_file.close()


