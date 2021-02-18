import zlib
import random
from os import path
from hashlib import sha1
from research.pack_db.pack_db import PackDB
from research.index_db.index_db import IndexDB
from research.index_db.index_object import IndexObject


def writePack(pack_db: PackDB, compress_types: list[int]):
    hash = sha1(b"a" * random.randint(1, 150)).hexdigest()

    index_db = IndexDB()
    fan_out: dict[int, int] = {}

    with open(path.join("research", "samples", f"pack-{hash}.pack"), "wb+") as file:
        signature = pack_db.signature
        file.write(signature)

        version = pack_db.version
        file.write((version[0]).to_bytes(1, "big"))
        file.write((version[1]).to_bytes(1, "big"))
        file.write((version[2]).to_bytes(1, "big"))
        file.write((version[3]).to_bytes(1, "big"))

        file.write(pack_db.total_object.to_bytes(4, "big"))

        for k in sorted(pack_db.objects):
            v = pack_db.objects[k]
            pack_offset = file.tell()

            fh = int(k[:2], 16)
            try:
                fan_out[fh] += 1
            except:
                if fh == 0:
                    fan_out[fh] = 1
                else:
                    fan_out[fh] = fan_out[fh - 1] + 1

            type: int = v.type << 4
            data_size = v.object_size

            size_bits: list[int] = [data_size & int("00001111", 2)]
            data_size >>= 4
            while data_size > 0:
                size_bits.insert(0, data_size & int("01111111", 2))
                data_size >>= 7

            msb = int("10000000", 2) if len(size_bits) > 1 else int("00000000", 2)

            file.write((msb + type + size_bits.pop()).to_bytes(1, "big"))

            while len(size_bits) > 0:
                msb = int("10000000", 2) if len(size_bits) > 1 else int("00000000", 2)
                file.write((msb + size_bits.pop()).to_bytes(1, "big"))

            if v.type in [7]:
                file.write(v.ref)

            if v.type in compress_types:
                file.write(zlib.compress(v.data))
            else:
                file.write(v.data)

            current_cursor = file.tell()
            file.seek(pack_offset, 0)
            crc32 = zlib.crc32(file.read(current_cursor - pack_offset))

            index_db.objects[k] = IndexObject(k, crc32, pack_offset)

        index_db.fan_out = list(fan_out.values())

        file.seek(0, 0)
        index_db.pack_checksum = sha1(file.read()).digest()
        file.write(index_db.pack_checksum)

    with open(path.join("research", "samples", f"pack-{hash}.idx"), "wb+") as file:
        file.write(b"\xfftOc")
        file.write((0).to_bytes(1, "big"))
        file.write((0).to_bytes(1, "big"))
        file.write((0).to_bytes(1, "big"))
        file.write((2).to_bytes(1, "big"))

        for v in index_db.fan_out:
            file.write(v.to_bytes(4, "big"))

        for k in index_db.objects:
            file.write(int(k, 16).to_bytes(20, "big"))

        for _, v in index_db.objects.items():
            file.write(v.crc32.to_bytes(4, "big"))

        for _, v in index_db.objects.items():
            file.write(v.pack_start_offset.to_bytes(4, "big"))

        file.write(index_db.pack_checksum)

        file.seek(0, 0)
        idx_checksum = sha1(file.read()).digest()
        file.write(idx_checksum)

    return hash


def updateContent(pack_db: PackDB, hash: str, old: str, new: str):
    object = pack_db.objects[hash]

    if object.data.find(b"test") < 0:
        return

    object.data = object.data.replace(b"test", b"test Heh Heh Heh Heh Heh")
    object.object_size = len(object.data)

    content = str(len(object.data)).encode("utf-8") + b"\x00" + object.data

    if object.type == 1:
        content = b"commit " + content

    new_hash = sha1(content).hexdigest()

    object.hash = new_hash
    pack_db.objects[new_hash] = object
    del pack_db.objects[hash]

    for k in pack_db.objects:
        obj = pack_db.objects[k]
        obj.data = obj.data.replace(hash.encode(), new_hash.encode())
        obj.data = obj.data.replace(
            int(hash, 16).to_bytes(20, "big"), int(new_hash, 16).to_bytes(20, "big")
        )
        if obj.ref:
            if obj.ref.hex() == hash:
                sa = 1 + 5
            # obj.ref = obj.ref.replace(
            #     int(hash, 16).to_bytes(20, 'big'), int(new_hash, 16).to_bytes(20, 'big'))

    return new_hash