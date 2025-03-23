import pandas as pd
import uuid

def normalize_to_3nf(df: pd.DataFrame, erd: dict):
    if df is None or df.empty:
        raise ValueError("DataFrame đầu vào trống hoặc không hợp lệ!")
    if not erd or not isinstance(erd, dict):
        raise ValueError("Cấu trúc ERD không hợp lệ!")

    normalized_tables = {}
    
    # Xử lý bảng Dim
    for table_name, columns in erd.items():
        if table_name.lower().startswith('dim_'):
            selected_columns = [col['name'] for col in columns if col['name'] in df.columns]
            if not selected_columns:
                continue
            
            table_df = df[selected_columns].copy().dropna(subset=selected_columns)
            primary_key_cols = [col['name'] for col in columns if col.get('is_primary', False)]
            
            if primary_key_cols:
                table_df = table_df.drop_duplicates(subset=primary_key_cols).reset_index(drop=True)
                if not any(col.endswith('_id') for col in primary_key_cols):
                    table_df.insert(0, f'{table_name}_id', [uuid.uuid4().hex for _ in range(len(table_df))])
            
            normalized_tables[table_name] = table_df
    
    # Xử lý bảng Fact
    for table_name, columns in erd.items():
        if table_name.lower().startswith('fact_'):
            fact_columns = [col['name'] for col in columns if col['name'] in df.columns]
            if not fact_columns:
                continue
            
            fact_df = df[fact_columns].copy().dropna(subset=fact_columns)
            
            for col in columns:
                col_name = col['name']
                ref_table = col.get('ref_table')
                ref_column = col.get('ref_column')
                
                if ref_table and ref_table in normalized_tables:
                    dim_df = normalized_tables[ref_table]
                    dim_pk_cols = [c['name'] for c in erd[ref_table] if c.get('is_primary', False)]
                    dim_pk_col = dim_pk_cols[0] if dim_pk_cols else None
                    
                    if ref_column and col_name in fact_df.columns and dim_pk_col and ref_column in dim_df.columns:
                        if dim_df[ref_column].duplicated().any():
                            raise ValueError(f"Cột tham chiếu {ref_column} trong {ref_table} không duy nhất!")
                        mapping = dict(zip(dim_df[ref_column], dim_df[dim_pk_col]))
                        fact_df[col_name] = fact_df[col_name].map(mapping).fillna(fact_df[col_name])
                        fact_df = fact_df.rename(columns={col_name: f'{col_name}_id'})
                    elif ref_column not in dim_df.columns:
                        raise ValueError(f"Cột tham chiếu {ref_column} không tồn tại trong {ref_table}!")
            
            normalized_tables[table_name] = fact_df
    
    return normalized_tables