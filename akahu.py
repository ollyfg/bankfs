#!/usr/bin/env python3

# This file deals with making the requests to the Akahu API.

import requests
import os
from file import File


class AkahuApi():
    lookup_start = None
    user_token = None
    app_id = None
    primary_account_id = None
    mirror_account_id = None

    def __init__(self):
        # Set up environment variables
        if "BANKFS_LOOKUP_START" not in os.environ:
            raise Exception("Missing 'BANKFS_LOOKUP_START' environment variable")
        if "BANKFS_AKAHU_USER_TOKEN" not in os.environ:
            raise Exception("Missing 'BANKFS_AKAHU_USER_TOKEN' environment variable")
        if "BANKFS_AKAHU_APP_ID" not in os.environ:
            raise Exception("Missing 'BANKFS_AKAHU_APP_ID' environment variable")
        self.lookup_start = os.environ["BANKFS_LOOKUP_START"]
        self.user_token = os.environ["BANKFS_AKAHU_USER_TOKEN"]
        self.app_id = os.environ["BANKFS_AKAHU_APP_ID"]
        # Get the accounts we will be using
        result = self._call("/accounts")
        account_ids = [acc["_id"] for acc in result["items"] if "TRANSFER_TO" in acc["attributes"] and "TRANSFER_FROM" in acc["attributes"]]
        account_ids.sort()
        if len(account_ids) != 2:
            print("Found %d accounts that can transfer"%(account_ids))
            raise Exception("You must have access to exactly two accounts that can make + receive transfers")
        self.primary_account_id = account_ids[0]
        self.mirror_account_id = account_ids[1]
        print("Initialised Akahu layer using the following two accounts: %s (primary) and %s (mirror)"%(self.primary_account_id, self.mirror_account_id))

    # Make a call to the Akahu API
    def _call(self, endpoint, method="GET", payload=None):
        return {
            'success': True,
            'items': [
                {
                    '_id': "acc_123",
                    'attributes': ["TRANSFER_TO", "TRANSFER_FROM"]
                },
                {
                    '_id': "acc_234",
                    'attributes': ["TRANSFER_TO", "TRANSFER_FROM"]
                }
            ]
        }

    # Read all of the transactions up to our `lookup_start`
    def _get_transactions(self):
        return []

    # Extract files from a list of transactions
    def _extract_files(self, transactions):
        return []

    # Write the provided bytes as a series of transfers
    def write(self, bytes):
        return

    # Reads out all the files we have stored in the FS
    def read_all(self):
        transactions = self._get_transactions()
        files = self._extract_files(transactions)
        return files
