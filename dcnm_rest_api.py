'''
get fabric inventory switches result format


[{u'connUnitStatus': 4,
  u'displayValues': [u'dcn-mds9148s',
                     u'x.x.x.x',
                     u'Fabric_mds9513',
                     u'20:00:00:de:fb:2c:51:c0',
                     u'48', u'Cisco',
                     u'DS-C9148S',
                     u'6.2(11c)',
                     u'3 days,03:59:49'],
  u'upTime': 0,
  u'licenseDetail': u'Permanent',
  u'switchRole': u'',
  u'standbySupState': 1,
  u'logicalName': u'dcn-mds9148s',
  u'domain': None,
  u'modelType': 1491,
  u'numberOfPortsStr': u'48',
  u'activeSupSlot': 1,
  u'vsanWwn': None,
  u'mds': True,
  u'vsanWwnName': None,
  u'wwn': None,
  u'primaryIP': None,
  u'principal': None,
  u'index': 1,
  u'availPortsStr': u'0',
  u'fcoeEnabled': False,
  u'unmanagableCause': None,
  u'network': u'SAN',
  u'switchDbID': 1651640,
  u'licenseViolation': False,
  u'availPorts': 0,
  u'version': None,
  u'health': 65,
  u'location': u'',
  u'fid': 50,
  u'upTimeStr': u'3 days, 03:59:49',
  u'managable': True,
  u'nonMdsModel': u'DS-C9148S',
  u'npvEnabled': False,
  u'fex': False,
  u'colDBId': 0,
  u'numberOfPorts': 48,
  u'lan': False,
  u'domainID': 0,
  u'vendor': u'Cisco',
  u'mgmtAddress': None,
  u'healthStr': u'65%',
  u'swWwn': {u'value': u'20:00:00:de:fb:2c:51:c0'},
  u'usedPortsStr': u'0',
  u'vdcName': u'',
  u'pmCollect': False,
  u'membership': None,
  u'vdcMac': None,
  u'scope': u'Fabric_mds9513',
  u'memoryUsage': 18,
  u'linkName': None,
  u'cpuUsage': 0,
  u'fabricName': u'Fabric_mds9513',
  u'present': True,
  u'upTimeNumber': 3,
  u'name': None,
  u'displayHdrs': [u'Name', u'IP Address', u'Fabric', u'WWN', u'FC Ports', u'Vendor', u'Model', u'Release', u'UpTime'],
  u'usedPorts': 0,
  u'serialNumber': u'JPG20320059',
  u'lastScanTime': 1543469845465,
  u'vdcId': -1,
  u'username': u'admin',
  u'swWwnName': u'20:00:00:de:fb:2c:51:c0', u'contact': u'qifawu', u'status': u'Module Warning',
  u'beaconable': False,
  u'release': u'6.2(11c)',
  u'model': u'DS-C9148S',
  u'ipAddress': u'x.x.x.x',
  u'ports': 0}
  ]

'''


import json
import requests
import base64
import ast

LOGON_URL = 'rest/logon'
dcnm_url='https://dcnm-ip/'

username='sample'
password='sample'

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


credentials = generate_encoded_credentials(username,password)

print ('#'*100)
print credentials

dcnm_token = generate_dcnmtoken(credentials)

print ('#'*100)
print dcnm_token['Dcnm-Token']

headers['Dcnm-Token'] = dcnm_token['Dcnm-Token']

print headers



event_url=dcnm_url+'fm/fmrest/inventory/switches'

response = requests.get(event_url,headers=headers,verify=verify)



response_content=json.loads(response.text)


print response_content

for i in response_content:
    print "switch Name =" +i['logicalName']
    print "Switch modsel ="+ i['model']
    print "Fabric = " +i['fabricName']
    print "Ip Address ="+i['ipAddress']
    print "OS version ="+i['release']
    print ("-"*100)


'''
result as 

switch Name =dcn-mds9148s
Switch modsel =DS-C9148S
Fabric = Fabric_mds9513
Ip Address =x.x.x.x
OS version =6.2(11c)
----------------------------------------------------------------------------------------------------
switch Name =MDS-1
Switch modsel =DS-C9250i
Fabric = Fabric_MDS-1
Ip Address =x.x.x.x
OS version =6.2(19)
----------------------------------------------------------------------------------------------------
switch Name =MDS-2
Switch modsel =DS-C9250i
Fabric = Fabric_MDS-1
Ip Address =x.x.x.x
OS version =6.2(19)
----------------------------------------------------------------------------------------------------
switch Name =mds9513
Switch modsel =DS-C9513
Fabric = Fabric_mds9513
Ip Address =x.x.x.x
OS version =6.2(19)
----------------------------------------------------------------------------------------------------
switch Name =sw-core1-9710
Switch modsel =DS-C9710
Fabric = Fabric_mds9513
Ip Address =x.x.x.x
OS version =8.1(1a)
----------------------------------------------------------------------------------------------------

'''
