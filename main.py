import zipfile as zf
import re
import os


def main():
    """Finds all .zip files in the custom cards folder, extracts all cards from each,
        parses the card name from the file name, and then renames the files (if they haven't been parsed previously).
    """

    name_pattern = re.compile("(.*?)(-\\w{3,4}-.*)")
    double_card_pattern = re.compile("(.*) -- (.*)")

    directory = input("Copy the path for the custom cards folder: ")
    zip_files = [file for file in os.listdir(directory) if zf.is_zipfile(file)]

    for zip_file in zip_files:
        with zf.ZipFile(os.path.join(directory, zip_file)) as f:
            for file in f.namelist():
                file_name, ext = os.path.splitext(file)
                name_match = name_pattern.match(file_name)
                card_name = name_match.group(1)
                double_card_match =  double_card_pattern.match(card_name)
                if double_card_match is not None:
                    card_name = double_card_match.group(1) + double_card_match.group(2)
                new_abs_path = os.path.join(directory, card_name + ext)
                if not os.path.exists(new_abs_path):
                    f.extract(file, directory)
                    abs_path = os.path.join(directory, file)
                    os.rename(abs_path, new_abs_path)
        os.remove(os.path.join(directory, zip_file))

if __name__ == "__main__":
    main()