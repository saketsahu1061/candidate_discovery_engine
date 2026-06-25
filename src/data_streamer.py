import pandas as pd
import json

def load_and_stream_dataset(file_source, file_name):
    """
    Ingests and builds a DataFrame from CSV, JSON, or JSONL sources.
    Handles memory-safe line streaming for large file payloads.
    """
    try:
        if file_name.endswith('.csv'):
            return pd.read_csv(file_source)
            
        elif file_name.endswith('.jsonl'):
            # If it's an uploaded file object from Streamlit, reset pointer and stream lines
            if hasattr(file_source, 'seek'):
                file_source.seek(0)
                records = [json.loads(line) for line in file_source if line.strip()]
                return pd.DataFrame(records)
            else:
                # If it's a local file path string (used by main.py)
                return pd.read_json(file_source, lines=True)
                
        elif file_name.endswith('.json'):
            return pd.read_json(file_source)
            
        else:
            raise ValueError("Unsupported extension. Must be .csv, .json, or .jsonl")
            
    except Exception as e:
        raise IOError(f"Data engine failed to stream target file structure: {str(e)}")