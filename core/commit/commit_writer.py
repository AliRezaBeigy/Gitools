from core.commit.commit import Commit


@staticmethod
def writeCommit(commit: Commit):
    tree = b"tree %s" % commit.tree
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

    data = tree + b'\n'

    if len(commit.parents):
        parent = b"".join(map(lambda x: b"parent %s\n" % x, commit.parents)).strip()
        data += parent + b'\n'

    data += author + b'\n'
    data += committer + b'\n'

    if commit.gpgsig is not None:
        gpgsig = b'gpgsig ' + commit.gpgsig
        data += gpgsig + b'\n'
        
    data += b'\n\n' + commit.message + b'\n'

    return data
