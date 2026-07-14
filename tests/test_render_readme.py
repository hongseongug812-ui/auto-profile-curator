import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
from render_readme import infer_activities


def repo(**overrides):
    base = {"name": "demo", "description": "", "is_fork": False, "is_archived": False, "last_commit_at": "2026-03-15T00:00:00Z", "primary_language": {"name": "Python"}}
    return base | overrides


class InferActivitiesTests(unittest.TestCase):
    def test_excludes_the_profile_repository_itself(self):
        activities = infer_activities([repo(name="octocat"), repo(name="real-project")], username="octocat")
        titles = [item["title"] for group in activities for item in group["items"]]
        self.assertEqual(titles, ["real-project"])

    def test_excludes_forks_and_archived(self):
        activities = infer_activities([repo(name="a", is_fork=True), repo(name="b", is_archived=True), repo(name="c")])
        titles = [item["title"] for group in activities for item in group["items"]]
        self.assertEqual(titles, ["c"])


if __name__ == "__main__":
    unittest.main()
