import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class PortfolioContentTest(unittest.TestCase):
    def test_kepco_card_links_to_detail_page(self):
        index_html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="kepco-enc.html"', index_html)

    def test_kepco_detail_page_contains_pdf_and_repo_links(self):
        detail_html = (ROOT / "kepco-enc.html").read_text(encoding="utf-8")
        self.assertIn(
            'href="assets/docs/kepco-labeling-analysis.pdf" target="_blank" rel="noreferrer"',
            detail_html,
        )
        self.assertIn(
            'href="https://github.com/young-ok-sin/pdf-extractor" target="_blank" rel="noreferrer"',
            detail_html,
        )
        self.assertIn("Paper PDF Extractor", detail_html)

    def test_kepco_detail_page_keeps_detail_page_shell(self):
        detail_html = (ROOT / "kepco-enc.html").read_text(encoding="utf-8")
        self.assertIn('<meta name="viewport" content="width=device-width, initial-scale=1.0">', detail_html)
        self.assertIn('class="page-shell"', detail_html)
