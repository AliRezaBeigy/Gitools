import shutil
from time import time
from research.pack_reader import getPackDB
from research.index_reader import getIndexDB
from research.pack_writer import updateContent, writePack

if __name__ == "__main__":
    hash = "888dbc9d9e3501abd469adf9d98da898964b5262"
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