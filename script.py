import requests

first_api_key = ""
second_api_key = ""


file_id = "1499142"

response = requests.get('https://api.affinity.co/entity-files/' + file_id, auth=('', first_api_key))
print("************** Download File ***************")
old_org_id = str(response.json()['organization_id'])
print(str(response.status_code) + " - download file.")
file_name = response.json()['name']
print(file_name)
old_file_content = response.content
old_file_header = response.headers['content-type']
print("")

print("************** GET old org info ***************")
response = requests.get('https://api.affinity.co/organizations/' + old_org_id, auth=('', first_api_key))
old_org_domain = response.json()['domain']
print(str(response.status_code) + " - old org request.")
print("")


print("************** GET new org info ***************")
response = requests.get('https://api.affinity.co/organizations?term=' + old_org_domain, auth=('', first_api_key))
print(str(response.status_code) + " - new org request.")
new_org_id = str(response.json()['organizations'][0]['id'])



print("************** Upload file ***************")
response = requests.post('https://api.affinity.co/entity-files', auth=('',second_api_key), params=({'organization_id': new_org_id}), files={'file': (file_name, old_file_content, old_file_header)})
print(str(response.status_code) + " - upload status code.")
print(response.json())



