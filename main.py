import logging
import pandas as pd
import typer


def main(
    transactions_path: str,
    crsids_path: str,
    search_str: str,
    search_column_name: str = "Narrative #2",
):
    logging.basicConfig(level=logging.INFO)
    logging.info("EBC Payments")

    # Load transactions
    df_transactions = pd.read_csv(transactions_path)
    logging.info(f"Read {len(df_transactions)} transactions")

    # Load CRSIDs list
    with open(crsids_path) as f:
        crsids = [i.strip().upper() for i in f.read().split("\n") if i.strip()]

    logging.info(f"Read {len(crsids)} crsids")

    logging.info(f"Using search string '{search_str}'")
    logging.info(f"Searching in column '{search_column_name}'")

    # Filter transactions that contain the search string
    df_transactions = df_transactions[
        df_transactions[search_column_name]
        .str.upper()
        .str.contains(search_str.upper(), na=False)
    ]

    logging.info(f"Found {len(df_transactions)} matching transactions")

    # Extract paid CRSIDs
    paid_crsids = {
        ref.split()[0].upper()
        for ref in df_transactions[search_column_name].dropna().tolist()
    }

    claimed = set(crsids)

    missing = claimed - paid_crsids
    unexpected = paid_crsids - claimed

    logging.info("Summary:")
    logging.info(f"Paid CRSIDs: {sorted(paid_crsids)}")
    logging.info(f"Missing (claimed but not paid): {sorted(missing)}")
    logging.info(f"Unexpected (paid but not claimed): {sorted(unexpected)}")

    print("\n=== PAYMENT CHECK RESULTS ===")
    print(f"Total claimed:   {len(claimed)}")
    print(f"Total paid:      {len(paid_crsids)}")
    print(f"Missing:         {len(missing)}")
    print(f"Unexpected:      {len(unexpected)}\n")

    if missing:
        print("❌ Missing payments:")
        for crsid in sorted(missing):
            print(f"  - {crsid}")

    if unexpected:
        print("\n⚠️  Unexpected payments:")
        for crsid in sorted(unexpected):
            print(f"  - {crsid}")


if __name__ == "__main__":
    typer.run(main)