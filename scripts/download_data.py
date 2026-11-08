import sys
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv() # reading KAGGLE_USERNAME and KAGGLE_KEY from the .env file

DATASET_NAME = "olistbr/brazilian-ecommerce"  # Dataset Olist on Kaggle

# generating the absolute path from Path(__file__)
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"

# declare the exact list of 9 core Olist CSV files.
EXPECTED_FILES = {
    "olist_customers_dataset.csv",
    "olist_geolocation_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_orders_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "product_category_name_translation.csv"
}

def download_kaggle_dataset(dataset_name=DATASET_NAME):
    # create folder data/raw/ if not existed
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    # Idempotent check: using set subtraction
    existing_files = {f.name for f in RAW_DIR.iterdir() if f.is_file()}
    missing_files = EXPECTED_FILES - existing_files
    if not missing_files:
        print(f"The '{RAW_DIR}' folder already contains all 9 required CSV files. Skip the download step!")
        return

    # check Kaggle credentials in os.environ before importing and authenticating.
    required_vars = ["KAGGLE_USERNAME", "KAGGLE_KEY"]
    missing_env = [var for var in required_vars if not os.environ.get(var)]
    if missing_env:
        print(f"Error: Missing environment variable {', '.join(missing_env)}. Please configure the .env file or refer to .env.example.", file=sys.stderr)
        sys.exit(1)

    print("Establishing Kaggle API connection ...")
    try:
        # Lazy Import:
        from kaggle.api.kaggle_api_extended import KaggleApi
        api = KaggleApi()
        api.authenticate()
    except Exception as e:
        print(f"Kaggle API validation error: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Loading dataset '{dataset_name}' from Kaggle to '{RAW_DIR}' ...")
    try:
        api.dataset_download_files(dataset_name, path=str(RAW_DIR), unzip=True)
    except Exception as e:
        print(f"Error loading dataset from Kaggle: {e}", file=sys.stderr)
        sys.exit(1)

    # verify the files after downloading.
    print("Comparing and verifying the integrity of the files after downloading... ...")
    existing_files_after = {f.name for f in RAW_DIR.iterdir() if f.is_file()}
    missing_files_after = EXPECTED_FILES - existing_files_after
    
    if missing_files_after:
        print(f"Error: The following files were missing during the download or extraction process: {list(missing_files_after)}")
        sys.exit(1)  # exit the program with an error code
    
    print(f"Data has been successfully downloaded and extracted to '{RAW_DIR}'!")

if __name__ == "__main__":
    download_kaggle_dataset()