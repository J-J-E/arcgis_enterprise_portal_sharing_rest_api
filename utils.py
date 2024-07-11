import http.client
import urllib.parse
from urllib.parse import urlparse, urlunparse
import json
import requests

# Suppress only the single InsecureRequestWarning from urllib3
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def get_token(portal_url, admin_username, admin_password):
    token_url = f"{portal_url}/sharing/rest/generateToken"
    params = {
        'username': admin_username,
        'password': admin_password,
        'referer': 'https://www.arcgis.com',
        'f': 'json'
    }
    response = requests.post(token_url, data=params, verify=False)
    return response.json().get('token')

def query_all_users(portal_url, token):
    users_url = f"{portal_url}/sharing/rest/portals/self/users"
    params = {
        'f': 'json',
        'start': 1,
        'num': 100,  # Adjust the number of users per request as needed
        'token': token
    }
    all_users = []
    while True:
        response = requests.get(users_url, params=params, verify=False)
        data = response.json()
        all_users.extend(data.get('users', []))
        if data['nextStart'] == -1:
            break
        params['start'] = data['nextStart']
    return all_users

def get_user_items(portal_url, token, owner):
    search_url = f"{portal_url}/sharing/rest/search"
    params = {
        'q': f'owner:{owner}',
        'f': 'json',
        'num': 100,  # Adjust the number of items per request as needed
        'start': 0,  # Start index for pagination
        'token': token
    }
    all_results = []

    while True:
        response = requests.get(search_url, params=params, verify=False)
        data = response.json()
        results = data.get('results', [])

        if not results:
            break

        all_results.extend(results)
        params['start'] += params['num']

    return all_results

def update_service_url(portal_url, token, item_id, old_url, new_url, owner):
    item_data_url = f"{portal_url}/sharing/rest/content/items/{item_id}"
    params = {
        'f': 'json',
        'token': token
    }
    response = requests.get(item_data_url, params=params, verify=False)
    item_data = response.json()

    updated_url = item_data.get('url')  # Get the URL of the item

    if updated_url and old_url and old_url in updated_url:
        updated_url = updated_url.replace(old_url, new_url)

        # Update the item URL
        update_url = f"{portal_url}/sharing/rest/content/users/{owner}/items/{item_id}/update"
        update_params = {
            'f': 'json',
            'token': token,
            'url': updated_url
        }
        update_response = requests.post(update_url, data=update_params, verify=False)
        return update_response.json()

    return None

def reindex_portal(portal_url, token):
    reindex_url = f"{portal_url}/portaladmin/system/indexer/reindex"
    params = {
        'mode': 'FULL_MODE',
        'includes': '',
        'f': 'json'
    }
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.post(reindex_url, headers=headers, data=params, verify=False)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status": "failed", "message": response.text}

def post_request(url: str, data: dict) -> dict:
    parsed_url = urlparse(url)
    host = parsed_url.hostname
    path = parsed_url.path
    query = parsed_url.query
    path = urlunparse(('', '', path, '', query, ''))

    if host is None or path is None:
        raise ValueError(f"Failed to parse service url: {url}")

    encoded_data = urllib.parse.urlencode(data)
    conn = http.client.HTTPSConnection(host)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    conn.request('POST', path, encoded_data, headers)
    response = conn.getresponse()
    response_data = response.read().decode()
    parsed_response = json.loads(response_data)
    conn.close()

    if response.status != 200:
        raise ValueError(f"FAILED - https://{host}{path}")

    return parsed_response

def get_request(url: str) -> dict:
    parsed_url = urlparse(url)
    host = parsed_url.hostname
    path = parsed_url.path
    query = parsed_url.query
    path = urlunparse(('', '', path, '', query, ''))

    if host is None or path is None:
        raise ValueError(f"Failed to parse service url: {url}")

    conn = http.client.HTTPSConnection(host)
    conn.request('GET', path)
    response = conn.getresponse()
    response_data = response.read().decode()
    parsed_response = json.loads(response_data)
    conn.close()

    if response.status != 200:
        raise ValueError(f"FAILED - {url}")

    return parsed_response
