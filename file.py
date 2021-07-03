import time

# A basic in-memory representation of a file
class File():
    header = {}
    body = b''

    def __init__(self):
        self.header['updated_at'] = int(time.time())
