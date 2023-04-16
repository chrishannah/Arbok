import os
import shutil
from os import listdir

import frontmatter
import markdown

from config import get_output_directory, get_image_directory, get_site_url
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
            tags = []
            if fm_post.get('tags') is not None:
                tags = str(fm_post.get('tags')).split(' ')

            date = fm_post.get('date')
            html = markdown.markdown(fm_post.content)

            post = Post(title, html, tags, output_name, date)
            posts.append(post)
    return posts


def clear_dir(directory: str):
    for filename in listdir(directory):
        full_path = directory + '/' + filename
        if os.path.isfile(full_path):
            os.remove(full_path)
        elif os.path.isdir(full_path):
            shutil.rmtree(full_path)


def copy_directory(source: str, destination: str):
    shutil.copytree(source, destination, dirs_exist_ok=True)


def set_up_output_directory():
    create_empty_dir(get_output_directory())
    create_empty_dir(get_image_directory())
    create_empty_dir(get_output_directory() + '/tags')
    create_empty_dir(get_output_directory() + '/page')


def create_empty_dir(directory: str):
    if not os.path.exists(directory):
        os.mkdir(directory)


def write_file(destination_dir, filename, content):
    out_filename = destination_dir + '/' + filename + '.html'
    output_file = open(out_filename, 'w')
    output_file.write(content)
    output_file.close()


def get_page_url(filename: str, type: str) -> str:
    if type == 'post':
        return get_site_url() + filename + '.html'
    elif type == 'index':
        return get_site_url() + filename + '.html'
    elif type == 'tag':
        return get_site_url() + 'tags/' + filename.lower() + '.html'
