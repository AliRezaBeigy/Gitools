import re
from core.commit.commit import Commit
from datetime import datetime, timedelta, timezone


def readCommit(data: bytes):
    tree = re.findall(
        b"tree\s*([a-z0-9]*)\n",
        data
    )

    if len(tree):
        tree = tree[0]
    else:
        raise Exception("Tree not found")

    committer = re.findall(
        b"committer\s*([^<]*)\s<(.*)>\s(\d+)\s((\+|\-)\d{4})",
        data
    )

    if len(committer):
        committer = committer[0]
    else:
        raise Exception("Committer not found")

    author = re.findall(
        b"author\s*([^<]*)\s<(.*)>\s(\d+)\s((\+|\-)\d{4})",
        data
    )
    
    if len(author):
        author = author[0]
    else:
        raise Exception("Author not found")

    gpgsig = re.findall(
        b"gpgsig\s*(-----BEGIN(.*)-----END(.*)-----)",
        data,
        flags=re.DOTALL
    )
    
    gpgsig = gpgsig[0][0] if len(gpgsig) else None

    message = re.findall(
        b"\n\n\s*(.*)\n$",
        data,
        flags=re.DOTALL,
    )

    parents = re.findall(
        b"parent\s*([a-z0-9]*)\n",
        data
    )

    return Commit(
        tree=tree,
        gpgsig=gpgsig,
        parents=parents,
        message=message,
        author_name=author[0],
        author_email=author[1],
        committer_name=committer[0],
        committer_email=committer[1],
        author_date=datetime.fromtimestamp(
            float(author[2]),
            tz=timezone(
                timedelta(
                    seconds=(
                        int(author[3][:3]) * 3600 + int(author[3][3:]) * 60
                    )
                )
            ),
        ),
        committer_date=datetime.fromtimestamp(
            float(committer[2]),
            tz=timezone(
                timedelta(
                    seconds=(
                        int(committer[3][:3]) * 3600 + int(committer[3][3:]) * 60
                    )
                )
            ),
        ),
    )
