from config import get_site_title, get_posts_per_page, get_secondary_text_colour, get_background_colour, \
    get_text_colour, get_link_colour, get_footer_links, get_header_links
from date import format_datetime
from files import write_file, get_page_url
from post import Post
from utils import split


def generate_pages(posts: list[Post], destination_dir: str):
    # indexes
    index_pages = generate_post_index_pages(posts)
    for index_page in index_pages:
        index_page_content = index_pages[index_page]
        write_file(destination_dir, index_page, index_page_content)
    # tag indexes
    tag_pages = generate_tag_archive_pages(posts)
    for tag_page in tag_pages:
        tag_page_content = tag_pages[tag_page]
        write_file(destination_dir + '/tags', tag_page, tag_page_content)
    # archive
    archive_page = generate_post_archive(posts)
    write_file(destination_dir, 'archive', archive_page)
    # individual post pages
    for post in posts:
        post_page = generate_post_page(post)
        write_file(destination_dir, post.filename, post_page)


def generate_tag_archive_pages(posts: [Post]):
    tag_archive_pages = {}
    tags = []
    for post in posts:
        tags.extend(post.tags)
    tags = list(set(tags))

    for tag in tags:
        filtered_posts = list(filter(lambda p: tag in p.tags, posts))
        tag_archive_page = generate_post_archive(filtered_posts, 'Tag: ' + tag)
        tag_archive_pages[tag.lower()] = tag_archive_page
    return tag_archive_pages


def generate_post_page(post: Post) -> str:
    post_page_content = generate_post_page_content(post, True)
    generated_page = generate_default_page(post_page_content)
    return generated_page


def generate_post_page_content(post: Post, include_tags: bool) -> str:
    tags_content = ''
    if include_tags and len(post.tags) > 0:
        content = ''
        link_template = open('templates/link.html').read()
        for index, tag in enumerate(post.tags):
            content += link_template \
                .replace('__URL__', get_page_url(tag, 'tag')) \
                .replace('__LABEL__', tag)
            if index < len(post.tags) - 1:
                content += ' '
        tags_content = open('templates/tags.html').read() \
            .replace('__CONTENT__', content)

    post_template = open('templates/post.html').read() \
        .replace('__POST__TITLE__', post.title) \
        .replace('__POST_URL__', '' + get_page_url(post.filename, 'post')) \
        .replace('__POST_DATE__', format_datetime(post.date)) \
        .replace('__CONTENT__', post.html) \
        .replace('__FOOTER_CONTENT__', tags_content)
    return post_template


def generate_post_archive(posts: list[Post], title='Archive') -> str:
    content = ""
    for post in posts:
        content += generate_post_archive_item(post)
    archive_template = open('templates/archive.html').read() \
        .replace('__CONTENT__', content) \
        .replace('__TITLE__', title)
    generated_page = generate_default_page(archive_template)
    return generated_page


def generate_post_index_pages(posts: list[Post]):
    post_index_pages = {}
    posts_per_page = get_posts_per_page()
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
        filename = 'page/' + str(page)
    return filename


def generate_post_index_page(posts: list[Post], previous: str, next: str) -> str:
    content = ""
    for post in posts:
        content += generate_post_page_content(post, False)
    paged_page = generate_paged_page(content, previous, next)
    generated_page = generate_default_page(paged_page)
    return generated_page


def generate_post_archive_item(post: Post) -> str:
    archive_item_template = open('templates/archive-post.html').read() \
        .replace('__POST_TITLE__', post.title) \
        .replace('__POST_URL__', '' + get_page_url(post.filename, 'post')) \
        .replace('__POST_DATE__', format_datetime(post.date))
    return archive_item_template


def generate_default_page(content: str) -> str:
    style_content = get_style_content()
    footer_content = get_footer_content()
    header_navigation_content = get_header_navigation_content()
    default_template = open('templates/default.html').read() \
        .replace('__SITE_TITLE__', get_site_title()) \
        .replace('__CONTENT__', content) \
        .replace('__STYLE__', style_content) \
        .replace('__FOOTER_CONTENT__', footer_content) \
        .replace('__HEADER_CONTENT__', header_navigation_content)
    return default_template


def generate_paged_page(content: str, previous: str, next: str) -> str:
    paged_link_template = open('templates/paged-link.html').read()
    previous_content = ''
    next_content = ''
    if len(previous) > 0:
        previous_content += paged_link_template \
            .replace('__URL__', get_page_url(previous, 'index')) \
            .replace('__TEXT__', '← Newer')
    if len(next) > 0:
        next_content += paged_link_template \
            .replace('__URL__', get_page_url(next, 'index')) \
            .replace('__TEXT__', 'Older →')
    links = []
    if previous_content != '':
        links.append(previous_content)
    if next_content != '':
        links.append(next_content)
    paged_content = ' '.join(links)
    paged_template = open('templates/paged.html').read() \
        .replace('__CONTENT__', content) \
        .replace('__PAGINATION__', paged_content)
    return paged_template


def get_style_content() -> str:
    style_content = open('templates/style.css').read() \
        .replace('__BACKGROUND_COLOUR__', get_background_colour()) \
        .replace('__TEXT_COLOUR__', get_text_colour()) \
        .replace('__SECONDARY_TEXT_COLOUR__', get_secondary_text_colour()) \
        .replace('__LINK_COLOUR__', get_link_colour())
    return style_content


def get_footer_content() -> str:
    links = get_footer_links()
    return generate_navigation_content(links)


def get_header_navigation_content() -> str:
    links = get_header_links()
    return generate_navigation_content(links)


def generate_navigation_content(links):
    link_template = open('templates/link.html').read()
    link_content = ''
    for index, link in enumerate(links):
        link_content += link_template \
            .replace('__URL__', link.url) \
            .replace('__LABEL__', link.label)
        if index < len(links) - 1:
            link_content += ' ∣ '
    nav_content = open('templates/nav.html').read() \
        .replace('__CONTENT__', link_content)
    return nav_content
