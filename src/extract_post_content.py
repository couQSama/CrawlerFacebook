from selectors import CSS_SELECTOR
from bs4 import BeautifulSoup

def create_cmt_dict(cmt_content):
    return {
        'cmt_content': cmt_content,
        'label': None,
        'comments': []
    }

def get_content_keep_space(span):
    div_sentences = span.select('div[dir="auto"][style="text-align: start;"]')
    content = ''

    if div_sentences:
        for div in div_sentences:
            content += (div.text + ' ')
    return content

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

        content = get_content_keep_space(span_content_cmt)

        return content
    else:
        return ''

def get_post_content(soup):
    span_content_post = soup.select_one(CSS_SELECTOR['class_span_content_post'])

    if span_content_post:
        # thêm icon vào nội dung
        for img_tag in span_content_post.find_all('img'):
            alt_text = img_tag.get('alt', '')  # icon nằm trong alt
            img_tag.replace_with(alt_text)

        # loại bỏ tag tên
        for a_tag in span_content_post.find_all('a'):
            a_tag.decompose()

        content = get_content_keep_space(span_content_post)

        return content

    else:
        return ''

def get_post_dict(html):
    soup = BeautifulSoup(html, 'lxml')

    post = {
        'post_url': '',
        'post_content': '',
        'label': None,
        'cmt_count': 0,
        'comments': []
    }

    # get content post
    content = get_post_content(soup)
    post['post_content'] = content

    # get comment
    # xem doc phần 6
    list_div_cmt = soup.select(CSS_SELECTOR['class_div_cmt'])
    for i, div_cmt in enumerate(list_div_cmt):
        list_div_cmt_lv = list(div_cmt) # tag trong div_cmt -> list: [div_cmt_lv1, div_cmt_lv2]

        # cmt lv1
        div_cmt_lv1 = list_div_cmt_lv[0]
        content = get_content_in_cmt(div_cmt_lv1)

        cmt_lv1_dict = create_cmt_dict(content)
        post['comments'].append(cmt_lv1_dict)
        post['cmt_count'] += 1

        # cmt lv2 & lv3
        div_contain_all_cmt_lv2_lv3 = list_div_cmt_lv[1]
        list_div_cmt_lv2_lv3 = list(div_contain_all_cmt_lv2_lv3)
        for j, div_cmt_lv2_lv3 in enumerate(list_div_cmt_lv2_lv3):
            # div cuối là ô cmt
            if j == len(list_div_cmt_lv2_lv3) - 1:
                break

            wrapper_lv = div_cmt_lv2_lv3.select_one(':scope > div')
            list_wrapper_lv2_lv3 = list(wrapper_lv)

            # cmt lv_2
            div_cmt_lv2 = list_wrapper_lv2_lv3[0]
            content = get_content_in_cmt(div_cmt_lv2)

            cmt_lv2_dict = create_cmt_dict(content)
            cmt_lv1_dict['comments'].append(cmt_lv2_dict)
            post['cmt_count'] += 1


            # cmt lv3
            div_contain_cmt_lv3 = list_wrapper_lv2_lv3[1]
            list_div_cmt_lv3 = list(div_contain_cmt_lv3)
            for k, div_cmt_lv3 in enumerate(list_div_cmt_lv3):
                # div cuối là ô cmt
                if k == len(list_div_cmt_lv3) - 1:
                    break

                content = get_content_in_cmt(div_cmt_lv3)

                cmt_lv3_dict = create_cmt_dict(content)
                cmt_lv2_dict['comments'].append(cmt_lv3_dict)
                post['cmt_count'] += 1

    return post