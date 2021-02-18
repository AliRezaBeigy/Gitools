class PackObject:
    type: int
    hash: str
    ref: bytes
    data: bytes
    object_size: int

    def __init__(self, hash: str):
        self.type = 0
        self.ref = None
        self.hash = hash