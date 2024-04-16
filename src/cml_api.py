from src import constants as c

import requests
import os
import json
import yaml

##  DISABLE WARNINGS
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)



def get_token():
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    token = requests.post(
        c.CML_URL+'/authenticate',
        headers=headers,
        verify=False, 
        json={'username': os.environ.get('CML_USER'), 'password': os.environ.get('CML_PWD')}     
    )
    return token.json()


def get_labs(token):
    print('Getting labs..')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+token
    }
    params = {'show_all': True}
    response = requests.get(c.CML_URL+'/labs', verify=False, headers=headers, params=params)
    return response.json()


def get_lab_details(token, lab_id):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+token
    }
    params = {}
    response = requests.get(c.CML_URL+'/labs/'+lab_id, verify=False, headers=headers)
    return response.json()

def get_state(token, lab_id):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+token
    }
    params = {}
    response = requests.get(c.CML_URL+'/labs/'+lab_id+'/state', verify=False, headers=headers)
    return response.json()


def check_converged(token, lab_id):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+token
    }
    params = {}
    response = requests.get(c.CML_URL+'/labs/'+lab_id+'/check_if_converged', verify=False, headers=headers)
    return response.json()


def download_lab(token, lab_id):
    print('Downloading lab file..')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+token
    }
    params = {}
    response = requests.get(c.CML_URL+'/labs/'+lab_id+'/download', verify=False, headers=headers)
    return response


def start_lab(token, lab_id, lab_name):
    print('Starting lab: '+lab_name)
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer '+token
    }
    params = {}
    response = requests.put(c.CML_URL+'/labs/'+lab_id+'/start', verify=False, headers=headers)
    return response


def stop_lab(token, lab_id, lab_name):
    print('Stopping lab: '+lab_name)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+token
    }
    params = {}
    response = requests.put(c.CML_URL+'/labs/'+lab_id+'/stop', verify=False, headers=headers)
    return response


def extract_config(token, lab_id):
    print('Extracting config..')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+token
    }
    params = {}
    response = requests.put(c.CML_URL+'/labs/'+lab_id+'/extract_configuration', verify=False, headers=headers)
    return response


def main():
    token = get_token()
    labs = get_labs(token)
    for lab in labs:
        print(lab)
        state = get_state(token, lab)
        print(state)

    response = start_lab(token, '29c32a3a-8d55-4f3a-b998-f008c23c7279')
    print('Start lab:')
    response = get_state(token, '29c32a3a-8d55-4f3a-b998-f008c23c7279')
    print('State:')
    print(response)
    response = check_converged(token, '29c32a3a-8d55-4f3a-b998-f008c23c7279')
    print('Check converged:')
    print(response)
    response = download_lab(token, '29c32a3a-8d55-4f3a-b998-f008c23c7279')
    with open('lab.yaml', 'w') as file:
        file.write(response.text)



if __name__ == "__main__":
    main()
