from selectors import CSS_SELECTOR
from bs4 import BeautifulSoup

def get_post_content(html):
    pass

def get_content_in_cmt(div_cmt):
    span_content_cmt = div_cmt.select_one(CSS_SELECTOR['class_span_content_cmt'])
    if span_content_cmt:
        # thêm icon vào nội dung
        for img_tag in span_content_cmt.find_all('img'):
            alt_text = img_tag.get('alt', '')  # icon nằm trong alt
            img_tag.replace_with(alt_text)

        # loại bỏ tag tên
        for a_tag in span_content_cmt.find_all('a'):
            a_tag.decompose()

        return span_content_cmt.text.strip()
    else:
        return ''

def get_comment(html):
    soup = BeautifulSoup(html, 'lxml')

    div_cmt = soup.select(CSS_SELECTOR['class_div_cmt'])

    # ghi teen bieens vo doc dum cai nho met qua ni !!!!!!!!!!!!!!!!!!!!!!!!!
    for i, div_cmt in enumerate(div_cmt):
        div_cmt_lv = list(div_cmt) # chuyển các con trong div_cmt thành 1 list
        print(f'cmt: {i + 1}')

        # cmt lv1
        div_cmt_lv1 = div_cmt_lv[0] # lấy div chứa cmt lv_1, xem doc phần 6
        content = get_content_in_cmt(div_cmt_lv1)
        print(f'\t {content}')

        # cmt lv2 & lv3
        div_cmt_lv_2_and_3 = list(div_cmt_lv[1]) # lấy div chứa cmt lv2 và lv3, xem doc phần 8
        for j, div_2_3 in enumerate(div_cmt_lv_2_and_3):
            # div_2_3 cuối là ô cmt
            if j == len(div_cmt_lv_2_and_3) - 1:
                break

            wrapper_2_3 = list(div_2_3.select_one(':scope > div')) # 1 lopws wrapper nho viet doc

            # cmt lv_2
            div_cmt_lv2 = wrapper_2_3[0] # doc
            content = get_content_in_cmt(div_cmt_lv2)
            print('\t'*2, content)






