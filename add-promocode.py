#!/usr/bin/env python

import accounts
import settings
import argparse

def add_promocode(code, bytes):
    accounts.Manager(settings.DATABASE_PATH).add_promocode(code, bytes)

def main():
    parser = argparse.ArgumentParser(
            description='Adds a promocode to metadisk-accounts.')

    parser.add_argument('promocode')
    parser.add_argument('bytes', type=int)

    options = parser.parse_args()

    add_promocode(options.promocode, options.bytes)

if __name__ == '__main__':
    main()
