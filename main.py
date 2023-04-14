import os
from os import listdir

import frontmatter
import markdown
from html5print import HTMLBeautifier

from post import Post

source_dir = 'source'
destination_dir = 'blog'
site_title = 'A Website'


def generate_blog():
    # read/parse post files
    posts = read_post_files(source_dir)
    posts.sort(key=lambda x: x.date, reverse=True)

    # should probably clear the dir first
    clear_dir(destination_dir)

    for post in posts:
        post_page = generate_post_page(post)
        out_filename = destination_dir + '/' + post.filename + '.html'
        output_file = open(out_filename, 'w')
        output_file.write(post_page)
        output_file.close()


def read_post_files(directory: str) -> list[Post]:
    posts = []
    filenames = listdir(directory)
    for filename in filenames:
        if filename.endswith('.md'):
            output_name = filename.removesuffix('.md')
            file = open(source_dir + '/' + filename).read()

            fm_post = frontmatter.loads(file)
            title = fm_post.get('title')
            tags = fm_post.get('tags')
            date = fm_post.get('date')
            html = markdown.markdown(fm_post.content)

            post = Post(title, html, tags, output_name, date)
            posts.append(post)
    return posts


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
        .replace('__SITE_TITLE__', site_title) \
        .replace('__CONTENT__', content)
    return default_template


def clear_dir(dir: str):
    for filename in listdir(dir):
        os.remove(dir + '/' + filename)


# lol
generate_blog()
