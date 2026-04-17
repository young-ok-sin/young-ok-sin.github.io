import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
PAGES_WORKFLOW = ".github/workflows/static.yml"
DETAIL_PAGES = [
    "moa.html",
    "healthcare-ai.html",
    "sebook.html",
    "rawfishs.html",
    "kepco-enc.html",
    "digital-sprout.html",
]


class PagesWorkflowTest(unittest.TestCase):
    def test_pages_workflow_publishes_all_root_detail_pages(self):
        workflow = (ROOT / PAGES_WORKFLOW).read_text(encoding="utf-8")
        for entry_page in DETAIL_PAGES:
            with self.subTest(page=entry_page):
                self.assertIn(f"cp {entry_page} .pages-dist/", workflow)
