def handle_error_response(response, targetname):
    if response.status_code == 200:
        return

    print
    print("!!!!!!!!!ERROR IN REQUEST TO " + targetname + "!!!!!!!!!!!!!!!")
    if response.status_code == 400:
        print("400 - Bad Request. \nReason:", response.text)
    elif response.status_code == 401:
        print("Authentication Error. Most likely a problem with the config.")
        print(response.json()['error']['message'])
    else:
        print(response.status_code)
        print(response.text['error'])

    print
