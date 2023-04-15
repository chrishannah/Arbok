from html5print import HTMLBeautifier

from constants import SITE_TITLE
from xml.dom import minidom
from post import Post


def generate_pages(posts: list[Post], destination_dir: str):
    # archive
    archive_page = generate_post_archive(posts)
    write_file(destination_dir, 'archive', archive_page)
    # individual post pages
    for post in posts:
        post_page = generate_post_page(post)
        write_file(destination_dir, post.filename, post_page)


def generate_post_page(post: Post) -> str:
    post_template = open('templates/post.html').read() \
        .replace('__POST__TITLE__', post.title) \
        .replace('__POST_URL__', '' + post.filename + ".html") \
        .replace('__POST_DATE__', post.date.strftime('%-d/%m/%Y')) \
        .replace('__CONTENT__', post.html)
    generated_page = generate_default_page(post_template)
    return generated_page


def generate_post_archive(posts: list[Post]) -> str:
    content = ""
    for post in posts:
        content += generate_post_archive_item(post)
    archive_template = open('templates/archive.html').read() \
        .replace('__CONTENT__', content)
    generated_page = generate_default_page(archive_template)
    # html = HTMLBeautifier.beautify(generated_page, 4)
    return generated_page


def generate_post_archive_item(post: Post) -> str:
    archive_item_template = open('templates/archive-post.html').read() \
        .replace('__POST_TITLE__', post.title) \
        .replace('__POST_URL__', '' + post.filename + ".html") \
        .replace('__POST_DATE__', post.date.strftime('%d/%m/%Y'))
    return archive_item_template


def generate_default_page(content: str) -> str:
    default_template = open('templates/default.html').read() \
        .replace('__SITE_TITLE__', SITE_TITLE) \
        .replace('__CONTENT__', content)
    return default_template


def write_file(destination_dir, filename, content):
    out_filename = destination_dir + '/' + filename + '.html'
    output_file = open(out_filename, 'w')
    output_file.write(content)
    output_file.close()
