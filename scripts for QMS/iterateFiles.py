import os
import sys


def iterateFiles(dirPath):
    """
    a generator
    :param dirPath: directory path
    :return: file Path for each file in this directory
    """
    if not os.path.isdir(dirPath):
        print(f'Error: {dirPath} is not a directory.')
        return
    with os.scandir(dirPath) as d:
        for entry in d:
            if not entry.name.startswith('.') and entry.is_file():
                yield entry.path



def main():
    if len(sys.argv) < 2:
        print(f'Error: one more argument is required: directory path.')
        return
    dp = sys.argv[1]
    count = 1
    for file in iterateFiles(dp):
        print(f'count {count}')
        print(file)
        count += 1




if __name__ == "__main__":
    main()