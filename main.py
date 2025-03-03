from playwright.sync_api import sync_playwright
from login_facebook import login_facebook

if __name__ == '__main__':
    username = 'huytin0392460501'
    password = 'chuong.05'
    state_path = 'state.json'
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = login_facebook(browser, username, password, state_path)
        print('Here')
        page.wait_for_timeout(120000)
