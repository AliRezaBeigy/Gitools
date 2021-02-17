class IndexObject:
    hash: str
    crc32: int
    pack_end_offset: int
    pack_start_offset: int

    def __init__(self, hash: str, crc32: int, pack_start_offset: int):
        self.hash = hash
        self.crc32 = crc32
        self.pack_start_offset = pack_start_offset