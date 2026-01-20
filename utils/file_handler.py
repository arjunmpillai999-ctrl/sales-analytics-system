# utils/file_handler.py

def read_sales_file(file_path):
    """
    Reads the sales data file and returns all lines
    """
    try:
        with open(file_path, "r", encoding="latin-1") as file:
            lines = file.readlines()
        return lines
    except Exception as e:
        print(f"Error reading file: {e}")
        return []
