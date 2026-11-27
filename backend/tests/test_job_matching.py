import sys, unittest
sys.path.insert(0, ".")
from backend.services.job_matching import calculate_match, rank_jobs
from backend.services.recommendation_engine import recommend_jobs

class TestJobMatching(unittest.TestCase):
    def test_all(self):
        self.assertEqual(calculate_match(["python", "SQL"], ["Python", "SQL"])["matching_score"], 100.0)
        self.assertEqual(rank_jobs(["Python", "SQL", "Git"])[0]["title"], "Data Analyst Intern")
        self.assertEqual(len(recommend_jobs(["Python", "SQL", "Git"], min_score=50.0, top_n=2)), 2)

if __name__ == "__main__":
    unittest.main()
