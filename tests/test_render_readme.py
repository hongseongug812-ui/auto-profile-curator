import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
from render_readme import infer_activities, render_stack_items, stack_rows


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


class RenderStackItemsTests(unittest.TestCase):
    def test_known_items_get_an_icon_and_url(self):
        items = render_stack_items(["Python", "OpenAI"])
        self.assertEqual(items[0], {"name": "Python", "icon": "python", "url": "https://www.python.org/"})
        self.assertEqual(items[1], {"name": "OpenAI", "icon": None, "url": None})


class StackRowsTests(unittest.TestCase):
    def test_keeps_items_grouped_by_their_own_category(self):
        stacks = {"ai_cloud": ["AWS", "OpenAI"], "back_end": ["FastAPI", "Python"], "front_end": [], "database": ["PostgreSQL"]}
        rows = stack_rows(stacks, ["Docker"])
        self.assertEqual([item["name"] for item in rows["ai_cloud"]], ["AWS", "OpenAI"])
        self.assertEqual([item["name"] for item in rows["back_end"]], ["FastAPI", "Python"])
        self.assertEqual([item["name"] for item in rows["front_end"]], [])
        self.assertEqual([item["name"] for item in rows["development_tools"]], ["Docker"])

    def test_every_item_appears_even_without_a_known_icon(self):
        stacks = {"ai_cloud": ["OpenAI", "Gemma"], "back_end": [], "front_end": [], "database": []}
        rows = stack_rows(stacks, [])
        self.assertEqual([item["icon"] for item in rows["ai_cloud"]], [None, None])


if __name__ == "__main__":
    unittest.main()
