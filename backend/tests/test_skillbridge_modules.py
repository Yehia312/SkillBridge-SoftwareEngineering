import json
from pathlib import Path
from backend.services.job_matching import calculate_match, load_jobs, rank_jobs
from backend.services.learning_roadmap import generate_roadmap
from backend.services.progress_tracker import calculate_progress, complete_task


def test_jobs_dataset_structure():
    jobs_path = Path(__file__).resolve().parent.parent / "data" / "jobs.json"
    with jobs_path.open(encoding="utf-8-sig") as f:
        jobs = json.load(f)
    assert len(jobs) >= 8
    for job in jobs:
        assert "id" in job
        assert "title" in job
        assert "company" in job
        assert isinstance(job.get("required_skills"), list)


def test_job_matching_functions():
    jobs = [
        {"id": 1, "title": "Backend Intern", "company": "Partner", "required_skills": ["Python", "SQL", "Git"]},
        {"id": 2, "title": "Frontend Intern", "company": "Partner", "required_skills": ["React", "CSS"]},
    ]
    assert isinstance(calculate_match(["Python", "SQL"], jobs[0]["required_skills"]), dict)
    ranked = rank_jobs(["Python", "SQL"], jobs)
    assert len(ranked) == 2
    assert ranked[0]["title"] == "Backend Intern"


def test_roadmap_and_progress_functions():
    roadmap = generate_roadmap(["SQL", "Docker"], {"SQL": ["SQL Basics"], "Docker": ["Docker Intro"]})
    assert isinstance(roadmap, (list, dict))
    tasks = [
        {"id": 1, "skill": "SQL", "type": "task", "completed": False},
        {"id": 2, "skill": "Docker", "type": "task", "completed": False},
    ]
    assert complete_task(tasks, 1) is True
    progress = calculate_progress(tasks)
    assert progress["total_tasks"] == 2
    assert progress["completed_tasks_count"] == 1