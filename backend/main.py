from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, field_validator
import json

from backend.database import (
    create_table,
    insert_candidate,
    get_all_candidates,
    update_candidate,
    delete_candidate
)
from backend.services.recommendation_engine import recommend_jobs
from backend.services.learning_roadmap import generate_roadmap
from backend.services.progress_tracker import calculate_progress, complete_task

app = FastAPI(title="SkillBridge API")

create_table()

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
class Candidate(BaseModel):
    name: str
    email: EmailStr
    skills: list[str]

    @field_validator("name")
    @classmethod
    def clean_name(cls, value):
        return value.strip()

    @field_validator("email")
    @classmethod
    def clean_email(cls, value):
        return str(value).strip().lower()

    @field_validator("skills")
    @classmethod
    def clean_skills(cls, value):
        cleaned_skills = []
        seen_skills = set()

        for skill in value:
            skill = skill.strip()

            if skill and skill.lower() not in seen_skills:
                cleaned_skills.append(skill)
                seen_skills.add(skill.lower())

        return cleaned_skills

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

@app.post("/candidates")
def create_candidate(candidate: Candidate):

    try:
        insert_candidate(
            candidate.name,
            str(candidate.email),
            json.dumps(candidate.skills)
        )

    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error)
        )

    return {
        "message": "Candidate added successfully!"
    }
@app.get("/candidates")
def get_candidates():
    return get_all_candidates()
@app.put("/candidates/{candidate_id}")
def update_candidate_api(candidate_id: int, candidate: Candidate):

    try:
        updated = update_candidate(
            candidate_id,
            candidate.name,
            str(candidate.email),
            json.dumps(candidate.skills)
        )

    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error)
        )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found!"
        )

    return {
        "message": "Candidate updated successfully!"
    }
@app.delete("/candidates/{candidate_id}")
def delete_candidate_api(candidate_id: int):

    deleted = delete_candidate(candidate_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found!"
        )

    return {
        "message": "Candidate deleted successfully!"
    }