import requests
from config import HIDDIFY_PANEL_URL, HIDDIFY_API_KEY

def create_user_and_get_configs(name: str, volume_gb: int) -> str:
    url = HIDDIFY_PANEL_URL.rstrip('/') + "/api/v2/users"
    headers = {
        "Hiddify-API-Key": HIDDIFY_API_KEY,
        "Accept": "application/json"
    }

    payload = {
        "name": name,
        "usage_limit_GB": volume_gb,
        "expired_at_days": 30,
        "telegram_id": ""
    }

    res = requests.post(url, headers=headers, json=payload)
    res.raise_for_status()
    user = res.json()

    user_id = user["uuid"]
    link_url = f"{HIDDIFY_PANEL_URL.rstrip('/')}/api/v2/user/{user_id}/all-configs/?is_sub_link=true"

    link_res = requests.get(link_url, headers=headers)
    link_res.raise_for_status()

    data = link_res.json()
    return data.get("sub_link", "لینک پیدا نشد")

