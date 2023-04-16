from config import get_output_directory, get_image_directory, get_source_directory
from files import read_post_files, clear_dir, copy_directory, set_up_output_directory
from generator import generate_pages


def generate_blog():
    # read/parse post files
    posts = read_post_files(get_source_directory())
    posts.sort(key=lambda x: x.date, reverse=True)

    output_directory = get_output_directory()

    # setup output directory
    clear_dir(output_directory)
    set_up_output_directory()

    # generate post pages
    generate_pages(posts, output_directory)

    # move resource directories
    source_image_directory = get_image_directory()
    destination_image_directory = output_directory + '/images'
    copy_directory(source_image_directory, destination_image_directory)


generate_blog()
