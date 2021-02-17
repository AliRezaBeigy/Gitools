import zlib
from hashlib import sha1
from io import BufferedReader
from research.pack_db import PackDB
from research.index_db import IndexDB
from research.pack_object import PackObject


def getPackObject(
    hash: str,
    index_db: IndexDB,
    pack_offset: int,
    file: BufferedReader,
    pack_object_size: int,
    decompress_types: list[int],
) -> PackDB:
    file.seek(pack_offset, 0)

    pack_object = PackObject(hash)

    n_byte = file.read(1)[0]
    pack_object.type = (n_byte & int("01110000", 2)) >> 4

    diff_data_offset = 1

    object_size_len = 4
    pack_object.object_size = n_byte & int("00001111", 2)
    while (n_byte & int("10000000", 2)) >> 7 == 1:
        n_byte = file.read(1)[0]
        pack_object.object_size += (1 << object_size_len) * (
            n_byte & int("01111111", 2)
        )
        object_size_len += 7
        diff_data_offset += 1

    if pack_object.type in [1, 2, 3, 4]:
        if pack_object.type in decompress_types:
            pack_object.data = zlib.decompress(
                file.read(pack_object_size - diff_data_offset)
            )
        else:
            pack_object.data = file.read(pack_object_size - diff_data_offset)

    elif pack_object.type in [6]:
        n_byte = file.read(1)[0]
        diff_data_offset += 1

        offset = n_byte & int("01111111", 2)

        while (n_byte & int("10000000", 2)) >> 7 == 1:
            offset += 1
            offset <<= 7
            n_byte = file.read(1)[0]
            offset += n_byte & int("01111111", 2)
            diff_data_offset += 1

        if pack_object.type in decompress_types:
            pack_object.data = zlib.decompress(
                file.read(pack_object_size - diff_data_offset)
            )
        else:
            pack_object.data = file.read(pack_object_size - diff_data_offset)

        pack_object.type = 7
        pack_object.ref = int(index_db.pack_offsets[pack_offset - offset], 16).to_bytes(
            20, "big"
        )

    elif pack_object.type in [7]:
        pack_object.ref = file.read(sha1().digest_size)
        diff_data_offset += sha1().digest_size

        if pack_object.type in decompress_types:
            pack_object.data = zlib.decompress(
                file.read(pack_object_size - diff_data_offset)
            )
        else:
            pack_object.data = file.read(pack_object_size - diff_data_offset)

    return pack_object


def getPackDB(hash: str, index_db: IndexDB, decompress_types: list[int]):
    pack_db = PackDB()

    with open(f"pack-{hash}.pack", "rb") as file:
        pack_db.signature = file.read(4)

        pack_db.version = [
            int.from_bytes(file.read(1), "big"),
            int.from_bytes(file.read(1), "big"),
            int.from_bytes(file.read(1), "big"),
            int.from_bytes(file.read(1), "big"),
        ]

        pack_db.total_object = int.from_bytes(file.read(4), "big")

        for k, v in index_db.objects.items():
            pack_object = getPackObject(
                hash=k,
                file=file,
                index_db=index_db,
                pack_offset=v.pack_start_offset,
                decompress_types=decompress_types,
                pack_object_size=v.pack_end_offset - v.pack_start_offset,
            )
            pack_db.objects[k] = pack_object

        file.seek(-20, 2)
        pack_db.pack_checksum = file.read(sha1().digest_size).hex()

    return pack_db