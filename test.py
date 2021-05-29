import requests




response = requests.get('https://api.affinity.co/entity-files/download/1520374' , auth=('',"OalyOEk3YNr2_NpcBcVD9662L8fTyJ8-Wrpdnzde4Eg"))

print(response.status_code)
print(response.json())
