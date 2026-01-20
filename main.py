# main.py

from utils.file_handler import read_sales_file
from utils.data_processor import clean_and_validate_data

def main():
    file_path = "data/sales_data.txt"

    lines = read_sales_file(file_path)
    valid_data = clean_and_validate_data(lines)

    # Later you can add analytics here
    # For now, cleaning is enough

if __name__ == "__main__":
    main()

