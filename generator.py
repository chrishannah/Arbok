from html5print import HTMLBeautifier

from constants import SITE_TITLE
from post import Post


def generate_pages(posts: list[Post], destination_dir: str):
    for post in posts:
        post_page = generate_post_page(post)
        out_filename = destination_dir + '/' + post.filename + '.html'
        output_file = open(out_filename, 'w')
        output_file.write(post_page)
        output_file.close()


def generate_post_page(post: Post) -> str:
    post_template = open('templates/post.html').read() \
        .replace('__POST__TITLE__', post.title) \
        .replace('__POST_DATE__', post.date.strftime('%-d/%m/%Y')) \
        .replace('__CONTENT__', post.html)
    generated_page = generate_default_page(post_template)
    html = HTMLBeautifier.beautify(generated_page, 4)
    return html


def generate_default_page(content: str) -> str:
    default_template = open('templates/default.html').read() \
        .replace('__SITE_TITLE__', SITE_TITLE) \
        .replace('__CONTENT__', content)
    return default_template
