import argparse
import os

import pyminizip


def parse_arguments():
    parser = argparse.ArgumentParser(description='DM-Bot')
    parser.add_argument('--name', help='Name of the file to be added to the protected archive')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    name = args.name
    if name:
        pyminizip.compress(name, None, name[:-4] + ".zip", b"1Ei2ttDIBadNmDHqh3HRIWpipnxh7DwNM", 0) 
    else:
        print("Specify filename using argument --name")
