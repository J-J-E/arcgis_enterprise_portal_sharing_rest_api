from env import portal_url, admin_username, admin_password
import utils

if __name__ == "__main__":
    token = utils.get_token(portal_url, admin_username, admin_password)

    if token:
        # Query all users
        all_users = utils.query_all_users(portal_url, token)
        sorted_users = sorted(all_users, key=lambda user: user['username'])

        # Print the list of users
        for user in sorted_users:
            print(user['username'], user['fullName'], user['email'])
