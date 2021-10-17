from core.pack_db.pack_object import PackObject


class PackDB:
    signature: bytes
    total_object: int
    version: list[int]
    pack_checksum: str
    objects: dict[str, PackObject]

    def __init__(self):
        self.objects = {}