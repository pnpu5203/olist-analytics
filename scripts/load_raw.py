import os
import sys
import csv
from google.cloud import bigquery
from pathlib import Path
from dotenv import load_dotenv

# import the EXPECTED_FILES list directly from the download_data.py script for reuse.
from download_data import EXPECTED_FILES

DATASET_ID = "raw"
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"

def get_bigquery_client() -> tuple[bigquery.Client, str]:
    """
    Read environment variables and initialize BigQuery Client.
    """

    # export environment variables "GCP_PROJECT_ID" and "GOOGLE_APPLICATION_CREDENTIALS" from .env file
    load_dotenv()

    required_vars = ["GCP_PROJECT_ID", "GOOGLE_APPLICATION_CREDENTIALS"]
    missing_env = [var for var in required_vars if not os.environ.get(var)]
    if missing_env:
        print(f"Error: Missing environment variable {', '.join(missing_env)}. Please configure the .env file or refer to .env.example.", file=sys.stderr)
        sys.exit(1)

    # initialize BigQuery client
    # get the Project ID from environment variable "GCP_PROJECT_ID"
    project_id = os.environ.get("GCP_PROJECT_ID")
    client = bigquery.Client(project=project_id)

    return client, project_id

def ensure_dataset(client: bigquery.Client, dataset_ref: str) -> None:
    """
    Create a `raw` dataset in BigQuery if it doesn't already exist.
    """

    # create the raw dataset if not exist
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = "US" # select the configured location
    client.create_dataset(dataset, exists_ok=True)

def read_header(file_path: Path) -> list[str]:
    """
    Read the header of the CSV file and return a list of column names.
    """

    with open(file_path, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader) # use the first row as the column name

    return header

def load_csv(client: bigquery.Client, file_path: Path, dataset_ref: str) -> int:
    """
    Load a CSV file into BigQuery, configure it to cast all STRING types,
    and return the actual number of rows.
    """

    table_name = file_path.stem
    table_id = f"{dataset_ref}.{table_name}"

    print(f"Processing table: {table_name} ...")

    # 1. read the CSV file and extract the header (columns)
    columns = read_header(file_path)
    
    # 2. automatically generate the STRING schema
    string_schema = [
        bigquery.SchemaField(
            name=col,
            field_type=bigquery.SqlTypeNames.STRING
        ) for col in columns
    ]

    ## configure job load data: All columns are STRING to preserve the raw data
    job_config = bigquery.LoadJobConfig(
        schema=string_schema,
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1, # ignore the header
        allow_quoted_newlines=True,
        # WRITE_TRUNCATE (overwrite the entire raw table)
        # the mechanism allows for repeated code execution without data duplication
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )

    # 3. proceed to upload the file to BigQuery
    with open(file_path, "rb") as source_file:
        load_job = client.load_table_from_file(
            source_file,
            table_id,
            job_config=job_config
        )

    # waiting for the load job to be completed
    try:
        load_job.result()
    except Exception as e:
        print(f"\n[ERROR] Data loading failed for table: {table_name}", file=sys.stderr)
        print(f"System details: {e}", file=sys.stderr)
        
        # if BigQuery returns a detailed list of errors (row number, column number)
        if load_job.errors:
            print("\n--- Details of the BigQuery Job Errors ---", file=sys.stderr)
            for error in load_job.errors:
                print(error, file=sys.stderr)
                
        # stop the entire program immediately with an error code other than 0 (Fail Fast)
        sys.exit(1)

    # 4. get the number of lines that have been successfully loaded
    num_rows = load_job.output_rows
    print(f"Successfully loaded {table_name} table: {num_rows} rows.")

    return num_rows

def main():
    """
    Main scheduler function:
    1. Initializes & validates the dataset
    2. Iterates through the files
    3. Summarizes
    """

    if not RAW_DIR.exists():
        print(f"[ERROR] Data folder not found: {RAW_DIR}", file=sys.stderr)
        print("Please run the following command to download the data first: `python scripts/download_data.py`", file=sys.stderr)
        sys.exit(1)

    csv_files = list(sorted(RAW_DIR.glob("*.csv")))

    if not csv_files:
        print(f"[ERROR] No CSV files were found in the folder: {RAW_DIR}.", file=sys.stderr)
        print("Please run the following command to download the data first: `python scripts/download_data.py`", file=sys.stderr)
        sys.exit(1)

    # Check the integrity of the number of files
    if EXPECTED_FILES:
        found_file_names = {f.name for f in csv_files}
        missing_files = [f for f in EXPECTED_FILES if f not in found_file_names]
        if missing_files:
            print(f"[ERROR] Missing required data files: {missing_files}", file=sys.stderr)
            print("Please run the following command: `python scripts/download_data.py` to download the complete dataset..", file=sys.stderr)
            sys.exit(1)

    # 1. Initialize client and prepare dataset
    client, project_id = get_bigquery_client()
    dataset_ref = f"{project_id}.{DATASET_ID}"
    ensure_dataset(client, dataset_ref)

    # 2. Iterates through the files
    summary_results = {}

    for file_path in csv_files:
        table_name = file_path.stem
        rows_loaded = load_csv(client, file_path, dataset_ref)
        summary_results[table_name] = rows_loaded

    # print the final summary table
    print(f"{len(summary_results)}/{len(EXPECTED_FILES)} tables loaded")
    print("\n" + "=" * 40)
    print(" LOAD SUMMARY ")
    print("=" * 40)
    for tbl, count in summary_results.items():
        print(f"Table '{tbl}': {count} rows")
    print("=" * 40)


if __name__ == "__main__":
    main()