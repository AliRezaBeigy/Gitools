from os import path
from time import time
from core.pack_db.pack_reader import getPackDB
from core.commit.commit_reader import readCommit
from core.commit.commit_writer import writeCommit
from core.index_db.index_reader import getIndexDB
from core.pack_db.pack_writer import updateObject, writePack


def test_packdb():
    hash = "06aaeaae812acc57df5fc48c92b3528d9488dcf5"
    decompress_types = [1, 2, 3, 4, 5, 6, 7]

    idx_path = path.join("core", "samples", f"pack-{hash}.idx")
    pack_path = path.join("core", "samples", f"pack-{hash}.pack")

    t0 = time()

    index_db = getIndexDB(idx_path, pack_path)
    pack_db = getPackDB(pack_path, index_db, decompress_types)

    t1 = time()
    print("Read Time: " + str(t1 - t0))

    new_hashes = updateObject(
        pack_db,
        pack_db.objects["015da177f181d01b03501043fcb0082220ff8987"],
        b"linux",
        b"Heh Heh Heh Heh Heh",
    )

    print("Update Time: " + str(time() - t1))
    t1 = time()

    result_dir = path.dirname(pack_path)

    hash = writePack(result_dir, pack_db, decompress_types)

    print("Write Time: " + str(time() - t1))

    t1 = time()

    print("Total Time: " + str(t1 - t0))

    [print(h) for h in new_hashes]

def test_commit():
    sample_commit = b"tree 09640a9d1c9862ee780816f25c5d0cb1668392e5\nparent b4b9d21d3d5a544ed1c2c127b6f169af38d1209d\nauthor AliRezaBeigy <AliRezaBeigyKhu@gmail.com> 1612593585 +0330\ncommitter AliRezaBeigy <AliRezaBeigyKhu@gmail.com> 1612593585 +0330\n\nUpdate README\n"
    commit = readCommit(sample_commit)
    result = writeCommit(commit)
    assert result == sample_commit
    commit.tree = b"XXXXXa9d1c9862ee780816f25c5d0cb1668392e5"
    result = writeCommit(commit)
    assert result != sample_commit
    assert result == sample_commit.replace(b'09640a9d1c9862ee780816f25c5d0cb1668392e5', b'XXXXXa9d1c9862ee780816f25c5d0cb1668392e5')
