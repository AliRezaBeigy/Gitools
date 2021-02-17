from research.index_object import IndexObject


class IndexDB:
    signature: bytes
    total_object: int
    idx_checksum: str
    version: list[int]
    fan_out: list[int]
    pack_checksum: str
    pack_offsets: dict[int, str]
    objects: dict[str, IndexObject]

    def __init__(self):
        self.fan_out = []
        self.objects = {}
        self.pack_offsets = {}