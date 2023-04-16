from constants import SITE_TITLE
from post import Post
from utils import split


def generate_pages(posts: list[Post], destination_dir: str):
    # indexes
    index_pages = generate_post_index_pages(posts)
    for index_page in index_pages:
        index_page_content = index_pages[index_page]
        write_file(destination_dir, index_page, index_page_content)
    # archive
    archive_page = generate_post_archive(posts)
    write_file(destination_dir, 'archive', archive_page)
    # individual post pages
    for post in posts:
        post_page = generate_post_page(post)
        write_file(destination_dir, post.filename, post_page)


def generate_post_page(post: Post) -> str:
    post_page_content = generate_post_page_content(post)
    generated_page = generate_default_page(post_page_content)
    return generated_page


def generate_post_page_content(post: Post) -> str:
    post_template = open('templates/post.html').read() \
        .replace('__POST__TITLE__', post.title) \
        .replace('__POST_URL__', '' + post.filename + ".html") \
        .replace('__POST_DATE__', post.date.strftime('%-d/%m/%Y')) \
        .replace('__CONTENT__', post.html)
    return post_template


def generate_post_archive(posts: list[Post]) -> str:
    content = ""
    for post in posts:
        content += generate_post_archive_item(post)
    archive_template = open('templates/archive.html').read() \
        .replace('__CONTENT__', content)
    generated_page = generate_default_page(archive_template)
    return generated_page


def generate_post_index_pages(posts: list[Post]):
    post_index_pages = {}
    posts_per_page = 10
    chunked_posts = list(split(posts, posts_per_page))
    for page, posts_chunk in enumerate(chunked_posts):
        previous = get_page_filename(get_previous_page(page))
        next = get_page_filename(get_next_page(page, len(chunked_posts)))
        index_page_content = generate_post_index_page(posts_chunk, previous, next)
        filename = get_page_filename(page)
        post_index_pages[filename] = index_page_content
    return post_index_pages


def get_previous_page(page: int) -> int:
    if page > 0:
        return page - 1
    else:
        return -1


def get_next_page(page: int, total_pages: int) -> int:
    if page == total_pages - 1:
        return -1
    else:
        return page + 1


def get_page_filename(page: int) -> str:
    filename = ''
    if page == 0:
        return 'index'
    elif page > 0:
        filename = 'page' + str(page)
    return filename


def generate_post_index_page(posts: list[Post], previous: str, next: str) -> str:
    content = ""
    for post in posts:
        content += generate_post_page_content(post)
    paged_page = generate_paged_page(content, previous, next)
    generated_page = generate_default_page(paged_page)
    return generated_page


def generate_post_archive_item(post: Post) -> str:
    archive_item_template = open('templates/archive-post.html').read() \
        .replace('__POST_TITLE__', post.title) \
        .replace('__POST_URL__', '' + post.filename + ".html") \
        .replace('__POST_DATE__', post.date.strftime('%d/%m/%Y'))
    return archive_item_template


def generate_default_page(content: str) -> str:
    style_content = open('templates/style.css').read()
    default_template = open('templates/default.html').read() \
        .replace('__SITE_TITLE__', SITE_TITLE) \
        .replace('__CONTENT__', content) \
        .replace('__STYLE__', style_content)
    return default_template


def generate_paged_page(content: str, previous: str, next: str) -> str:
    paged_link_template = open('templates/paged-link.html').read()
    paged_content = ''
    if len(previous) > 0:
        paged_content += paged_link_template \
            .replace('__URL__', previous + ".html") \
            .replace('__TEXT__', 'Newer')
    if len(next) > 0:
        paged_content += paged_link_template \
            .replace('__URL__', next + ".html") \
            .replace('__TEXT__', 'Older')
    paged_template = open('templates/paged.html').read() \
        .replace('__CONTENT__', content) \
        .replace('__PAGINATION__', paged_content)
    return paged_template


def write_file(destination_dir, filename, content):
    out_filename = destination_dir + '/' + filename + '.html'
    output_file = open(out_filename, 'w')
    output_file.write(content)
    output_file.close()
