from datetime import datetime
import random

def delay(page):
    time_to_wait = random.uniform(1000, 2000)
    page.wait_for_timeout(time_to_wait)

def is_cookie_expired(cookie):
    if 'expires' in cookie:
        expires = datetime.fromtimestamp(cookie['expires'])
        return expires < datetime.now()
    return False
