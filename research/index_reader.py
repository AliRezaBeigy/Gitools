import operator
from os import path
from hashlib import sha1
from research.index_db import IndexDB
from research.index_object import IndexObject


def getIndexDB(hash: str, skip_fan_out=True):
    index_db = IndexDB()

    with open(f"pack-{hash}.idx", "rb") as file:
        index_db.signature = file.read(4)

        index_db.version = [
            int.from_bytes(file.read(1), "big"),
            int.from_bytes(file.read(1), "big"),
            int.from_bytes(file.read(1), "big"),
            int.from_bytes(file.read(1), "big"),
        ]

        if skip_fan_out:
            file.seek(255 * 4, 1)
        else:
            for _ in range(255):
                index_db.fan_out.append(int.from_bytes(file.read(4), "big"))

        index_db.total_object = int.from_bytes(file.read(4), "big")

        object_hashes: list[str] = []

        for _ in range(index_db.total_object):
            object_hash = file.read(sha1().digest_size).hex()
            object_hashes.append(object_hash)

        crc32_list: list[int] = []

        for _ in range(index_db.total_object):
            crc32 = int.from_bytes(file.read(4), "big")
            crc32_list.append(crc32)

        for index in range(index_db.total_object):
            pack_start_offset = int.from_bytes(file.read(4), "big")
            object_hash = object_hashes[index]

            index_db.objects[object_hash] = IndexObject(
                object_hash, crc32_list[index], pack_start_offset
            )
            index_db.pack_offsets[pack_start_offset] = object_hash

        del crc32_list
        del object_hashes

        index_db.pack_checksum = file.read(sha1().digest_size).hex()
        index_db.idx_checksum = file.read(sha1().digest_size).hex()

    sorted_idx_object = sorted(
        index_db.objects.values(), key=operator.attrgetter("pack_start_offset")
    )

    for i in range(len(sorted_idx_object) - 1):
        sorted_idx_object[i].pack_end_offset = sorted_idx_object[
            i + 1
        ].pack_start_offset

    pack_file_size: int = path.getsize(path.abspath(f"pack-{hash}.pack"))

    sorted_idx_object[len(sorted_idx_object) - 1].pack_end_offset = pack_file_size - 20

    return index_db
