import zlib
from os import path
from io import BytesIO
from hashlib import sha1
from core.pack_db.pack_db import PackDB
from core.index_db.index_db import IndexDB
from core.index_db.index_object import IndexObject
from core.pack_db.pack_object import PackObject


def writePack(
    pack_path: str, pack_db: PackDB, compress_types: list[int] = [1, 2, 3, 4, 5, 6, 7]
):
    index_db = IndexDB()
    fan_out: dict[int, int] = {}

    pack_file = BytesIO()
    signature = pack_db.signature
    pack_file.write(signature)

    version = pack_db.version
    pack_file.write((version[0]).to_bytes(1, "big"))
    pack_file.write((version[1]).to_bytes(1, "big"))
    pack_file.write((version[2]).to_bytes(1, "big"))
    pack_file.write((version[3]).to_bytes(1, "big"))

    pack_file.write(pack_db.total_object.to_bytes(4, "big"))

    for k in sorted(pack_db.objects):
        v = pack_db.objects[k]
        pack_offset = pack_file.tell()

        fh = int(k[:2], 16)
        if fh in fan_out:
            fan_out[fh] += 1
        else:
            if fh == 0:
                fan_out[fh] = 1
            else:

                def fill_fan_out(c, fan_out):
                    if not c in fan_out:
                        if c == 0:
                            fan_out[c] = 0
                            return
                        if not c - 1 in fan_out and c != 0:
                            fill_fan_out(c - 1, fan_out)
                        fan_out[c] = fan_out[c - 1]

                fill_fan_out(fh - 1, fan_out)
                fan_out[fh] = fan_out[fh - 1] + 1

        type: int = v.type << 4
        data_size = v.object_size

        size_bits: list[int] = [data_size & int("00001111", 2)]
        data_size >>= 4
        while data_size > 0:
            size_bits.insert(0, data_size & int("01111111", 2))
            data_size >>= 7

        msb = int("10000000", 2) if len(size_bits) > 1 else int("00000000", 2)

        pack_file.write((msb + type + size_bits.pop()).to_bytes(1, "big"))

        while len(size_bits) > 0:
            msb = int("10000000", 2) if len(size_bits) > 1 else int("00000000", 2)
            pack_file.write((msb + size_bits.pop()).to_bytes(1, "big"))

        if v.type in [7]:
            pack_file.write(v.ref)

        if v.type in compress_types:
            pack_file.write(zlib.compress(v.data))
        else:
            pack_file.write(v.data)

        current_cursor = pack_file.tell()
        pack_file.seek(pack_offset, 0)
        crc32 = zlib.crc32(pack_file.read(current_cursor - pack_offset))

        index_db.objects[k] = IndexObject(k, crc32, pack_offset)

        index_db.fan_out = list(fan_out.values())

        pack_file.seek(0, 0)
        index_db.pack_checksum = sha1(pack_file.read()).digest()
        pack_file.write(index_db.pack_checksum)

    index_file = BytesIO()
    index_file.write(b"\xfftOc")
    index_file.write((0).to_bytes(1, "big"))
    index_file.write((0).to_bytes(1, "big"))
    index_file.write((0).to_bytes(1, "big"))
    index_file.write((2).to_bytes(1, "big"))

    for v in index_db.fan_out:
        index_file.write(v.to_bytes(4, "big"))

    for k in index_db.objects:
        index_file.write(int(k, 16).to_bytes(20, "big"))

    for _, v in index_db.objects.items():
        index_file.write(v.crc32.to_bytes(4, "big"))

    for _, v in index_db.objects.items():
        index_file.write(v.pack_start_offset.to_bytes(4, "big"))

    index_file.write(index_db.pack_checksum)

    index_file.seek(0, 0)
    idx_checksum = sha1(index_file.read()).digest()
    index_file.write(idx_checksum)
    pack_db.pack_checksum = idx_checksum.hex()
    
    with open(path.join(pack_path, f"pack-{pack_db.pack_checksum}.pack"), "wb+") as file:
        pack_file.seek(0)
        file.write(pack_file.read())

    with open(path.join(pack_path, f"pack-{pack_db.pack_checksum}.idx"), "wb+") as file:
        index_file.seek(0)
        file.write(index_file.read())
    
    return pack_db.pack_checksum


def updateObject(pack_db: PackDB, object: PackObject, old: str, new: str):
    if object.data.find(old) < 0:
        return

    object_hash = object.hash

    object.data = object.data.replace(old, new)
    object.object_size = len(object.data)

    content = str(object.object_size).encode("utf-8") + b"\x00" + object.data

    if object.type == 1:
        content = b"commit " + content
    elif object.type == 2:
        content = b"tree " + content
    elif object.type == 3:
        content = b"blob " + content
    else:
        raise Exception("This type does not supported.")

    new_hash = sha1(content).hexdigest()

    if new_hash == object_hash:
        return

    object.hash = new_hash
    pack_db.objects[new_hash] = object
    del pack_db.objects[object_hash]

    object_key_index = 0
    object_keys = list(pack_db.objects.keys())
    object_key_len = len(object_keys)
    while object_key_index < object_key_len:
        obj = pack_db.objects[object_keys[object_key_index]]
        object_key_index += 1

        if obj.type == 3:
            continue

        if obj.type == 1:
            encoded_hash = object_hash.encode()
            if obj.data.find(encoded_hash) >= 0:
                updateObject(pack_db, obj, encoded_hash, new_hash.encode())
                object_key_index = 0
                object_keys = list(pack_db.objects.keys())

        if obj.type == 2:
            hash_bytes = int(object_hash, 16).to_bytes(20, "big")
            if obj.data.find(hash_bytes) >= 0:
                updateObject(
                    pack_db, obj, hash_bytes, int(new_hash, 16).to_bytes(20, "big")
                )
                object_key_index = 0
                object_keys = list(pack_db.objects.keys())

        if obj.ref:
            if obj.ref.hex() == object_hash:
                raise Exception("This type does not supported.")

    print(object_hash + " -> " + new_hash)
    return new_hash
