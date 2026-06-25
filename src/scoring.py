from src.stage1_retrieval import evaluate_stage1_retrieval
from src.stage2_reranker import compute_reranker_score

def calculate_optimized_master_score(row):
    profile = row['profile']
    history = row['career_history']
    skills_list = row['skills']
    signals = row['redrob_signals']
    
    # Pre-extract text representations
    skills_text = " ".join([str(s.get('name', '')).lower() for s in skills_list if isinstance(s, dict)])
    history_text = " ".join([str(j.get('title', '')) + " " + str(j.get('description', '')) for j in history if isinstance(j, dict)]).lower()
    full_text = skills_text + " " + history_text

    # Run Stage 1 Gate
    early_score, passed_gate = evaluate_stage1_retrieval(profile, history, signals, skills_text)
    if not passed_gate:
        return 0

    # Run Stage 2 Reranker
    final_weighted_score = compute_reranker_score(
        profile, history, signals, full_text, history_text, early_score
    )
    
    return final_weighted_score