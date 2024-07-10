# File: register-service.py
import utils
import json
import getpass


def read_input() -> dict:
    input_file_path = "./register-service-input.json"
    try:
        with open(input_file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {input_file_path} was not found.")
    except json.JSONDecodeError:
        raise ValueError(f"Error decoding JSON from the file {input_file_path}.")


def get_user_credentials():
    try:
        username = input("Enter your username: ")
        if not username:
            raise ValueError("Username cannot be empty.")

        password = getpass.getpass("Enter your password: ")
        if not password:
            raise ValueError("Password cannot be empty.")

        return username, password
    except Exception as e:
        raise e


def main():
    input_data = read_input()

    if "username" in input_data and "password" in input_data:
        username = input_data["username"]
        password = input_data["password"]

        if username == "" or password == "":
            username, password = get_user_credentials()

    else:
        username, password = get_user_credentials()

    serviceUser = input_data.get("serviceUsername", "")
    servicePass = input_data.get("servicePassword", "")

    portal_root_token = input_data["portalRoot"]
    portal_root_service = input_data["portalRoot"] + "/sharing/rest"

    token = utils.get_token(portal_root_token, username, password)

    add_item_path = f"/content/users/{username}/addItem"
    add_item_url = portal_root_service + add_item_path

    for service in input_data["services"]:
        url = f"{service['url']}?f=json&token={token}"
        service_info = utils.get_request(url)

        register_service_body = {
            "url": service["url"],
            "title": service["title"],
            "typeKeywords": json.dumps(
                ["ArcGIS Server", "Data", "Feature Access", "Feature Service", "Service", "Singlelayer",
                 "Hosted Service", "Multilayer", "ArcGIS Server", "Data", "Feature Access", "Feature Service",
                 "Service", "Singlelayer", "Hosted Service"]),
            "storeAuth": True,
            "serviceInfo": service_info,
            "addAsBasemap": False,
            "username": username,
            "password": password,
            "serviceUsername": serviceUser,
            "servicePassword": servicePass,
            "spatialReference": 102100,
            "type": "Feature Service",
            "f": "json",
            "token": token,
        }

        response = utils.post_request(add_item_url, register_service_body)

        if "id" not in response:
            raise ValueError(f"Register service request returned unexpected response: {json.dumps(response)}");

        print(f"{service['title']} - {response['id']}")


if __name__ == "__main__":
    main()
