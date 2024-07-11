import utils
import json
from env import portal_url, RS_username, RS_password

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

def main():
    input_data = read_input()

    username = RS_username
    password = RS_password
    serviceUser = input_data.get("serviceUsername", "")
    servicePass = input_data.get("servicePassword", "")
    portal_root_token = portal_url
    portal_root_service = portal_url + "/sharing/rest"
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
