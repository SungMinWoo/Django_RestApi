import requests

endpoint = 'http://127.0.0.1:8000/api/products/6/delete'

get_response = requests.delete(endpoint) # Http request

print(get_response.status_code, get_response.status_code==204)