def read_sales_file(file_path):
    try:
        with open(file_path, "r", encoding="latin-1") as file:
            lines = file.readlines()
        return lines
    except Exception as e:
        print("Error reading file:", e)
        return []
    
def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues

    Returns: list of raw lines (strings)
    """

    encodings = ['utf-8', 'latin-1', 'cp1252']

    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                lines = file.readlines()

            # Remove header (first line)
            data_lines = lines[1:]

            # Remove empty lines and strip whitespace
            cleaned_lines = []
            for line in data_lines:
                line = line.strip()
                if line:
                    cleaned_lines.append(line)

            return cleaned_lines

        except UnicodeDecodeError:
            # Try next encoding
            continue

        except FileNotFoundError:
            print(f"Error: File not found -> {filename}")
            return []

    print("Error: Unable to read file with supported encodings.")
    return [] 

def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    """

    transactions = []

    for line in raw_lines:
        parts = line.split('|')

        # Skip rows with incorrect number of fields
        if len(parts) != 8:
            continue

        (
            transaction_id,
            date,
            product_id,
            product_name,
            quantity,
            unit_price,
            customer_id,
            region
        ) = parts

        # Clean product name
        product_name = product_name.replace(',', '')

        # Clean numeric fields
        quantity = quantity.replace(',', '')
        unit_price = unit_price.replace(',', '')

        try:
            transaction = {
                'TransactionID': transaction_id,
                'Date': date,
                'ProductID': product_id,
                'ProductName': product_name,
                'Quantity': int(quantity),
                'UnitPrice': float(unit_price),
                'CustomerID': customer_id,
                'Region': region
            }

            transactions.append(transaction)

        except ValueError:
            continue

    return transactions



def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters
    """

    valid_transactions = []
    invalid_count = 0

    total_input = len(transactions)

    # Display available regions
    regions = set(t['Region'] for t in transactions)
    print("Available regions:", regions)

    # Display transaction amount range
    amounts = [t['Quantity'] * t['UnitPrice'] for t in transactions]
    print("Transaction amount range:", min(amounts), "-", max(amounts))

    filtered_by_region = 0
    filtered_by_amount = 0

    for t in transactions:
        # Validation rules
        if (
            t['Quantity'] <= 0 or
            t['UnitPrice'] <= 0 or
            not t['TransactionID'].startswith('T') or
            not t['ProductID'].startswith('P') or
            not t['CustomerID'].startswith('C')
        ):
            invalid_count += 1
            continue

        amount = t['Quantity'] * t['UnitPrice']

        # Region filter
        if region and t['Region'] != region:
            filtered_by_region += 1
            continue

        # Amount filters
        if min_amount and amount < min_amount:
            filtered_by_amount += 1
            continue

        if max_amount and amount > max_amount:
            filtered_by_amount += 1
            continue

        valid_transactions.append(t)

    summary = {
        'total_input': total_input,
        'invalid': invalid_count,
        'filtered_by_region': filtered_by_region,
        'filtered_by_amount': filtered_by_amount,
        'final_count': len(valid_transactions)
    }

    return valid_transactions, invalid_count, summary