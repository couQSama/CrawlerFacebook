import os
import json
import random
from datetime import datetime

def delay(page):
    time_to_wait = random.uniform(1000, 2000)
    page.wait_for_timeout(time_to_wait)

def is_cookie_expired(cookie):
    if 'expires' in cookie:
        expires = datetime.fromtimestamp(cookie['expires'])
        return expires < datetime.now()
    return False

def save_post_incrementally(post, folder='.', default_filename='data', extension='json', indent=4, ensure_ascii=False):
    os.makedirs(folder, exist_ok=True)
    index = 1
    while True:
        filename = f'{default_filename}_{index}.{extension}'
        filepath = os.path.join(folder, filename)

        if not os.path.exists(filepath):
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(post, f, indent=indent, ensure_ascii=ensure_ascii)
            print(f"Data saved to {filepath}")
            break
        index += 1

def post_exists(post_url, url_filename='./data/post_url.json'):
    if not os.path.exists(url_filename):
        return False

    with open(url_filename, 'r', encoding='utf-8') as f:
        list_url = json.load(f)

    if post_url in list_url:
        return True

    return False

def save_post_url(post_url, url_filename='./data/post_url.json'):
    os.makedirs(os.path.dirname(url_filename), exist_ok=True)

    if os.path.exists(url_filename):
        with open(url_filename, 'r', encoding='utf-8') as f:
            list_url = json.load(f)
    else:
        list_url = []

    list_url.append(post_url)

    with open(url_filename, 'w', encoding='utf-8') as f:
        json.dump(list_url, f, indent=4, ensure_ascii=False)