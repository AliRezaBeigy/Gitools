from datetime import datetime


class Commit:
    tree: str
    message: str
    author_name: str
    author_email: str
    parents: list[str]
    committer_name: str
    committer_email: str
    author_date: datetime
    committer_date: datetime

    def __init__(
        self,
        tree: str,
        message: str,
        author_name: str,
        author_email: str,
        parents: list[str],
        committer_name: str,
        committer_email: str,
        author_date: datetime,
        committer_date: datetime,
    ):
        self.tree = tree
        self.parents = parents
        self.message = message.strip()
        self.author_name = author_name
        self.author_date = author_date
        self.author_email = author_email
        self.committer_name = committer_name
        self.committer_date = committer_date
        self.committer_email = committer_email