import requests
import json


def hubsolv_push(data: dict):
    """
    Dict must include the following values:
    data['HTTP-USERNAME'] = "username"
    data['HTTP-PASSWORD'] = "password"
    data['API-URL'] = "url"
    data['HUBSOLV-API-KEY'] = "key"

    Other understood static values include:

    lead_generator
    lead_source
    campaignid
    firstname
    lastname
    phone_home
    phone_mobile
    email
    employment_status

    :param data:
    :return:
    """
    username, password, url = data['HTTP-USERNAME'], data['HTTP-PASSWORD'], data['API-URL']
    enable_send = True

    if enable_send:
        return_this_id = 0
        response = requests.post(url, auth=(username, password), data=data)
        try:
            response_json = response.json()
            return_this_id = response_json['id']
        except json.decoder.JSONDecodeError:
            return {'result': False, 'data': response.text}
        return {'result': True, 'data': return_this_id}
    return {'result': False, 'data': 'enable is false'}
