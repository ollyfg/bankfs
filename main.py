#!/usr/bin/env python3

import os
import sys
import errno
import time

from fuse import FUSE, FuseOSError, Operations

class File():
    def __init__(self):
        self.header = {
            'updated_at': int(time.time())
        }
        self.body = b''

files = []

class BankFS(Operations):
    def __init__(self, root):
        self.root = root

    # Helpers
    # =======

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    # Filesystem methods
    # ==================

    def access(self, path, mode):
        try:
            if path == "/":
                return 0
            fname = path[1:]
            file = [f for f in files if f.header["name"] == fname][0]
            return 0
        except IndexError as e:
            raise FuseOSError(errno.EACCES)

    def chmod(self, path, mode):
        return 0

    def chown(self, path, uid, gid):
        return 0

    def getattr(self, path, fh=None):
        if path == "/":
            return {
                "st_atime": int(time.time()),
                "st_mtime": int(time.time()),
                "st_ctime": int(time.time()),
                "st_mode": 16877,
                "st_nlink": 5,
                "st_size": 160,
                "st_gid": 0,
                "st_uid": 0
            }
        # Get the file header
        # For now, just return placeholder...
        try:
            fname = path[1:]
            file = [f for f in files if f.header["name"] == fname][0]
            return {
                "st_atime": file.header["mode"],
                "st_mtime": file.header["mode"],
                "st_ctime": file.header["mode"],
                "st_mode": file.header["mode"],
                # "st_mode": 33188,
                "st_nlink": 1,
                "st_size": len(file.body),
                "st_gid": 0,
                "st_uid": 0
            }
        except IndexError as e:
            raise FuseOSError(errno.ENOENT)

    def readdir(self, path, fh):
        # Get files from the last 7 days
        return [".", ".."] + [f.header["name"] for f in files]

    def readlink(self, path):
        return 0

    def mknod(self, path, mode, dev):
        return 0

    def rmdir(self, path):
        return 0

    def mkdir(self, path, mode):
        return 0

    def statfs(self, path):
        return {'f_bavail': 5107109, 'f_bfree': 57462189, 'f_blocks': 61202533, 'f_bsize': 1048576, 'f_favail': 2447547563, 'f_ffree': 2447547563, 'f_files': 2448101320, 'f_flag': 1, 'f_frsize': 4096, 'f_namemax': 255}

    def unlink(self, path):
        return 0

    def symlink(self, name, target):
        return 0

    def rename(self, old, new):
        return 0

    def link(self, target, name):
        return 0

    def utimens(self, path, times=None):
        return 0

    # File methods
    # ============

    def open(self, path, flags):
        return 0

    def create(self, path, mode, fi=None):
        fname = path[1:]
        filenames = [f.header["name"] for f in files]
        if fname in filenames:
            raise FuseOSError(errno.EEXIST)
        file = File()
        file.header["name"] = fname
        file.header["mode"] = mode
        files.append(file)
        return 0

    def read(self, path, length, offset, fh):
        # Find and read the file
        # For now, just return placeholder
        try:
            fname = path[1:]
            file = [f for f in files if f.header["name"] == fname][0]
            return file.body[offset:length]
        except IndexError as e:
            raise FuseOSError(errno.ENOENT)

    def write(self, path, buf, offset, fh):
        # Make some transfers!
        try:
            fname = path[1:]
            file = [f for f in files if f.header["name"] == fname][0]
            file.body = file.body[:offset] + buf + file.body[offset + (len(buf)):]
            file.header["updated_at"] = int(time.time())
            return len(buf)
        except IndexError as e:
            raise FuseOSError(errno.ENOENT)

    def truncate(self, path, length, fh=None):
        try:
            fname = path[1:]
            file = [f for f in files if f.header["name"] == fname][0]
            file.body = file.body[:length]
            file.header["updated_at"] = int(time.time())
            return 0
        except IndexError as e:
            raise FuseOSError(errno.ENOENT)

    def flush(self, path, fh):
        return 0

    def release(self, path, fh):
        return 0

    def fsync(self, path, fdatasync, fh):
        return 0


def main(mountpoint, root):
    FUSE(BankFS(root), mountpoint, nothreads=True, foreground=True)

if __name__ == '__main__':
    main(sys.argv[2], sys.argv[1])
