from selectors import CSS_SELECTOR
from random import uniform
from ultis import delay

def click_all_view_reply_buttons(page):
    while True:
        view_reply_buttons = page.locator(CSS_SELECTOR['class_view_reply_button'])
        button_count = view_reply_buttons.count()
        if button_count == 0:
            break
        view_reply_buttons.nth(0).click()
        delay(page)

def click_all_view_more_buttons(page):
    while True:
        view_more_buttons = page.get_by_role('button', name='Xem thêm')
        button_count = view_more_buttons.count()
        if button_count == 0:
            break
        view_more_buttons.nth(0).click(force=True)
        delay(page)

def scroll_to_load_comments(page):
    # Di chuột vào giữa để cuộn
    viewport_width = 1280
    viewport_height = 800
    center_x = viewport_width // 2
    center_y = viewport_height // 2
    page.mouse.move(center_x, center_y)

    body_post = page.locator(CSS_SELECTOR['class_body_post'])
    old_height, new_height = 0, body_post.bounding_box()['height']
    while old_height != new_height:
        # Nhấn các nút xem phản hồi hiện có
        click_all_view_reply_buttons(page)
        # Nhấn các nút xem thêm có
        click_all_view_more_buttons(page)

        # Cuộn xuống
        px_to_scroll = uniform(2000, 3000)
        page.mouse.wheel(0, px_to_scroll)
        old_height = new_height
        new_height = body_post.bounding_box()['height']
        delay(page)

    return body_post

def get_post_html(page, post_url):
    page.goto(post_url, timeout=120000, wait_until='domcontentloaded')
    delay(page)

    # Thao tác xổ tất cả bình luận
    most_popular_button = page.locator(CSS_SELECTOR['class_most_popular'])
    most_popular_button.scroll_into_view_if_needed()
    most_popular_button.click()
    delay(page)
    page.locator(CSS_SELECTOR['class_most_popular_menu']).nth(2).click()
    delay(page)

    post_full_content = scroll_to_load_comments(page)

    return post_full_content.inner_html()

#     while old_height != new_height:
#         while True:
#             while True:
#                 view_more_buttons = page.get_by_role('button', name='Xem thêm')
#                 button_count = view_more_buttons.count()
#                 print(f'more:{button_count}')
#                 if button_count == 0:
#                     break
#
#                 button = view_more_buttons.nth(0)
#                 button.click(force=True)
#                 delay(page)
#             # Click vao xem tat ca phan hoi
#             view_replies_buttons = page.locator(CSS_SELECTOR['class_view_replies_div'])
#             button_count = view_replies_buttons.count()
#             print(f'rep:{button_count}')
#
#             if button_count == 0:
#                 break
#
#             button = view_replies_buttons.nth(0)
#             button.scroll_into_view_if_needed()
#             button.click(force=True)
#             delay(page)
#
#         px = uniform(3000, 4000)
#         page.mouse.wheel(0, px)
#         delay(page)
#
#         old_height = new_height
#         new_height = post_body.bounding_box()['height']
#
#     delay(page)
#     page.wait_for_load_state(state='load')
#
#     soup = BeautifulSoup(page.content(), 'lxml')
#
#     body = soup.select(CSS_SELECTOR['class_post_body_to_soup_div'])
#     browser.close()
#     print('Done!')
#
#     return body[0].prettify()
#
# def extract_comment_with_emoji(comment_div):
#     comment_text = ""
#     for element in comment_div.children:
#         if element.name == "span" and element.find('img'):
#             emoji = element.find('img').get('alt')
#             comment_text += emoji
#         elif isinstance(element, str):
#             comment_text += element.strip()
#
#     return comment_text.strip()
#
# def get_data(html):
#     soup = BeautifulSoup(html, 'lxml')
#     post = {
#         'content': '',
#         'label': None
#     }
#
#     cmt_section = soup.select('.x169t7cy.x19f6ikt')
#     post['comments'] = []
#
#     for k in range(len(cmt_section)):
#         cmt_hier = cmt_section[k].select(':scope > div')
#         par_cmt = cmt_hier[0].select('.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs > div')
#         if len(par_cmt) == 0:
#             continue
#         else:
#             par_cmt = par_cmt[0]
#         content = extract_comment_with_emoji(par_cmt)
#
#         post['comments'].append({
#             'content': content,
#             'label': None,
#             'comments': []
#         })
#
#         if len(cmt_hier[1]) > 1:
#             child_section = cmt_hier[1].select(':scope > div')
#             for i in range(len(child_section) - 1):
#                 is_delete = False
#
#                 child = child_section[i].select(':scope > div > div')
#                 child_cmt = child[0].select('.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs > div')
#                 if len(child_cmt) == 0:
#                     child_cmt = child[1].select('.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs > div')[0]
#                     is_delete = True
#                 else:
#                     child_cmt = child_cmt[0]
#                 content = extract_comment_with_emoji(child_cmt)
#
#                 post['comments'][-1]['comments'].append({
#                     'content': content,
#                     'label': None,
#                     'comments': []
#                 })
#
#                 if len(child[1]) > 1 and not is_delete:
#                     sub_child_section = child[1].select(':scope > div')
#
#                     for j in range(len(sub_child_section) - 1):
#                         sub_child_cmt = sub_child_section[j].select('.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs > div')[0]
#                         content = extract_comment_with_emoji(sub_child_cmt)
#
#                         post['comments'][-1]['comments'][i]['comments'].append({
#                             'content': content,
#                             'label': None
#                         })
#
#     return post
#
# def flatten_comments(comments):
#     def process_level(comments):
#         flattened = []
#         for comment in comments:
#             if comment['content'] is None or comment['content'] == "":
#                 if 'comments' in comment and comment['comments']:
#                     sub_flattened = process_level(comment['comments'])
#                     flattened.extend(sub_flattened)
#             else:
#                 if 'comments' in comment and comment['comments']:
#                     comment['comments'] = process_level(comment['comments'])
#                 flattened.append(comment)
#         return flattened
#
#     return process_level(comments)
#
# def count_comment(post):
#     if 'comments' in post and post['comments']:
#         current_count = len(post['comments'])
#         for cmt in post['comments']:
#             current_count += count_comment(cmt)
#         return current_count
#     else:
#         return 0
#
