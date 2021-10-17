import re
import zlib
from os import path
from core.commit.commit import Commit
from gitools.utils.utilities import Utilities
from datetime import datetime, timedelta, timezone


class CommitReader:
    @staticmethod
    def commit(hash: str):
        with open(
            path.join(
                Utilities.cwd,
                ".git",
                "objects",
                hash[:2],
                hash[2:],
            ),
            "rb",
        ) as object_file:
            object = object_file.read()
            data = zlib.decompress(object)

            commit_index = re.findall(b"commit (\d+)", data)[0]
            content = re.findall(
                b"author\s*([^<]*)\s<(.*)>\s(\d+)\s((\+|\-)\d{4})\ncommitter\s*([^<]*)\s<(.*)>\s(\d+)\s((\+|\-)\d{4})\n\n\s*(.*)",
                data,
                flags=re.DOTALL,
            )[0]
            parents = re.findall(
                b"parent\s*([a-z0-9]*)\n",
                data,
            )
            trees = re.findall(
                b"tree\s*([a-z0-9]*)\n",
                data,
            )

            return Commit(
                trees=trees,
                parents=parents,
                message=content[10],
                author_name=content[0],
                author_email=content[1],
                committer_name=content[5],
                committer_email=content[6],
                commit_index=int(commit_index),
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
