import zlib
from hashlib import sha1
from research.object import Object
from os import path, remove, makedirs
from gitools.utils.utilities import Utilities


class ObjectWriter:
    @staticmethod
    def update(hash: str, object: Object):
        tree = b"".join(map(lambda x: b"tree %s\n" % x, object.trees)).strip()
        parent = b"".join(map(lambda x: b"parent %s\n" % x, object.parents)).strip()
        author = b"author %s <%s> %d %s" % (
            object.author_name,
            object.author_email,
            int(object.author_date.timestamp()),
            object.author_date.strftime("%z").encode(),
        )
        committer = b"committer %s <%s> %d %s" % (
            object.committer_name,
            object.committer_email,
            int(object.committer_date.timestamp()),
            object.committer_date.strftime("%z").encode(),
        )
        object_content = b"commit %d\x00%s\n%s\n%s\n%s\n\n%s\n" % (
            object.commit_index,
            tree,
            parent,
            author,
            committer,
            object.message,
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
