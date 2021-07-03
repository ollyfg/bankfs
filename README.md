Store your files... in your bank!

# The Problem

The world is full of cyber criminals, identity thieves, and ransomware.

How do you keep your private files safe? Where can you store them securely? Who do you trust?

# The Solution

You keep your files where you keep your money - in the bank!

# Running it

python3 main.py / /Volumes/bfs

# How it works

When the filesystem is mounted, it goes and fetches your transactions from the bank, before parsing them to extract your files. These are cached in memory so we get reasonable read times.

When you read a file, it is fetched from the cache and served to you.

When you write a file, we first write the file to your bank, before making an in-memory file object. This is the slow bit...

# Config

BankFS supports the following configuration via environment variables:

- `BANKFS_LOOKUP_START` The date you first start using BankFS. BankFS will not look at transactions earlier than this.
- `BANKFS_AKAHU_USER_TOKEN` Your Akahu user token. It must be allowed to access exactly two accounts that can make transfers. While they don't strictly **have** to be from the same bank, you will find writes much faster if they are.
- `BANKFS_AKAHU_APP_ID` Your Akahu app ID.
