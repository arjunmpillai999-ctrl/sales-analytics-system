def fetch_product_info(product_id):
    return {
        "product_id": product_id,
        "category": "Electronics"
    }

import requests

def fetch_all_products():
    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        print("✅ Successfully fetched products from API")
        return data.get("products", [])

    except Exception as e:
        print("❌ Failed to fetch products from API")
        print("Error:", e)
        return []

def create_product_mapping(api_products):
    product_mapping = {}

    for product in api_products:
        product_mapping[product.get("id")] = {
            "title": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand"),
            "rating": product.get("rating"),
        }

    return product_mapping