import os
import re
from glob import glob
import stat
from ..module import Module
from os import path, listdir, walk
from ..utils.loading import Loading
from gitools.utils.utilities import Utilities
from core.pack_db.pack_reader import getPackDB
from core.commit.commit_reader import readCommit
from core.commit.commit_writer import writeCommit
from core.index_db.index_reader import getIndexDB
from core.pack_db.pack_writer import updateObject, writePack


class UpdateMessageModule(Module):
    def process(self):
        Module.checkBackup()
        Module.runGC()
        self.selectCommit()

        if not self.commit_message:
            old_message = next(
                (commit for commit in self.commits if commit[0] == self.commit_hash),
                None,
            )
            self.commit_message = Module.input(
                "# Enter New Commit Message" if old_message is None else old_message[5]
            ).replace("# Enter New Commit Message", "")

        Utilities.clearConsole()
        loading = Loading("Please wait")
        try:
            git_dir = path.join(Utilities.cwd, ".git")
            pack_dir = path.join(git_dir, "objects", "pack")
            idx_name = next(filter(lambda f: f.endswith(".idx"), listdir(pack_dir)))
            pack_name = next(filter(lambda f: f.endswith(".pack"), listdir(pack_dir)))
            idx_path = path.join(pack_dir, idx_name)
            pack_path = path.join(pack_dir, pack_name)

            index_db = getIndexDB(idx_path, pack_path)
            pack_db = getPackDB(pack_path, index_db)

            object = pack_db.objects[self.commit_hash]
            commit = readCommit(object.data)
            commit.message = self.commit_message.encode()

            new_hashes = updateObject(
                pack_db,
                pack_db.objects[self.commit_hash],
                object.data,
                writeCommit(commit),
            )

            writePack(pack_dir, pack_db)

            refs = [
                y
                for f in ["packed-refs", "ORIG_HEAD", "FETCH_HEAD", "HEAD"]
                for x in walk(git_dir)
                for y in glob(path.join(x[0], f))
            ] + [y for x in walk(path.join(git_dir, 'refs')) for y in glob(path.join(x[0], "*"))]

            refs = list(filter(lambda f: path.isfile(f), refs))

            os.chmod(idx_path, stat.S_IWRITE)
            os.chmod(pack_path, stat.S_IWRITE)
            os.remove(idx_path)
            os.remove(pack_path)
            
            for ref in refs:
                with open(ref, 'rb+') as f:
                    content = f.read().decode()
                    if not any(filter(lambda h: h[0] in content, new_hashes)):
                        continue
                    for new_hash in new_hashes:
                        if not new_hash[0] in content:
                            continue
                        content = re.sub(new_hash[0], new_hash[1], content)
                    f.seek(0)
                    f.write(content.encode())
                    f.truncate()

            loading.stop()
            Utilities.clearConsole()

            print("Commit Message Changed Successfully")
        except Exception as err:
            print("Commit Message Change Failed, Error:\r\n" + err)

    @staticmethod
    def getFlag():
        return "um"

    @staticmethod
    def getName():
        return "Update Message"

    @staticmethod
    def getDescription():
        return "Update commit message"

    def isVisible(self):
        return True
