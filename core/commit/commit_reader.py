import re
from core.commit.commit import Commit
from datetime import datetime, timedelta, timezone


def readCommit(data: bytes):
    content = re.findall(
        b"author\s*([^<]*)\s<(.*)>\s(\d+)\s((\+|\-)\d{4})\ncommitter\s*([^<]*)\s<(.*)>\s(\d+)\s((\+|\-)\d{4})\n\n\s*(.*)",
        data,
        flags=re.DOTALL,
    )[0]
    parents = re.findall(
        b"parent\s*([a-z0-9]*)\n",
        data,
    )
    tree = re.findall(
        b"tree\s*([a-z0-9]*)\n",
        data,
    )[0]

    return Commit(
        tree=tree,
        parents=parents,
        message=content[10],
        author_name=content[0],
        author_email=content[1],
        committer_name=content[5],
        committer_email=content[6],
        author_date=datetime.fromtimestamp(
            float(content[2]),
            tz=timezone(
                timedelta(
                    seconds=(
                        int(content[3][:3]) * 3600 + int(content[3][3:]) * 60
                    )
                )
            ),
        ),
        committer_date=datetime.fromtimestamp(
            float(content[7]),
            tz=timezone(
                timedelta(
                    seconds=(
                        int(content[8][:3]) * 3600 + int(content[8][3:]) * 60
                    )
                )
            ),
        ),
    )
