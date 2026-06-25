import pandas as pd
import ast
import json

def parse_to_native(val, default_factory=dict):
    if isinstance(val, (dict, list)):
        return val
    if isinstance(val, str):
        cleaned = val.strip()
        if not cleaned or cleaned.lower() == 'nan':
            return default_factory()
        try:
            res = ast.literal_eval(cleaned)
            return res if isinstance(res, (dict, list)) else default_factory()
        except:
            try:
                res = json.loads(cleaned)
                return res if isinstance(res, (dict, list)) else default_factory()
            except:
                return default_factory()
    try:
        if pd.isna(val):
            return default_factory()
    except:
        pass
    return default_factory()

def normalize_column(series, default_type):
    if series.dropna().empty:
        return series
    first_val = series.dropna().iloc[0]
    
    if isinstance(first_val, (dict, list)):
        return series.fillna(lambda: default_type())

    def fast_parse(val):
        if not isinstance(val, str):
            return default_type()
        cleaned = val.strip()
        if not cleaned or cleaned.lower() == 'nan':
            return default_type()
        try:
            return ast.literal_eval(cleaned)
        except:
            try:
                return json.loads(cleaned)
            except:
                return default_type()
                
    return series.apply(fast_parse)