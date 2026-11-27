from backend.services.progress_tracker import calculate_progress, complete_task


def test_calculate_progress_partial():
    tasks = [
        {"id": i, "skill": "Docker", "type": "task", "completed": i <= 4}
        for i in range(1, 11)
    ]
    result = calculate_progress(tasks)
    assert result["total_tasks"] == 10
    assert result["completed_tasks_count"] == 4
    assert result["progress_percentage"] == 40.0


def test_complete_task_and_projects():
    tasks = [
        {"id": 1, "skill": "Docker", "type": "task", "completed": False},
        {"id": 2, "skill": "Docker", "type": "project", "completed": False},
    ]
    assert complete_task(tasks, 1) is True
    assert complete_task(tasks, 2) is True
    assert complete_task(tasks, 99) is False
    result = calculate_progress(tasks, completed_skills=["Docker"])
    assert result["completed_skills_count"] == 1
    assert result["completed_projects_count"] == 1
    assert result["progress_percentage"] == 100.0


def test_empty_tasks():
    result = calculate_progress([])
    assert result["total_tasks"] == 0
    assert result["progress_percentage"] == 0.0
