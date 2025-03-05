from playwright.sync_api import sync_playwright
from login_facebook import login_facebook
from crawler import get_post_html
from extract_post_content import get_post_dict
from utils import save_post_incrementally, post_exists, save_post_url

if __name__ == '__main__':
    username = ''
    password = ''
    state_path = 'state.json'
    post_url = 'https://www.facebook.com/share/p/16NQdActFn/'

    if post_exists(post_url):
        print('Post already exists')
    else:
        save_post_url(post_url)
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = login_facebook(browser, username, password, state_path)
            html = get_post_html(page, post_url)
            browser.close()

        post = get_post_dict(html)
        post['post']['post_url'] = post_url
        save_post_incrementally(post, folder=r'.\data')


