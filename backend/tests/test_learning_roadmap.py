import sys, unittest
sys.path.insert(0, ".")
from backend.services.learning_roadmap import generate_roadmap

class TestLearningRoadmap(unittest.TestCase):
    def test_roadmap(self):
        out = generate_roadmap(["sql", "Docker", "SQL"])
        self.assertEqual(out["total_steps"], 2)
        self.assertEqual(out["roadmap"][0]["skill"], "SQL")
        self.assertEqual(out["roadmap"][1]["skill"], "Docker")

if __name__ == "__main__":
    unittest.main()
