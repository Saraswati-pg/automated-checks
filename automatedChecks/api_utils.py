import requests

API_URL = "https://www.cea.gov.sg/aceas/api/internet/profile/v2/public-register/filter"

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Chrome",
}

def fetch_cea_profile(identifier):
    """Fetch agent profile details from CEA using the extracted license number."""
    payload = {
        "page": 1,
        "pageSize": 10,
        "sortAscFlag": True,
        "sort": "name",
    }

    if identifier.startswith("L"):
        payload["licenseNumber"] = identifier
        payload["profileType"] = 1
    elif identifier.startswith("R"):
        payload["registrationNumber"] = identifier
        payload["profileType"] = 2
    else:
        return "Invalid identifier format. It should start with 'L' or 'R'."

    try:
        response = requests.post(API_URL, json=payload, headers=HEADERS)
        print('came hereeeeee')
        if response.status_code == 200:
            return response.json().get('data', "No Data Found")
        return f"Failed: {response.status_code}, {response.text}"
    except requests.exceptions.RequestException as e:
        return f"API Error: {e}"
