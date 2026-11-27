def calculate_progress(tasks, completed_skills=None):
    total_tasks = len(tasks) if tasks else 0
    completed_tasks = [t for t in (tasks or []) if t.get("completed")]
    completed_tasks_count = len(completed_tasks)
    progress_percentage = round((completed_tasks_count / total_tasks) * 100, 2) if total_tasks else 0.0
    completed_projects_count = sum(
        1 for t in completed_tasks if t.get("type") in ("project", "mini-project")
    )
    if completed_skills is not None:
        completed_skills_count = len(set(completed_skills))
    else:
        completed_skills_count = len(
            {t.get("skill") for t in completed_tasks if t.get("skill")}
        )
    return {
        "completed_skills_count": completed_skills_count,
        "completed_tasks_count": completed_tasks_count,
        "total_tasks": total_tasks,
        "progress_percentage": progress_percentage,
        "completed_projects_count": completed_projects_count,
    }


def complete_task(tasks, task_id):
    for t in tasks or []:
        if t.get("id") == task_id:
            t["completed"] = True
            return True
    return False
