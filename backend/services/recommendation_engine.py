from backend.services.job_matching import rank_jobs

def recommend_jobs(user_skills, min_score=0.0, top_n=5, jobs=None):
    return [j for j in rank_jobs(user_skills, jobs=jobs) if j["matching_score"] >= min_score][:top_n]
