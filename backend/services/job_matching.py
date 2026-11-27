import json
from pathlib import Path

def load_jobs(file_path="backend/data/jobs.json"):
    return json.loads(Path(file_path).read_text(encoding="utf-8-sig"))

def calculate_match(user_skills, job_skills):
    if not job_skills: return {"matching_score": 0.0, "matched_skills": [], "missing_skills": []}
    u = {s.strip().lower(): s.strip() for s in user_skills if s and s.strip()}
    j = {s.strip().lower(): s.strip() for s in job_skills if s and s.strip()}
    m = [j[k] for k in set(u) & set(j)]
    miss = [j[k] for k in set(j) - set(u)]
    return {"matching_score": round(len(m)/len(j)*100, 2), "matched_skills": m, "missing_skills": miss}

def rank_jobs(user_skills, jobs=None):
    data = jobs if jobs is not None else load_jobs()
    out = [{"job_id": g.get("id"), "title": g.get("title"), "company": g.get("company", ""), **calculate_match(user_skills, g.get("required_skills", []))} for g in data]
    return sorted(out, key=lambda x: x["matching_score"], reverse=True)
