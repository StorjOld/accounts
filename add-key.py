import accounts
import settings
import argparse

def add_key(key):
    accounts.Manager(settings.DATABASE_PATH).add_key(key)

def main():
    parser = argparse.ArgumentParser(
            description='Adds an API key to metadisk-accounts.')

    parser.add_argument('key')

    options = parser.parse_args()

    add_key(options.key)

if __name__ == '__main__':
    main()
