from config import get_output_directory
from files import read_post_files, clear_dir
from generator import generate_pages


def generate_blog():
    # read/parse post files
    posts = read_post_files('source')
    posts.sort(key=lambda x: x.date, reverse=True)

    output_directory = get_output_directory()

    # should probably clear the dir first
    clear_dir(output_directory)

    # generate post pages
    generate_pages(posts, output_directory)


generate_blog()
