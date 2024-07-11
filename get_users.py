from env import portal_url, admin_username, admin_password
import utils
import requests

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



if __name__ == "__main__":
    token = utils.get_token(portal_url, admin_username, admin_password)

    if token:
        # Query all users
        all_users = query_all_users(portal_url, token)
        sorted_users = sorted(all_users, key=lambda user: user['username'])

        # Print the list of users
        for user in sorted_users:
            print(user['username'], user['fullName'], user['email'])
