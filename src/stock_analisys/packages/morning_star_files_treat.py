from pathlib import Path
import stock_analisys.packages.paths as paths
import os 


def files(path):
    """Yields the name of all files inside a directory

    Args:
        path (Path): the path to the folder

    Yields:
        generator: takes only the name of each file inside a folder
    """
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file

def main():
    """
    Takes all files from files
    Removes the first line from each file 

    """
    folder_path = paths.morning_star_path / 'key_ratios'

    for file in files(folder_path):
        with open(folder_path / file, 'r') as fin:
            data = fin.read().splitlines(True)
        with open(folder_path / file, 'w') as fout:
            fout.writelines(data[1:])

if __name__ == "__main__":
    main()