import requests

# Configuration Section
email = ""  # Enter the email for your NP account
password = ""  # Enter the password for your NP account
gameNumber = ""  # Enter the game number of the game you want to pause and unpause

# Creates a session to store the login cookie in (needed to make any orders as player).
np = requests.session()

# Defines data for the login cookie requests. The request is sent straight to the NP server
url = "https://np.ironhelmet.com/arequest/login"
payload = "type=login&alias=" + email + "&password=" + password
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://np.ironhelmet.com',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://np.ironhelmet.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-GPC': '1',
    'TE': 'trailers'
}

# Requests the login cookie from the server and saves it to the np session from earlier
np.request("POST", url, headers=headers, data=payload)

# Redefines new data for the actual pause game order
url = "https://np.ironhelmet.com/trequest/order"
payload = "type=order&order=toggle_pause_game&version=&game_number=" + gameNumber
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://np.ironhelmet.com',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://np.ironhelmet.com/game/5879571561578496',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-GPC': '1',
    'TE': 'trailers'
}

# Uses the url, headers, and payload variables to make the pause game order.
# The np session from earlier automatically adds the login cookie to the request
np.request("POST", url, headers=headers, data=payload)
