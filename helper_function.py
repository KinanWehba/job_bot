import requests
from typing import Dict
from dotenv import load_dotenv
import os
load_dotenv()


BASE_URL = os.getenv("BASE_URL")

def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f"{key} - {value}" for key, value in user_data.items()]

    return "\n".join(facts).join(["\n", "\n"])


def base_request(user_info,url,return_type='str'):
    r = requests.get(BASE_URL+url,params=user_info)
    if return_type == 'json':
        req = r.text
    else:
        req = r.text
    print(req)
    return  req