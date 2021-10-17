import zlib
from hashlib import sha1
from os import path, remove, makedirs
from core.commit.commit import Commit
from gitools.utils.utilities import Utilities


class CommitWriter:
    @staticmethod
    def update(hash: str, commit: Commit):
        tree = b"".join(map(lambda x: b"tree %s\n" % x, commit.trees)).strip()
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
        object_content = b"commit %d\x00%s\n%s\n%s\n%s\n\n%s\n" % (
            commit.commit_index,
            tree,
            parent,
            author,
            committer,
            commit.message,
        )

        object_name = sha1(object_content).hexdigest()
        data = zlib.compress(object_content)

        if not path.exists(
            path.join(
                Utilities.cwd,
                ".git",
                "objects",
                object_name[:2],
            )
        ):
            makedirs(
                path.join(
                    Utilities.cwd,
                    ".git",
                    "objects",
                    object_name[:2],
                )
            )

        with open(
            path.join(
                Utilities.cwd,
                ".git",
                "objects",
                object_name[:2],
                object_name[2:],
            ),
            "wb",
        ) as object_file:
            object_file.write(data)

        # ObjectWriter.replace(hash, object_name)

    @staticmethod
    def replace(src_hash: str, des_hash: str):
        remove(
            path.join(
                Utilities.cwd,
                ".git",
                "objects",
                hash[:2],
                hash[2:],
            )
        )
