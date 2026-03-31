import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
DETAIL_PAGES = [
    "moa.html",
    "healthcare-ai.html",
    "sebook.html",
    "kepco-enc.html",
]


class PortfolioContentTest(unittest.TestCase):
    def test_kepco_card_links_to_detail_page(self):
        index_html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="kepco-enc.html"', index_html)

    def test_all_detail_pages_use_readme_document_structure(self):
        for page_name in DETAIL_PAGES:
            with self.subTest(page=page_name):
                detail_html = (ROOT / page_name).read_text(encoding="utf-8")
                self.assertIn('class="page-shell"', detail_html)
                self.assertIn('class="markdown-document"', detail_html)
                for phrase in [
                    "README",
                    "Table of Contents",
                    "Overview",
                    "Tech Stack",
                    "Key Features",
                    "Troubleshooting",
                    "Retrospective",
                    "Links",
                ]:
                    self.assertIn(phrase, detail_html)
                self.assertIn("<table>", detail_html)
                self.assertIn("<blockquote>", detail_html)
                self.assertIn("<pre><code>", detail_html)

    def test_all_detail_pages_have_right_side_section_navigation(self):
        for page_name in DETAIL_PAGES:
            with self.subTest(page=page_name):
                detail_html = (ROOT / page_name).read_text(encoding="utf-8")
                self.assertIn('class="section-nav"', detail_html)
                for anchor in [
                    'href="#overview"',
                    'href="#tech-stack"',
                    'href="#features"',
                    'href="#troubleshooting"',
                    'href="#retrospective"',
                    'href="#links"',
                ]:
                    self.assertIn(anchor, detail_html)

    def test_css_hides_right_side_section_navigation_on_mobile(self):
        css = (ROOT / "moa.css").read_text(encoding="utf-8")
        self.assertIn(".section-nav", css)
        self.assertIn("display: none;", css)

    def test_all_detail_pages_use_icon_style_footer_actions(self):
        for page_name in DETAIL_PAGES:
            with self.subTest(page=page_name):
                detail_html = (ROOT / page_name).read_text(encoding="utf-8")
                self.assertIn('class="doc-action"', detail_html)
                self.assertIn("<svg", detail_html)

    def test_css_contains_shared_detail_page_mobile_rules(self):
        css = (ROOT / "moa.css").read_text(encoding="utf-8")
        self.assertIn(".detail-page", css)
        self.assertIn(".detail-page .page-shell[data-readme-layout=\"true\"]", css)
        self.assertIn(".detail-page .markdown-document", css)
        self.assertIn(".doc-action", css)

    def test_detail_pages_preserve_project_identity(self):
        expected_labels = {
            "moa.html": ["MoA", "state-transition", "polling"],
            "healthcare-ai.html": ["Healthcare AI", "blockchain", "spring-boot"],
            "sebook.html": ["SEBook", "recommendation", "community"],
            "kepco-enc.html": ["KEPCO", "Paper PDF Extractor", "ocr"],
        }
        for page_name, phrases in expected_labels.items():
            with self.subTest(page=page_name):
                detail_html = (ROOT / page_name).read_text(encoding="utf-8")
                for phrase in phrases:
                    self.assertIn(phrase, detail_html)

    def test_healthcare_and_sebook_repo_links_remain(self):
        healthcare_html = (ROOT / "healthcare-ai.html").read_text(encoding="utf-8")
        sebook_html = (ROOT / "sebook.html").read_text(encoding="utf-8")

        self.assertIn(
            'href="https://github.com/young-ok-sin/my-health-block-original-server" target="_blank" rel="noreferrer"',
            healthcare_html,
        )
        self.assertIn(
            'href="https://github.com/young-ok-sin/SEBook_backend" target="_blank" rel="noreferrer"',
            sebook_html,
        )

    def test_kepco_detail_page_keeps_pdf_and_repo_links(self):
        detail_html = (ROOT / "kepco-enc.html").read_text(encoding="utf-8")
        self.assertIn(
            'href="assets/docs/kepco-labeling-analysis.pdf" target="_blank" rel="noreferrer"',
            detail_html,
        )
        self.assertIn(
            'href="https://github.com/young-ok-sin/pdf-extractor" target="_blank" rel="noreferrer"',
            detail_html,
        )

    def test_sample_project_page_contains_required_readme_sections(self):
        sample_page = ROOT / "sample-project.html"
        self.assertTrue(sample_page.exists())
        if not sample_page.exists():
            return

        detail_html = sample_page.read_text(encoding="utf-8")
        for phrase in [
            "README",
            "Table of Contents",
            "Overview",
            "Tech Stack",
            "Features",
            "Installation",
            "Directory Structure",
            "Troubleshooting",
            "Retrospective",
            "build-passing",
        ]:
            self.assertIn(phrase, detail_html)

    def test_sample_project_page_uses_detail_shell(self):
        sample_page = ROOT / "sample-project.html"
        self.assertTrue(sample_page.exists())
        if not sample_page.exists():
            return

        detail_html = sample_page.read_text(encoding="utf-8")
        self.assertIn('<meta name="viewport" content="width=device-width, initial-scale=1.0">', detail_html)
        self.assertIn('class="page-shell"', detail_html)
        self.assertIn("<pre><code>", detail_html)
        self.assertIn("<table>", detail_html)
        self.assertIn("<blockquote>", detail_html)
