import shutil
from time import time
from research.pack_db.pack_reader import getPackDB
from research.index_db.index_reader import getIndexDB
from research.pack_db.pack_writer import updateContent, writePack


def test():
    hash = "b14bbd4f6e5c90250dbfaeb101ecc468e4e1faf2"
    decompress_types = [1, 2, 3, 4, 5, 6, 7]

    t0 = time()

    index_db = getIndexDB(hash)
    pack_db = getPackDB(hash, index_db, decompress_types)

    new_hash = updateContent(pack_db, "2c2f01c7230c5dc09ffe20d3e597155be02172d6")

    hash = writePack(pack_db, decompress_types)

    index_db = getIndexDB(hash)
    pack_db = getPackDB(hash, index_db, decompress_types)

    t1 = time()

    shutil.move("pack-" + hash + ".idx", "pack-" + pack_db.pack_checksum + ".idx")
    shutil.move("pack-" + hash + ".pack", "pack-" + pack_db.pack_checksum + ".pack")

    print("Total Time: " + str(t1 - t0))


def testCommit():
    sample_commit = b"tree 09640a9d1c9862ee780816f25c5d0cb1668392e5\nparent b4b9d21d3d5a544ed1c2c127b6f169af38d1209d\nauthor AliRezaBeigy <AliRezaBeigyKhu@gmail.com> 1612593585 +0330\ncommitter AliRezaBeigy <AliRezaBeigyKhu@gmail.com> 1612593585 +0330\n\nUpdate README\n"
