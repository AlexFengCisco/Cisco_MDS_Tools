import json
import requests
import base64
import ast

LOGON_URL = 'rest/logon'
dcnm_url='https://10.124.34.233/'

username='root'
password='1qaz@WSX'

headers = {'Content-Type': 'application/json; charset=utf8'}
verify = False
logon_url = dcnm_url + LOGON_URL
expiration_time='99999999'
dcnm_token = None
fdbid = None


def generate_encoded_credentials(username, password):
    """This generates the credentials"""
    data = {'Content-Type': 'application/json; charset=utf8'}
    credentials = username + ':' + password
    encoded = base64.b64encode(credentials.encode())
    print("//////////////")
    print(encoded)
    print(encoded.decode('ascii'))
    print("////////////")
    data.update({"Authorization": 'Basic ' + encoded.decode('ascii')})
    print(data)
    return data

def generate_dcnmtoken(headers,js_token=None):
    """This generates valid DCNM-Token for the encoded credentials"""
    dcnm_token = None
    payload = {'expirationTime': expiration_time}
    print("//////////Header///////")
    print(headers)
    try:
        print(logon_url)
        response = requests.post(
        logon_url,
        data=json.dumps(payload),
        headers=headers,
        verify=verify)
        if response.status_code == 200: # Successful token generation
            dcnm_token = ast.literal_eval(response.text)
    except:
        return None
    return dcnm_token


def create_zone(queryKey, zoneName, fabricDBID):
print("creating zone")
zone_url = self._dcnm_url + self.CREATE_ZONE
print(zone_url)
self._rest_api.headers['Content-Type'] = 'application/x-www-form-urlencoded'
payload = {}
payload['queryKey'] = queryKey
payload['zoneName'] = zoneName
payload['fabricDBID'] = fabricDBID
response = requests.post(zone_url, data=payload, headers=self._rest_api.headers, verify=self.verify)
print("printing response")
print(response.text)



credentials = generate_encoded_credentials(username,password)

print ('#'*100)
print credentials

dcnm_token = generate_dcnmtoken(credentials)

print ('#'*100)
print dcnm_token['Dcnm-Token']

headers['Dcnm-Token'] = dcnm_token['Dcnm-Token']

print headers

event_url='pmn/events'

response = requests.