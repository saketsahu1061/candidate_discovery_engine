import pandas as pd

def generate_submission_schema(df_top):
    submission_rows = []
    
    for idx, row in df_top.iterrows():
        prof = row['profile']
        signals = row['redrob_signals']
        history = row['career_history']
        skills = row['skills']
        
        # Build flattened strings lazily only for top isolated records
        companies_list = [str(j.get('company', '')) for j in history if isinstance(j, dict) and j.get('company')]
        flat_companies = ", ".join(companies_list) if companies_list else "N/A"
        
        skills_list = [str(s.get('name', '')) for s in skills if isinstance(s, dict) and s.get('name')]
        top_skills = ", ".join(skills_list[:3]) if skills_list else "AI Systems Engineering"
        
        # Build strict evaluation summary string pattern
        reasoning = (
            f"{prof.get('current_title', 'AI Engineer')} with {prof.get('years_of_experience', 0.0):.1f} yrs exp; "
            f"companies: {flat_companies}; "
            f"core infrastructure: {top_skills}; "
            f"response rate: {signals.get('recruiter_response_rate', 0.0):.2f}."
        )
        
        submission_rows.append({
            'candidate_id': row.get('candidate_id'),
            'rank': idx + 1,
            'score': round(row['final_weighted_score'] / 100.0, 4),
            'reasoning': reasoning
        })
        
    return pd.DataFrame(submission_rows)