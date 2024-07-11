import utils

# Configuration
portal_url = 'https://domain.com/arcgis'
admin_username = ''
admin_password = ''
old_url = 'https://old-domain.com'
new_url = 'https://new-domain.com'
owners = [] #if list is left empty, all users from portal will be retrieved and iterated through

if __name__ == "__main__":
    token = utils.get_token(portal_url, admin_username, admin_password)
    all_items = []

    if not owners:
        all_users = utils.query_all_users(portal_url, token)
        owners = sorted([user['username'] for user in all_users])

    for owner in owners:
        print(f"getting content for user {owner}.")
        current_items = utils.get_user_items(portal_url, token, owner)
        print(f" - total items for user {owner}: {len(current_items)}")
        all_items.extend(current_items)

    print("\nUpdating Item URLs\n")

    for item in all_items:
        item_id = item['id']
        item_title = item['title']
        item_type = item['type']
        item_url = item.get('url', '')  # Ensure item_url is always a string

        update_result = utils.update_service_url(portal_url, token, item_id, old_url, new_url, owner)

        if update_result:
            print(f"Updated item {item_title} - {item_type} ({item_id})")
        else:
            print(f"No update necessary for item {item_title} - {item_type} ({item_id})")

    # After all updates, reindex the portal
    reindex_response = utils.reindex_portal(portal_url, token)
    print("Portal reindex response:", reindex_response)
