import yaml

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
