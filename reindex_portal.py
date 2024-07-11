import utils

# Configuration
portal_url = 'https://domain.com/arcgis'
admin_username = ''
admin_password = ''

token = utils.get_token(portal_url, admin_username, admin_password)
reindex_response = utils.reindex_portal(portal_url, token)
print("Portal reindex response:", reindex_response)