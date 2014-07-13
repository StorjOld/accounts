#!/usr/bin/env python

import accounts
import settings
import argparse

def add_promocode(code):
    accounts.Manager(settings.DATABASE_PATH).add_promocode(code)

def main():
    parser = argparse.ArgumentParser(
            description='Adds a promocode to metadisk-accounts.')

    parser.add_argument('promocode')

    options = parser.parse_args()

    add_promocode(options.promocode)

if __name__ == '__main__':
    main()
