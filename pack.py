import argparse
import os

import pyminizip


def parse_arguments():
    parser = argparse.ArgumentParser(description='DM-Bot')
    parser.add_argument('--file1', help='Name of the first file to be added to the protected archive')
    parser.add_argument('--file2', help='Name of the second file to be added to the protected archive')
    parser.add_argument('--output', help='Name of the output archive')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    file1 = args.file1
    file2 = args.file2
    output_zip_name = args.output + ".zip" if args.output else "archive.zip"

    if file1 or file2:
        # Пароль для архива
        password = b"1Ei2ttDIBadNmDHqh3HRIWpipnxh7DwNM"
        
        # Упаковка двух файлов в архив
        pyminizip.compress_multiple([file1, file2], [None, None], output_zip_name, password, 0)
        
        print(f"File(s) are compressed into {output_zip_name}")
    else:
        print("Specify filenames using arguments --file1 and --file2")
