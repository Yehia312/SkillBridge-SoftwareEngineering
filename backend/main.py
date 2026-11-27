from fastapi import FastAPI
from pydantic import BaseModel
from backend.services.recommendation_engine import recommend_jobs
from backend.services.learning_roadmap import generate_roadmap

app = FastAPI(title="SkillBridge API")

class SkillRequest(BaseModel):
    skills: list[str]
    min_score: float = 0.0
    top_n: int = 5

class RoadmapRequest(BaseModel):
    missing_skills: list[str]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/recommendations")
def recommendations(req: SkillRequest):
    return {"recommendations": recommend_jobs(req.skills, min_score=req.min_score, top_n=req.top_n)}

@app.post("/roadmap")
def roadmap(req: RoadmapRequest):
    return generate_roadmap(req.missing_skills)
