import os

def get_api_credentials():
    api_user = os.getenv('SPEKTRIX_API_USER')
    api_key = os.getenv('SPEKTRIX_API_KEY')
    client_name = os.getenv('SPEKTRIX_CLIENT_NAME')
    return api_user, api_key, client_name

SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')