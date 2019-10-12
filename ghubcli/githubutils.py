import os
import json
import webbrowser

def authorize(ghcli, reauthorize = False):
    if not os.path.isfile(ghcli.data_path / ghcli.auth_filename) or reauthorize:
        authorization_base_url = 'https://github.com/login/oauth/authorize'
        token_url = 'https://github.com/login/oauth/access_token'
        authorization_url, _ = ghcli.github.authorization_url(authorization_base_url)
        webbrowser.open(authorization_url)
        print("Please visit this site and grant access: {}".format(authorization_url))
        redirect_response = input("Please enter the URL you were redirected to after granting access: ")
        response = ghcli.github.fetch_token(token_url, client_secret=ghcli.client_secret, authorization_response=redirect_response)
        if not os.path.isdir(ghcli.data_path):
            os.makedirs(ghcli.data_path)
        data_file = open(ghcli.data_path / ghcli.auth_filename, "w+")
        json.dump(response, data_file)
        data_file.close()
        ghcli.oauth_data = response
    else:
        data_file = open(ghcli.data_path / ghcli.auth_filename, "r")
        oauth_data = json.loads(data_file.read())
        data_file.close()
        ghcli.oauth_data = oauth_data
        ghcli.github.token = oauth_data
