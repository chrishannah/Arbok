import yaml

from link import Link

# read config file
config_file = open('source/blog.yaml').read()
config = yaml.safe_load(config_file)


def get_site_title() -> str:
    return config['site']['title']


def get_posts_per_page() -> int:
    return config['site']['posts_per_page']


def get_source_directory() -> str:
    return 'source'


def get_output_directory() -> str:
    return config['output_directory']


def get_image_directory() -> str:
    return get_source_directory() + '/' + config['image_directory']


def get_background_colour() -> str:
    return config['style']['background-colour']


def get_text_colour() -> str:
    return config['style']['text-colour']


def get_secondary_text_colour() -> str:
    return config['style']['secondary-text-colour']


def get_link_colour() -> str:
    return config['style']['link-colour']


def get_links() -> list[Link]:
    links = []
    for link_item in config['links']:
        link = Link(link_item['label'], link_item['url'])
        links.append(link)
    return links
