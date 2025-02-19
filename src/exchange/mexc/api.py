BASE_URL = "https://api.mexc.com/api/v3"
import requests





def make_request( endpoint, params=None):
    url = f"{BASE_URL}/{endpoint}"
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        return "TIMEOUT" 
    except requests.exceptions.RequestException as e:
        return str(e)  