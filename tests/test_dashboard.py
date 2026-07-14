import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
from dashboard import apply_form, split_commas, split_lines


class SplitHelperTests(unittest.TestCase):
    def test_split_lines_drops_blank_lines(self):
        self.assertEqual(split_lines("AI\n\n  Cloud \n"), ["AI", "Cloud"])

    def test_split_commas_drops_blank_items(self):
        self.assertEqual(split_commas("OpenAI, , AWS ,"), ["OpenAI", "AWS"])


class ApplyFormTests(unittest.TestCase):
    def test_blank_fields_reset_to_empty_for_auto_inference(self):
        config = {"profile": {"name": "Old Name", "headline": "Old Role"}, "stacks": {"ai_cloud": ["Stale"]}}
        apply_form(config, {"github_username": "octocat"})
        self.assertEqual(config["profile"]["name"], "")
        self.assertEqual(config["profile"]["headline"], "")
        self.assertEqual(config["stacks"]["ai_cloud"], [])
        self.assertEqual(config["profile"]["github_username"], "octocat")

    def test_list_and_stack_fields_are_parsed(self):
        config = {"profile": {}, "stacks": {}}
        apply_form(config, {
            "github_username": "octocat",
            "interests": "AI\nCloud",
            "stack_back_end": "Python, FastAPI",
        })
        self.assertEqual(config["profile"]["interests"], ["AI", "Cloud"])
        self.assertEqual(config["stacks"]["back_end"], ["Python", "FastAPI"])

    def test_theme_color_only_overrides_when_provided(self):
        config = {"profile": {}, "stacks": {}, "render": {"theme_color": "7c5cfc"}}
        apply_form(config, {"github_username": "octocat", "theme_color": ""})
        self.assertEqual(config["render"]["theme_color"], "7c5cfc")
        apply_form(config, {"github_username": "octocat", "theme_color": "#ff0000"})
        self.assertEqual(config["render"]["theme_color"], "ff0000")


if __name__ == "__main__":
    unittest.main()
