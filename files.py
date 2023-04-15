import os
from os import listdir

import frontmatter
import markdown

from post import Post


def read_post_files(directory: str) -> list[Post]:
    posts = []
    filenames = listdir(directory)
    for filename in filenames:
        if filename.endswith('.md'):
            output_name = filename.removesuffix('.md')
            file = open(directory + '/' + filename).read()

            fm_post = frontmatter.loads(file)
            title = fm_post.get('title')
            tags = fm_post.get('tags')
            date = fm_post.get('date')
            html = markdown.markdown(fm_post.content)

            post = Post(title, html, tags, output_name, date)
            posts.append(post)
    return posts


def clear_dir(directory: str):
    for filename in listdir(directory):
        os.remove(directory + '/' + filename)
