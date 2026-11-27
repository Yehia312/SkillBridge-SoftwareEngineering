from fastapi import FastAPI
from pydantic import BaseModel
from backend.services.recommendation_engine import recommend_jobs
from backend.services.learning_roadmap import generate_roadmap
from backend.services.progress_tracker import calculate_progress, complete_task

app = FastAPI(title="SkillBridge API")


class SkillRequest(BaseModel):
    skills: list[str]
    min_score: float = 0.0
    top_n: int = 5


class RoadmapRequest(BaseModel):
    missing_skills: list[str]


class ProgressRequest(BaseModel):
    tasks: list[dict]
    completed_skills: list[str] | None = None


class CompleteTaskRequest(BaseModel):
    tasks: list[dict]
    task_id: int | str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/recommendations")
def recommendations(req: SkillRequest):
    return {"recommendations": recommend_jobs(req.skills, min_score=req.min_score, top_n=req.top_n)}


@app.post("/roadmap")
def roadmap(req: RoadmapRequest):
    return generate_roadmap(req.missing_skills)


@app.post("/progress")
def progress(req: ProgressRequest):
    return calculate_progress(req.tasks, completed_skills=req.completed_skills)


@app.post("/progress/complete")
def progress_complete(req: CompleteTaskRequest):
    updated = complete_task(req.tasks, req.task_id)
    progress_summary = calculate_progress(req.tasks)
    return {"updated": updated, "progress": progress_summary, "tasks": req.tasks}
