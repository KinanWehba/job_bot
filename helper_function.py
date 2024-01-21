import requests
from typing import Dict
from dotenv import load_dotenv
import os
load_dotenv()


BASE_URL = os.getenv("BASE_URL")

def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    x = "\n".join(facts).join(["\n", "\n"])
    print(x)
    return x


def base_request(user_info,url,return_type='str'):
    r = requests.get(BASE_URL+url,params=user_info)
    r_code = r.status_code
    if r_code == 200 :
        if return_type == 'json':
            req = r.json()
            facts_to_str(req)
        else:
            req = r.text
        return  req
    else :
        return "خطا في الاتصال يرجى معاودة المحاولة مرة اخرى"