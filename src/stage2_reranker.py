def compute_reranker_score(profile, history, signals, full_text, history_text, early_score):
    # Pillar 1: Infrastructure Competency (40% Weight Base)
    core_production_score = 0
    if any(m in full_text for m in {'sentence-transformers', 'openai embeddings', 'bge', 'e5'}): 
        core_production_score += 10
    if any(i in full_text for i in {'embedding drift', 'index refresh', 'quality regression', 'retrieval-quality'}): 
        core_production_score += 15

    vector_infra = {'pinecone', 'weaviate', 'qdrant', 'milvus', 'opensearch', 'elasticsearch', 'faiss', 'hybrid search'}
    infra_matches = sum(1 for tech in vector_infra if tech in full_text)
    if infra_matches > 0: 
        core_production_score += min(10 + (infra_matches * 3), 25)

    eval_metrics = {'ndcg', 'mrr', 'map', 'offline-to-online', 'correlation', 'a/b test'}
    eval_matches = sum(1 for metric in eval_metrics if metric in full_text)
    if eval_matches > 0: 
        core_production_score += min(10 + (eval_matches * 5), 25)

    # Average Job Stability Evaluation
    total_years = profile.get('years_of_experience', 0)
    if len(history) > 1:
        avg_tenure = total_years / len(history)
        if avg_tenure >= 3.0: core_production_score += 25
        elif avg_tenure >= 1.8: core_production_score += 15
    else:
        core_production_score += 20

    if 'redux' in full_text or ('langchain' in full_text and eval_matches == 0):
        core_production_score = max(0, core_production_score - 20)

    # CV/Robotics Domain Safeguard Check
    cv_gen_keywords = {'opencv', 'cnn', 'computer vision', 'ros', 'robotics', 'object detection', 'diffusion models', 'gans'}
    core_search_infra = {'vector search', 'hybrid search', 'index refresh', 'embedding drift', 'weaviate', 'pinecone', 'qdrant', 'milvus', 'faiss', 'ndcg', 'mrr'}
    if any(k in full_text for k in cv_gen_keywords) and not any(k in full_text for k in core_search_infra):
        core_production_score = max(0, core_production_score - 25)

    # Pillar 2: Strategic Target Alignment (30% Weight Base)
    ideal_target_score = 0
    if 5 <= total_years <= 9: 
        ideal_target_score += 20
        
    consulting_blacklist = {'tcs', 'tata consultancy', 'infosys', 'wipro', 'accenture', 'cognizant', 'capgemini'}
    companies = [str(j.get('company', '')).lower() for j in history if isinstance(j, dict) and j.get('company')]
    if companies and not any(any(black in comp for black in consulting_blacklist) for comp in companies): 
        ideal_target_score += 15
        
    if any(kw in history_text for kw in {'ranking', 'ranker', 'search', 'recommendation', 'retrieval'}): 
        ideal_target_score += 25
        
    fluency_matches = sum(1 for kw in {'hybrid search', 'dense retrieval', 'offline evaluation', 'online evaluation', 'fine-tuning', 'prompting'} if kw in full_text)
    ideal_target_score += min(fluency_matches * 5, 20)
    
    candidate_loc = str(profile.get('location', '')).lower()
    if 'pune' in candidate_loc or 'noida' in candidate_loc: 
        ideal_target_score += 10
    if signals.get('open_to_work_flag', False): 
        ideal_target_score += 10

    # Pillar 3: Nice-to-Have Bonuses (20% Weight Base)
    nice_to_have_score = 0
    if any(kw in full_text for kw in {'lora', 'qlora', 'peft', 'fine-tuning', 'llm adaptation'}): 
        nice_to_have_score += 30
    if any(kw in full_text for kw in {'hr-tech', 'hr tech', 'marketplace', 'talent intelligence', 'ats'}): 
        nice_to_have_score += 20
    if any(kw in full_text for kw in {'distributed systems', 'large-scale inference', 'inference optimization', 'ray', 'spark', 'cuda'}): 
        nice_to_have_score += 30
    if 'open-source' in full_text or 'open source' in full_text or signals.get('github_activity_score', -1) > 30: 
        nice_to_have_score += 20

    # Composite Balanced Weight Matrix Summary
    return (core_production_score * 0.40) + (ideal_target_score * 0.30) + (nice_to_have_score * 0.20) + (early_score * 0.10)