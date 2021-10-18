from core.commit.commit import Commit


@staticmethod
def writeCommit(commit: Commit):
    tree = b"tree %s" % commit.tree
    parent = b"".join(map(lambda x: b"parent %s\n" % x, commit.parents)).strip()
    author = b"author %s <%s> %d %s" % (
        commit.author_name,
        commit.author_email,
        int(commit.author_date.timestamp()),
        commit.author_date.strftime("%z").encode(),
    )
    committer = b"committer %s <%s> %d %s" % (
        commit.committer_name,
        commit.committer_email,
        int(commit.committer_date.timestamp()),
        commit.committer_date.strftime("%z").encode(),
    )
    return b"%s\n%s\n%s\n%s\n\n%s\n" % (tree,
        parent,
        author,
        committer,
        commit.message)
