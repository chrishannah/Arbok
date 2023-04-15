from files import read_post_files, clear_dir
from generator import generate_pages


def generate_blog():
    # read/parse post files
    posts = read_post_files('source')
    posts.sort(key=lambda x: x.date, reverse=True)

    # should probably clear the dir first
    clear_dir('blog')

    # generate post pages
    generate_pages(posts, 'blog')


generate_blog()
