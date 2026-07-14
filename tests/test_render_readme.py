import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
from render_readme import infer_activities, stack_badges, stacks_without_icons, without_icons


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


class StackBadgesTests(unittest.TestCase):
    def test_maps_frameworks_and_languages_across_categories(self):
        stacks = {"ai_cloud": ["AWS", "OpenAI"], "back_end": ["FastAPI", "Python"], "front_end": [], "database": ["PostgreSQL"]}
        badges = stack_badges(stacks, ["Docker"])
        self.assertEqual([badge["slug"] for badge in badges], ["aws", "fastapi", "python", "postgres", "docker"])

    def test_dedupes_by_slug(self):
        stacks = {"ai_cloud": [], "back_end": ["Python", "python"], "front_end": [], "database": []}
        badges = stack_badges(stacks, [])
        self.assertEqual(len(badges), 1)

    def test_merges_language_names_alongside_stack_items(self):
        stacks = {"ai_cloud": [], "back_end": ["FastAPI"], "front_end": [], "database": []}
        badges = stack_badges(stacks, [], language_names=["Python", "TypeScript"])
        self.assertEqual([badge["slug"] for badge in badges], ["python", "ts", "fastapi"])

    def test_skips_unmapped_items(self):
        stacks = {"ai_cloud": ["OpenAI", "Gemma"], "back_end": [], "front_end": [], "database": []}
        self.assertEqual(stack_badges(stacks, []), [])


class WithoutIconsTests(unittest.TestCase):
    def test_stacks_without_icons_drops_items_that_already_have_a_badge(self):
        stacks = {"ai_cloud": ["OpenAI", "AWS"], "back_end": ["Python"], "front_end": [], "database": []}
        filtered = stacks_without_icons(stacks)
        self.assertEqual(filtered["ai_cloud"], ["OpenAI"])
        self.assertEqual(filtered["back_end"], [])

    def test_without_icons_filters_a_plain_list(self):
        self.assertEqual(without_icons(["Docker", "SomeCustomTool"]), ["SomeCustomTool"])


if __name__ == "__main__":
    unittest.main()
