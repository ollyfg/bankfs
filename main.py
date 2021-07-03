#!/usr/bin/env python3

# This file deals with the filesystem stuff, transalting to to API calls for Akahu.

import os
import sys
import errno
import time
import zlib

from fuse import FUSE, FuseOSError, Operations

from file import File
from akahu import AkahuApi

class BankFS(Operations):
    def __init__(self):
        # Initialise the Akahu Api client
        self.akahu = AkahuApi()
        # Our in-memory cache
        self.files = self.akahu.read_all()
        print("Loaded all existing files into cache. You can now use the filesystem!")

    # Filesystem methods
    # ==================

    def access(self, path, mode):
        try:
            if path == "/":
                return 0
            fname = path[1:]
            file = [f for f in self.files if f.header["name"] == fname][0]
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
            file = [f for f in self.files if f.header["name"] == fname][0]
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
        return [".", ".."] + [f.header["name"] for f in self.files]

    def readlink(self, path):
        return 0

    def mknod(self, path, mode, dev):
        return 0

    def rmdir(self, path):
        return 0

    def mkdir(self, path, mode):
        return 0

    def statfs(self, path):
        return {'f_bavail': 5107109, 'f_bfree': 57462189, 'f_blocks': 61202533, 'f_bsize': 1048576, 'f_favail': 2447547563, 'f_ffree': 2447547563, 'f_files': 2448101320, 'f_flag': 1, 'f_frsize': 4096, 'f_namemax': 32}

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
        filenames = [f.header["name"] for f in self.files]
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
            file = [f for f in self.files if f.header["name"] == fname][0]
            return file.body[offset:length]
        except IndexError as e:
            raise FuseOSError(errno.ENOENT)

    def write(self, path, buf, offset, fh):
        # Make some transfers!
        # Append only, because of the underlying storage

        try:
            fname = path[1:]
            file = [f for f in self.files if f.header["name"] == fname][0]
            compressed = zlib.compress(buf)
            print("write!", path, buf)
            # Write to Akahu

            # Write the in-memory file object
            file.body = buf
            file.header["updated_at"] = int(time.time())
            return len(buf)
        except IndexError as e:
            raise FuseOSError(errno.ENOENT)

    def truncate(self, path, length, fh=None):
        return 0
    def flush(self, path, fh):
        return 0

    def release(self, path, fh):
        return 0

    def fsync(self, path, fdatasync, fh):
        return 0


def main(mountpoint):
    FUSE(BankFS(), mountpoint, nothreads=True, foreground=True)

if __name__ == '__main__':
    main(sys.argv[1])
