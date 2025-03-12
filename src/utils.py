import os
import json
import random
from datetime import datetime

def delay(page):
    time_to_wait = random.uniform(1000, 1500)
    page.wait_for_timeout(time_to_wait)

def is_cookie_expired(cookie):
    if 'expires' in cookie:
        expires = datetime.fromtimestamp(cookie['expires'])
        return expires < datetime.now()
    return False

def save_post(post, folder, default_filename='data', extension='json', indent=4, ensure_ascii=False):
    os.makedirs(folder, exist_ok=True)
    filename = f'{default_filename}.{extension}'
    filepath = os.path.join(folder, filename)

    if not os.path.exists(filepath):
        list_post = [post]
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(list_post, f, indent=indent, ensure_ascii=ensure_ascii)
    else:
        with open(filepath, 'r', encoding='utf-8') as f:
            list_post = json.load(f)
        list_post.append(post)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(list_post, f, indent=4, ensure_ascii=False)

def post_exists(post_url, url_filename='../data/data.json'):
    if not os.path.exists(url_filename):
        return False

    with open(url_filename, 'r', encoding='utf-8') as f:
        posts = json.load(f)

    for post in posts:
        if post['post_url'] == post_url:
            return True

    return False

def save_html(html):
    with open('post.html', 'w', encoding='utf-8') as f:
        f.write(html)

def load_html():
    with open('post.html', 'r', encoding='utf-8') as f:
        html = f.read()
    return html