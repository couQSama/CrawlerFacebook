from playwright.sync_api import sync_playwright
from login_facebook import login_facebook
from crawler import get_post_html
from extract_post_content import get_comment

if __name__ == '__main__':
    username = 'huytin0392460501'
    password = 'chuong.05'
    state_path = 'state.json'
    post_url = 'https://www.facebook.com/share/p/15vpNau8ye/'

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = login_facebook(browser, username, password, state_path)
        html = get_post_html(page, post_url)
        with open('post.htm', 'w', encoding='utf-8') as f:
            f.write(html)

        browser.close()

    with open('post.htm', 'r', encoding='utf-8') as f:
        post_html = f.read()
    get_comment(post_html)




