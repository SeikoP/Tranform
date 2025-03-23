import pandas as pd

def analyze_dependencies(df):
    unique_counts = {col: df[col].nunique() for col in df.columns}
    dim_cols = [col for col, count in unique_counts.items() if count < len(df) * 0.1]
    fact_cols = [col for col in df.columns if col not in dim_cols]
    return {"Dim": dim_cols, "Fact": fact_cols}

def normalize_to_3nf(df, tables):
    if not tables:
        tables = {
            "Dim_Data": df.iloc[:, :2].drop_duplicates().columns.tolist(),
            "Fact_Data": df.columns.tolist()
        }
    normalized_tables = {table_name: df[columns] for table_name, columns in tables.items()}
    return normalized_tables