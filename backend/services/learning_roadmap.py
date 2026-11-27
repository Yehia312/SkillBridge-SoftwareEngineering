import json
from pathlib import Path

def load_resources(file_path="backend/data/learning_resources.json"):
    return json.loads(Path(file_path).read_text(encoding="utf-8-sig"))

def generate_roadmap(missing_skills, resources=None):
    catalog = resources if resources is not None else load_resources()
    norm_map = {k.strip().lower(): (k.strip(), v) for k, v in catalog.items()}
    steps = []
    seen = set()
    for idx, skill in enumerate(missing_skills, start=1):
        key = skill.strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        canonical_name, res_list = norm_map.get(key, (skill.strip(), [f"Search official docs & practice for {skill.strip()}"]))
        steps.append({"step": len(steps) + 1, "skill": canonical_name, "resources": res_list})
    return {"total_steps": len(steps), "roadmap": steps}
