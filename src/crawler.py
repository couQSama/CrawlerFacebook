from selectors import CSS_SELECTOR
from random import uniform
from utils import delay

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

