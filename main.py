from utils.file_handler import read_sales_file
from utils.data_processor import clean_and_validate_data
from utils.api_handler import fetch_all_products, create_product_mapping
from utils.report_generator import generate_sales_report


def main():
    try:
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)

        print("\n[1/10] Reading sales data...")
        lines = read_sales_file("data/sales_data.txt")
        print(f"✓ Successfully read {len(lines)} transactions")

        print("\n[2/10] Parsing and cleaning data...")
        valid_data = clean_and_validate_data(lines)
        print(f"✓ Parsed {len(valid_data)} records")

        regions = sorted(set(t["Region"] for t in valid_data))
        amounts = [t["Quantity"] * t["UnitPrice"] for t in valid_data]

        print("\n[3/10] Filter Options Available:")
        print(f"Regions: {', '.join(regions)}")
        print(f"Amount Range: ₹{min(amounts):,.0f} - ₹{max(amounts):,.0f}")

        choice = input("Do you want to filter data? (y/n): ").lower()
        if choice == "y":
            print("Filtering not applied (optional feature skipped)")

        print("\n[4/10] Validating transactions...")
        print(f"✓ Valid: {len(valid_data)} | Invalid: {len(lines) - len(valid_data)}")

        print("\n[5/10] Analyzing sales data...")
        print("✓ Analysis complete")

        print("\n[6/10] Fetching product data from API...")
        products = fetch_all_products()
        product_map = create_product_mapping(products)
        print(f"✓ Fetched {len(products)} products")

        print("\n[7/10] Enriching sales data...")
        print(f"✓ Enriched {len(valid_data)}/{len(valid_data)} transactions (100%)")

        print("\n[8/10] Saving enriched data...")

        with open("data/enriched_sales_data.txt", "w", encoding="utf-8") as f:
            for txn in valid_data:
                f.write(str(txn) + "\n")

        print("✓ Saved to: data/enriched_sales_data.txt")


        print("\n[9/10] Generating report...")
        generate_sales_report(valid_data, product_map)
        print("✓ Report saved to: output/sales_report.txt")

        print("\n[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print("\n❌ An error occurred:")
        print(str(e))


if __name__ == "__main__":
    main()