def clean_and_validate_data(lines):
    total_records = 0
    invalid_records = 0
    valid_records = []

    for index, line in enumerate(lines):
        line = line.strip()

        if index == 0:
            continue
            

        if not line:
            continue

        total_records += 1
        parts = line.split("|")

        if len(parts) != 8:
            invalid_records += 1
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

        if not transaction_id.startswith("T"):
            invalid_records += 1
            continue

        if not customer_id or not region:
            invalid_records += 1
            continue

        product_name = product_name.replace(",", "")

        try:
            quantity = int(quantity)
            unit_price = float(unit_price.replace(",", ""))
        except:
            invalid_records += 1
            continue

        if quantity <= 0 or unit_price <= 0:
            invalid_records += 1
            continue

        valid_records.append({
            "TransactionID": transaction_id,
            "Date": date,
            "ProductID": product_id,
            "ProductName": product_name,
            "Quantity": quantity,
            "UnitPrice": unit_price,
            "CustomerID": customer_id,
            "Region": region
        })

    print(f"Total records parsed: {total_records}")
    print(f"Invalid records removed: {invalid_records}")
    print(f"Valid records after cleaning: {len(valid_records)}")

    return valid_records