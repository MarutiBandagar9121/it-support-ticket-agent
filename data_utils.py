import pandas as pd

def load_tickets(path:str):
    df = pd.read_csv(path, keep_default_na=False, na_values=[""])
    cat_cols = ["customer_segment", "channel", "product_area", "issue_type",
            "priority", "status", "sla_plan", "customer_sentiment", "platform", "region"]
    df[cat_cols] = df[cat_cols].astype("category")
    df["created_at"] = pd.to_datetime(df["created_at"])
    return df