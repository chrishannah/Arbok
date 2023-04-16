from datetime import datetime


class Post:
    def __init__(self, title: str, html: str, tags: list[str], filename: str, date: datetime):
        self.title = title
        self.html = html
        self.tags = tags
        self.filename = filename
        self.date = date
