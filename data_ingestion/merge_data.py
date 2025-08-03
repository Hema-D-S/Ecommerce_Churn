import pandas as pd

def merge_sales_and_products(sales_df: pd.DataFrame, products_df: pd.DataFrame):
    """
    Merges sales and product datasets on 'product_id'.
    """
    merged_df = pd.merge(sales_df, products_df, on="product_id", how="left")
    return merged_df

if __name__ == "__main__":
    sales = pd.read_csv("C:\Users\user\Ecommerce_Churn\data\Sales.csv")
    products = pd.read_csv("C:\Users\user\Ecommerce_Churn\data\products.csv")
    merged = merge_sales_and_products(sales, products)
    print(f"Merged DataFrame shape: {merged.shape}")
