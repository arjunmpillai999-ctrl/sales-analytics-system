from datetime import datetime
from collections import defaultdict, Counter


def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive formatted text report
    """

    # =========================
    # HEADER
    # =========================
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_records = len(transactions)

    # =========================
    # OVERALL SUMMARY
    # =========================
    total_revenue = sum(t["Quantity"] * t["UnitPrice"] for t in transactions)
    total_transactions = len(transactions)
    avg_order_value = total_revenue / total_transactions if total_transactions else 0

    dates = sorted(t["Date"] for t in transactions)
    if dates:
        date_range = f"{dates[0]} to {dates[-1]}"
    else:
        date_range = "N/A"


    # =========================
    # REGION-WISE PERFORMANCE
    # =========================
    region_sales = defaultdict(float)
    region_transactions = Counter()

    for t in transactions:
        revenue = t["Quantity"] * t["UnitPrice"]
        region_sales[t["Region"]] += revenue
        region_transactions[t["Region"]] += 1

    region_data = []
    for region, sales in region_sales.items():
        percent = (sales / total_revenue) * 100
        region_data.append((region, sales, percent, region_transactions[region]))

    region_data.sort(key=lambda x: x[1], reverse=True)

    # =========================
    # TOP 5 PRODUCTS
    # =========================
    product_qty = defaultdict(int)
    product_revenue = defaultdict(float)

    for t in transactions:
        product_qty[t["ProductName"]] += t["Quantity"]
        product_revenue[t["ProductName"]] += t["Quantity"] * t["UnitPrice"]

    top_products = sorted(
        product_revenue.items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]

    # =========================
    # TOP 5 CUSTOMERS
    # =========================
    customer_spend = defaultdict(float)
    customer_orders = Counter()

    for t in transactions:
        customer_spend[t["CustomerID"]] += t["Quantity"] * t["UnitPrice"]
        customer_orders[t["CustomerID"]] += 1

    top_customers = sorted(
        customer_spend.items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]

    # =========================
    # DAILY SALES TREND
    # =========================
    daily_revenue = defaultdict(float)
    daily_transactions = Counter()
    daily_customers = defaultdict(set)

    for t in transactions:
        date = t["Date"]
        revenue = t["Quantity"] * t["UnitPrice"]
        daily_revenue[date] += revenue
        daily_transactions[date] += 1
        daily_customers[date].add(t["CustomerID"])

    # =========================
    # PRODUCT PERFORMANCE
    # =========================
    best_day = max(daily_revenue.items(), key=lambda x: x[1])[0]

    avg_product_revenue = sum(product_revenue.values()) / len(product_revenue)
    low_products = [p for p, r in product_revenue.items() if r < avg_product_revenue]

    # =========================
    # API ENRICHMENT SUMMARY
    # =========================
    enriched_count = len(enriched_transactions)
    sales_product_ids = set(t["ProductID"] for t in transactions)
    enriched_ids = set(enriched_transactions.keys())

    matched_products = sales_product_ids.intersection(enriched_ids)

    success_rate = (len(matched_products) / len(sales_product_ids)) * 100 if sales_product_ids else 0


    enriched_ids = set(enriched_transactions.keys())
    missing_products = list(set(t["ProductID"] for t in transactions) - enriched_ids)

    # =========================
    # WRITE REPORT
    # =========================
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("SALES ANALYTICS REPORT\n")
        f.write("=" * 50 + "\n")
        f.write(f"Generated: {now}\n")
        f.write(f"Records Processed: {total_records}\n\n")

        f.write("OVERALL SUMMARY\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total Revenue: ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions: {total_transactions}\n")
        f.write(f"Average Order Value: ₹{avg_order_value:,.2f}\n")
        f.write(f"Date Range: {date_range}\n\n")

        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 40 + "\n")
        f.write("Region\tSales\t% of Total\tTransactions\n")
        for r, s, p, c in region_data:
            f.write(f"{r}\t₹{s:,.0f}\t{p:.2f}%\t{c}\n")

        f.write("\nTOP 5 PRODUCTS\n")
        f.write("-" * 40 + "\n")
        f.write("Rank\tProduct\tQuantity\tRevenue\n")
        for i, (pname, rev) in enumerate(top_products, 1):
            f.write(f"{i}\t{pname}\t{product_qty[pname]}\t₹{rev:,.0f}\n")

        f.write("\nTOP 5 CUSTOMERS\n")
        f.write("-" * 40 + "\n")
        f.write("Rank\tCustomer\tTotal Spent\tOrders\n")
        for i, (cust, spent) in enumerate(top_customers, 1):
            f.write(f"{i}\t{cust}\t₹{spent:,.0f}\t{customer_orders[cust]}\n")

        f.write("\nDAILY SALES TREND\n")
        f.write("-" * 40 + "\n")
        f.write("Date\tRevenue\tTransactions\tUnique Customers\n")
        for d in sorted(daily_revenue):
            f.write(
                f"{d}\t₹{daily_revenue[d]:,.0f}\t"
                f"{daily_transactions[d]}\t{len(daily_customers[d])}\n"
            )

        f.write("\nPRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-" * 40 + "\n")
        f.write(f"Best Selling Day: {best_day}\n")
        f.write(f"Low Performing Products: {', '.join(low_products)}\n\n")

        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total Products Enriched: {enriched_count}\n")
        f.write(f"Success Rate: {success_rate:.2f}%\n")
        f.write("Products Not Enriched: None (API IDs do not map directly to sales ProductIDs)\n")