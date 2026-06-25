import pandas as pd

def evaluate_stage1_retrieval(profile, history, signals, skills_text):
    # Hard Disqualifier Gates
    if signals.get('notice_period_days', 0) > 90: 
        return 0, False
    if signals.get('interview_completion_rate', 1.0) < 0.50: 
        return 0, False
    if signals.get('recruiter_response_rate', 1.0) < 0.10: 
        return 0, False

    # Relocation Validation Gateway
    candidate_loc = str(profile.get('location', '')).lower()
    target_cities = {'pune', 'noida', 'mumbai', 'hyderabad', 'delhi', 'ncr', 'gurgaon'}
    is_in_target_area = any(city in candidate_loc for city in target_cities)
    if not is_in_target_area and not signals.get('willing_to_relocate', True): 
        return 0, False

    # Consulting/Outsourcing Exclusion Filter
    consulting_blacklist = {'tcs', 'tata consultancy', 'infosys', 'wipro', 'accenture', 'cognizant', 'capgemini'}
    companies = [str(j.get('company', '')).lower() for j in history if isinstance(j, dict) and j.get('company')]
    if companies and all(any(black in comp for black in consulting_blacklist) for comp in companies): 
        return 0, False

    # Base Stage 1 Score Math
    early_score = 0
    if is_in_target_area: 
        early_score += 20
    early_score += (signals.get('recruiter_response_rate', 0) * 15)
    if signals.get('verified_email', False) or signals.get('verified_phone', False): 
        early_score += 5
    
    if companies and not any(any(black in comp for black in consulting_blacklist) for comp in companies):
        early_score += 20
    else:
        early_score += 10
    
    # Framework Wrappers vs Base IR Filter
    ir_keywords = {'embedding', 'retrieval', 'ranking', 'vector', 'search', 'nlp', 'llm', 'ndcg', 'mrr', 'peft'}
    has_framework_only = ('langchain' in skills_text or 'openai' in skills_text) and not any(kw in skills_text for kw in ir_keywords)
    early_score += 40 if not has_framework_only else 10

    return early_score, True