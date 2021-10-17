import shutil
from os import path
from time import time
from core.pack_db.pack_reader import getPackDB
from core.index_db.index_reader import getIndexDB
from core.pack_db.pack_writer import updateObject, writePack


def test():
    hash = "06aaeaae812acc57df5fc48c92b3528d9488dcf5"
    decompress_types = [1, 2, 3, 4, 5, 6, 7]

    idx_path = path.join("core", "samples", f"pack-{hash}.idx")
    pack_path = path.join("core", "samples", f"pack-{hash}.pack")

    t0 = time()

    index_db = getIndexDB(idx_path, pack_path)
    pack_db = getPackDB(pack_path, index_db, decompress_types)

    t1 = time()
    print("Read Time: " + str(t1 - t0))

    updateObject(
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

    result_index_db = path.join(result_dir, f"pack-{hash}.idx")
    result_pack_db = path.join(result_dir, f"pack-{hash}.pack")

    index_db = getIndexDB(result_index_db, result_pack_db)
    pack_db = getPackDB(result_pack_db, index_db, decompress_types)

    t1 = time()

    shutil.move(
        result_index_db,
        path.join(result_dir, "pack-" + pack_db.pack_checksum + ".idx"),
    )
    shutil.move(
        result_pack_db,
        path.join(result_dir, "pack-" + pack_db.pack_checksum + ".pack"),
    )

    print("Total Time: " + str(t1 - t0))


def testCommit():
    sample_commit = b"tree 09640a9d1c9862ee780816f25c5d0cb1668392e5\nparent b4b9d21d3d5a544ed1c2c127b6f169af38d1209d\nauthor AliRezaBeigy <AliRezaBeigyKhu@gmail.com> 1612593585 +0330\ncommitter AliRezaBeigy <AliRezaBeigyKhu@gmail.com> 1612593585 +0330\n\nUpdate README\n"
