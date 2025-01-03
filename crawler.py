import json
import os.path
import sys
import argparse
from datetime import datetime
from random import randint, uniform
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

CSS_SELECTOR = {
    'text_most_relevant': "text='Phù hợp nhất'",
    'text_all_comment': "text='Tất cả bình luận'",
    'id_email_input': '#email',
    'id_pass_input': '#pass',
    'name_login_button': "button[name='login']",
    'role_navigation_div': "div[role='navigation']",
    'class_post_body_div': '.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6.xaci4zi.x129vozr',

    'class_view_replies_div': 'div.x1i10hfl.xjbqb8w.xjqpnuy.xa49m3k.xqeqjp1.x2hbi6w.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xdl72j9.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x2lwn1j.xeuugli.xexx8yu.x18d9i69.xkhd6sd.x1n2onr6.x16tdsg8.x1hl2dhg.xggy1nq.x1ja2u2z.x1t137rt.x1o1ewxj.x3x9cwd.x1e5q0jg.x13rtm0m.x3nfvp2.x87ps6o.x1lku1pv.x1a2a7pz.x6s0dn4.xi81zsa.x1q0g3np.x1iyjqo2.xs83m0k.xsyo7zv.x1mnrxsn[role="button"][tabindex="0"]',

    'class_view_more_div': '.x1i10hfl.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1sur9pj.xkrqix3.xzsf02u.x1s688f',
    'text_view_more': 'Xem thêm',
    'class_post_body_to_soup_div': '.html-div.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6.xqbnct6.xga75y6'
}

# Gọi delay sau mỗi thao tác để tránh bị phát hiện post và đợi load (chắc v :))
def delay(page):
    page.wait_for_timeout(randint(1000, 2000))
    page.wait_for_load_state(state='networkidle')
    page.wait_for_load_state(state='domcontentloaded')

def login_and_save_state(browser, username, password, is_headless=False):
    context = browser.new_context(headless=is_headless)
    page = context.new_page()
    page.goto('https://www.facebook.com/', timeout=120000)

    page.wait_for_selector('#email')
    page.wait_for_selector('#pass')

    page.type(CSS_SELECTOR['id_email_input'], username, delay=randint(50, 150))
    delay(page)
    page.type(CSS_SELECTOR['id_pass_input'], password, delay=randint(50, 150))
    delay(page)
    page.click(CSS_SELECTOR['name_login_button'])

    page.wait_for_selector(CSS_SELECTOR['role_navigation_div'], timeout=120000)
    context.storage_state(path='state.json')
    page.close()

def is_cookie_expired(cookie):
    if 'expires' in cookie:
        expires = datetime.fromtimestamp(cookie['expires'])
        return expires < datetime.now()
    return False

def get_html(username, password, post_url, is_headless=False):
    with sync_playwright() as p:
        print('Crawling html...')
        browser = p.chromium.launch(headless=is_headless)

        if os.path.exists('state.json'):
            with open('state.json', 'r') as f:
                state = json.load(f)
            cookies = state.get('cookie', [])

            if any(is_cookie_expired(cookie) for cookie in cookies):
                login_and_save_state(browser, username, password, is_headless)
        else:
            login_and_save_state(browser, username, password)

        context = browser.new_context(storage_state='state.json')
        page = context.new_page()

        # Open post
        page.goto(post_url, timeout=120000, wait_until='domcontentloaded')

        # Nhấn nút Phù hợp nhất và Tất cả bình luận để lấy hết bình luận
        page.locator(CSS_SELECTOR['text_most_relevant']).click()
        delay(page)
        page.locator(CSS_SELECTOR['text_all_comment']).click()
        delay(page)

        # Di chuột ra giữa để cuộn
        viewport_width = 1280
        viewport_height = 800
        center_x = viewport_width // 2
        center_y = viewport_height // 2
        page.mouse.move(center_x, center_y)

        # Lấy body của post (chiều cao của body phải thay đổi khi cuộn xuống để load cmt)
        post_body = page.locator(CSS_SELECTOR['class_post_body_div'])
        old_height = 0
        new_height = post_body.bounding_box()['height']

        # Cuộn xuống cho đến khi chiều cao ko còn thay đổi == hết cmt để load
        while old_height != new_height:
            while True:
                while True:
                    view_more_buttons = page.get_by_role('button', name='Xem thêm')
                    button_count = view_more_buttons.count()
                    print(f'more:{button_count}')
                    if button_count == 0:
                        break

                    button = view_more_buttons.nth(0)
                    button.click(force=True)
                    delay(page)
                # Click vao xem tat ca phan hoi
                view_replies_buttons = page.locator(CSS_SELECTOR['class_view_replies_div'])
                button_count = view_replies_buttons.count()
                print(f'rep:{button_count}')

                if button_count == 0:
                    break

                button = view_replies_buttons.nth(0)
                button.scroll_into_view_if_needed()
                button.click(force=True)
                delay(page)

            px = uniform(3000, 4000)
            page.mouse.wheel(0, px)
            delay(page)

            old_height = new_height
            new_height = post_body.bounding_box()['height']

        delay(page)
        page.wait_for_load_state(state='load')

        soup = BeautifulSoup(page.content(), 'lxml')

        body = soup.select(CSS_SELECTOR['class_post_body_to_soup_div'])
        browser.close()
        print('Done!')

        return body[0].prettify()

def extract_comment_with_emoji(comment_div):
    comment_text = ""
    for element in comment_div.children:
        if element.name == "span" and element.find('img'):
            emoji = element.find('img').get('alt')
            comment_text += emoji
        elif isinstance(element, str):
            comment_text += element.strip()

    return comment_text.strip()

def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    post = {
        'content': '',
        'label': None
    }

    cmt_section = soup.select('.x169t7cy.x19f6ikt')
    post['comments'] = []

    for k in range(len(cmt_section)):
        cmt_hier = cmt_section[k].select(':scope > div')
        par_cmt = cmt_hier[0].select('.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs > div')
        if len(par_cmt) == 0:
            continue
        else:
            par_cmt = par_cmt[0]
        content = extract_comment_with_emoji(par_cmt)

        post['comments'].append({
            'content': content,
            'label': None,
            'comments': []
        })

        if len(cmt_hier[1]) > 1:
            child_section = cmt_hier[1].select(':scope > div')
            for i in range(len(child_section) - 1):
                is_delete = False

                child = child_section[i].select(':scope > div > div')
                child_cmt = child[0].select('.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs > div')
                if len(child_cmt) == 0:
                    child_cmt = child[1].select('.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs > div')[0]
                    is_delete = True
                else:
                    child_cmt = child_cmt[0]
                content = extract_comment_with_emoji(child_cmt)

                post['comments'][-1]['comments'].append({
                    'content': content,
                    'label': None,
                    'comments': []
                })

                if len(child[1]) > 1 and not is_delete:
                    sub_child_section = child[1].select(':scope > div')

                    for j in range(len(sub_child_section) - 1):
                        sub_child_cmt = sub_child_section[j].select('.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs > div')[0]
                        content = extract_comment_with_emoji(sub_child_cmt)

                        post['comments'][-1]['comments'][i]['comments'].append({
                            'content': content,
                            'label': None
                        })

    return post

def flatten_comments(comments):
    def process_level(comments):
        flattened = []
        for comment in comments:
            if comment['content'] is None or comment['content'] == "":
                if 'comments' in comment and comment['comments']:
                    sub_flattened = process_level(comment['comments'])
                    flattened.extend(sub_flattened)
            else:
                if 'comments' in comment and comment['comments']:
                    comment['comments'] = process_level(comment['comments'])
                flattened.append(comment)
        return flattened

    return process_level(comments)

def count_comment(post):
    if 'comments' in post and post['comments']:
        current_count = len(post['comments'])
        for cmt in post['comments']:
            current_count += count_comment(cmt)
        return current_count
    else:
        return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('username', type=str, help='Username')
    parser.add_argument('password', type=str, help='Password')
    parser.add_argument('post_url', type=str, help='Post url')
    parser.add_argument('is_headless', type=bool, nargs='?', default=False ,help='Post url')

    arg = parser.parse_args()

    username = arg.username # huytin0392460501
    password = arg.password # chuong.05
    post_url = arg.post_url
    is_headless = arg.is_headless

    body = get_html(username, password, post_url, is_headless)
    post = get_data(body)
    print(count_comment(post))

    post['comments'] = flatten_comments(post['comments'])
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(post)

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
