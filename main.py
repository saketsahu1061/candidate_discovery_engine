import argparse
import pandas as pd
from src.data_streamer import load_and_stream_dataset
from src.utils import normalize_column
from src.scoring import calculate_optimized_master_score
from src.stage3_schema import generate_submission_schema

def run_pipeline(input_path, target_count=100, output_path="final_submission.csv"):
    print(f"Streaming data stream directly from source: {input_path}")
    df_raw = load_and_stream_dataset(input_path, input_path)

    print("Executing vectorized type normalization pass...")
    df_raw['profile'] = normalize_column(df_raw['profile'], dict)
    df_raw['career_history'] = normalize_column(df_raw['career_history'], list)
    df_raw['skills'] = normalize_column(df_raw['skills'], list)
    df_raw['redrob_signals'] = normalize_column(df_raw['redrob_signals'], dict)

    print("Evaluating progressive heuristic filter matrices...")
    df_raw['final_weighted_score'] = df_raw.apply(calculate_optimized_master_score, axis=1)
    df_filtered = df_raw[df_raw['final_weighted_score'] > 0].copy()

    if df_filtered.empty:
        print("All candidate profiles dropped behind behavioral/logistical gateways.")
        return

    df_top = df_filtered.nlargest(target_count, 'final_weighted_score').copy()
    df_top = df_top.sort_values(by='final_weighted_score', ascending=False).reset_index(drop=True)

    print("Synthesizing final submission metadata schemas...")
    df_submission = generate_submission_schema(df_top)
    
    df_submission.to_csv(output_path, index=False)
    print(f"Pipeline completely processed. Saved output to target: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Modular Local Headless Talent Pipeline")
    parser.add_argument("--input", type=str, required=True, help="Input data file path location")
    parser.add_argument("--count", type=int, default=100, help="Total candidate selection size limit")
    parser.add_argument("--output", type=str, default="final_submission.csv", help="Output file print directory target")
    
    args = parser.parse_args()
    run_pipeline(args.input, args.count, args.output)