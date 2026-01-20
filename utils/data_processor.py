def clean_and_validate_data(lines):
    valid_records = []

    for index, line in enumerate(lines):
        line = line.strip()

        # Skip header
        if index == 0:
            continue

        if not line:
            continue

        parts = line.split("|")
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

        if not transaction_id.startswith("T"):
            continue

        if not customer_id or not region:
            continue

        try:
            quantity = int(quantity)
            unit_price = float(unit_price.replace(",", ""))
        except ValueError:
            continue

        if quantity <= 0 or unit_price <= 0:
            continue

        valid_records.append({
            "TransactionID": transaction_id,
            "Date": date,
            "ProductID": product_id,
            "ProductName": product_name.replace(",", ""),
            "Quantity": quantity,
            "UnitPrice": unit_price,
            "CustomerID": customer_id,
            "Region": region
        })

    print(f"Valid records after cleaning: {len(valid_records)}")
    return valid_records


def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions
    """

    total_revenue = 0.0

    for t in transactions:
        total_revenue += t['Quantity'] * t['UnitPrice']

    return total_revenue

def region_wise_sales(transactions):
    """
    Analyzes sales by region
    """

    region_data = {}
    overall_sales = 0.0

    # First pass: total sales and counts
    for t in transactions:
        region = t['Region']
        amount = t['Quantity'] * t['UnitPrice']
        overall_sales += amount

        if region not in region_data:
            region_data[region] = {
                'total_sales': 0.0,
                'transaction_count': 0
            }

        region_data[region]['total_sales'] += amount
        region_data[region]['transaction_count'] += 1

    # Second pass: calculate percentage
    for region in region_data:
        region_data[region]['percentage'] = round(
            (region_data[region]['total_sales'] / overall_sales) * 100, 2
        )

    # Sort by total_sales descending
    sorted_regions = dict(
        sorted(
            region_data.items(),
            key=lambda x: x[1]['total_sales'],
            reverse=True
        )
    )

    return sorted_regions

def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold
    """

    product_data = {}

    for t in transactions:
        name = t['ProductName']
        qty = t['Quantity']
        revenue = qty * t['UnitPrice']

        if name not in product_data:
            product_data[name] = {
                'quantity': 0,
                'revenue': 0.0
            }

        product_data[name]['quantity'] += qty
        product_data[name]['revenue'] += revenue

    sorted_products = sorted(
        product_data.items(),
        key=lambda x: x[1]['quantity'],
        reverse=True
    )

    result = []
    for name, data in sorted_products[:n]:
        result.append((name, data['quantity'], data['revenue']))

    return result

def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns
    """

    customer_data = {}

    for t in transactions:
        customer_id = t['CustomerID']
        amount = t['Quantity'] * t['UnitPrice']
        product = t['ProductName']

        if customer_id not in customer_data:
            customer_data[customer_id] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'products': set()
            }

        customer_data[customer_id]['total_spent'] += amount
        customer_data[customer_id]['purchase_count'] += 1
        customer_data[customer_id]['products'].add(product)

    result = {}

    for cid, data in customer_data.items():
        result[cid] = {
            'total_spent': data['total_spent'],
            'purchase_count': data['purchase_count'],
            'avg_order_value': round(
                data['total_spent'] / data['purchase_count'], 2
            ),
            'products_bought': list(data['products'])
        }

    return dict(
        sorted(
            result.items(),
            key=lambda x: x[1]['total_spent'],
            reverse=True
        )
    )

def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date
    """

    daily_data = {}

    for t in transactions:
        date = t['Date']
        revenue = t['Quantity'] * t['UnitPrice']
        customer = t['CustomerID']

        if date not in daily_data:
            daily_data[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'customers': set()
            }

        daily_data[date]['revenue'] += revenue
        daily_data[date]['transaction_count'] += 1
        daily_data[date]['customers'].add(customer)

    result = {}
    for date in sorted(daily_data.keys()):
        result[date] = {
            'revenue': daily_data[date]['revenue'],
            'transaction_count': daily_data[date]['transaction_count'],
            'unique_customers': len(daily_data[date]['customers'])
        }

    return result

def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue
    """

    daily = daily_sales_trend(transactions)

    peak_date = None
    max_revenue = 0.0
    peak_count = 0

    for date, data in daily.items():
        if data['revenue'] > max_revenue:
            max_revenue = data['revenue']
            peak_date = date
            peak_count = data['transaction_count']

    return (peak_date, max_revenue, peak_count)

def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales
    """

    product_data = {}

    for t in transactions:
        name = t['ProductName']
        qty = t['Quantity']
        revenue = qty * t['UnitPrice']

        if name not in product_data:
            product_data[name] = {
                'quantity': 0,
                'revenue': 0.0
            }

        product_data[name]['quantity'] += qty
        product_data[name]['revenue'] += revenue

    result = []

    for name, data in product_data.items():
        if data['quantity'] < threshold:
            result.append((name, data['quantity'], data['revenue']))

    result.sort(key=lambda x: x[1])  # sort by quantity ascending

    return result

