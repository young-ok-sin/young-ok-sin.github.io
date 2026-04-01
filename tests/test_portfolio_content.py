import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
DETAIL_PAGES = {
    "moa.html": "projects/moa/page.html",
    "healthcare-ai.html": "projects/healthcare-ai/page.html",
    "sebook.html": "projects/sebook/page.html",
    "kepco-enc.html": "projects/kepco-enc/page.html",
}
SHARED_DETAIL_CSS = "projects/shared/detail-page.css"
SHARED_DETAIL_LOADER = "projects/shared/detail-page-loader.js"
HOME_CSS = "styles/home.css"
PROFILE_IMAGE = "assets/images/profile.jpg"
SAMPLE_PROJECT_PAGE = "examples/sample-project.html"


class PortfolioContentTest(unittest.TestCase):
    def test_home_page_uses_role_based_asset_folders(self):
        index_html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn(f'href="{HOME_CSS}"', index_html)
        self.assertIn(f'src="{PROFILE_IMAGE}"', index_html)
        self.assertTrue((ROOT / HOME_CSS).exists())
        self.assertTrue((ROOT / PROFILE_IMAGE).exists())

    def test_root_keeps_only_public_entry_html_files(self):
        for path in ["style.css", "profile.jpg", "moa.css", "sample-project.html"]:
            with self.subTest(path=path):
                self.assertFalse((ROOT / path).exists())

    def test_root_detail_pages_keep_public_urls(self):
        for entry_page, project_page in DETAIL_PAGES.items():
            with self.subTest(page=entry_page):
                detail_html = (ROOT / entry_page).read_text(encoding="utf-8")
                self.assertIn(f'href="{SHARED_DETAIL_CSS}"', detail_html)
                self.assertIn(f'src="{SHARED_DETAIL_LOADER}"', detail_html)
                self.assertIn(f'data-detail-source="{project_page}"', detail_html)

    def test_project_folder_pages_exist(self):
        for project_page in DETAIL_PAGES.values():
            with self.subTest(page=project_page):
                self.assertTrue((ROOT / project_page).exists())

    def test_kepco_card_links_to_detail_page(self):
        index_html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="kepco-enc.html"', index_html)

    def test_kepco_experience_card_uses_jump_icon(self):
        index_html = (ROOT / "index.html").read_text(encoding="utf-8")
        card_start = '<a class="panel-card project-card-link" href="kepco-enc.html" aria-label="한국전력기술 상세 페이지로 이동">'
        card_end = "</a>"
        self.assertIn(card_start, index_html)
        kepco_card = index_html.split(card_start, 1)[1].split(card_end, 1)[0]
        self.assertIn('<span class="card-jump" aria-hidden="true">', kepco_card)

    def test_all_detail_pages_use_readme_document_structure(self):
        for project_page in DETAIL_PAGES.values():
            with self.subTest(page=project_page):
                detail_html = (ROOT / project_page).read_text(encoding="utf-8")
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
        for project_page in DETAIL_PAGES.values():
            with self.subTest(page=project_page):
                detail_html = (ROOT / project_page).read_text(encoding="utf-8")
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
        css = (ROOT / SHARED_DETAIL_CSS).read_text(encoding="utf-8")
        self.assertIn(".section-nav", css)
        self.assertIn("display: none;", css)

    def test_all_detail_pages_use_icon_style_footer_actions(self):
        for project_page in DETAIL_PAGES.values():
            with self.subTest(page=project_page):
                detail_html = (ROOT / project_page).read_text(encoding="utf-8")
                self.assertIn('class="doc-action"', detail_html)
                self.assertIn("<svg", detail_html)

    def test_css_contains_shared_detail_page_mobile_rules(self):
        css = (ROOT / SHARED_DETAIL_CSS).read_text(encoding="utf-8")
        self.assertIn(".detail-page", css)
        self.assertIn(".detail-page .page-shell[data-readme-layout=\"true\"]", css)
        self.assertIn(".detail-page .markdown-document", css)
        self.assertIn(".doc-action", css)

    def test_detail_pages_preserve_project_identity(self):
        expected_labels = {
            "projects/moa/page.html": ["MoA", "state-transition", "polling"],
            "projects/healthcare-ai/page.html": ["Healthcare AI", "blockchain", "spring-boot"],
            "projects/sebook/page.html": ["SEBook", "recommendation", "community"],
            "projects/kepco-enc/page.html": ["KEPCO", "Paper PDF Extractor", "ocr"],
        }
        for project_page, phrases in expected_labels.items():
            with self.subTest(page=project_page):
                detail_html = (ROOT / project_page).read_text(encoding="utf-8")
                for phrase in phrases:
                    self.assertIn(phrase, detail_html)

    def test_moa_page_uses_rewritten_portfolio_copy(self):
        detail_html = (ROOT / "projects/moa/page.html").read_text(encoding="utf-8")
        for phrase in [
            "금융 데이터 기반 목표 관리 서비스에서 목표 생성 이후 AI 후처리까지 이어지는 흐름을 설계한 백엔드 프로젝트입니다.",
            "목표 생성 API를 구현하면서 단순 저장에 그치지 않고 우선순위 이동, 예산 재배치, 즉시 저축 반영까지 하나의 흐름으로 묶었습니다.",
            "영상 생성은 polling scheduler로 추적했고, PROCESSING, SUCCEEDED, FAILED 상태를 나눠 장시간 작업을 관리했습니다.",
            "@Version 기반 낙관적 락과 조건부 update를 적용해 비동기 상태 변경 중 오래된 데이터가 최신 상태를 덮어쓰는 문제를 줄였습니다.",
            "외부 연동이 포함된 기능은 요청-응답 흐름과 후처리 흐름을 분리해야 안정적으로 운영할 수 있다는 점을 확인했습니다.",
        ]:
            self.assertIn(phrase, detail_html)
        self.assertNotIn(
            "이 문서에서는 MoA에서 맡았던 목표 생성, 비동기 파이프라인, 상태 정합성 문제를 포트폴리오용 README 형식으로 정리했습니다.",
            detail_html,
        )
        self.assertNotIn('class="badge-row"', detail_html)

    def test_healthcare_and_sebook_repo_links_remain(self):
        healthcare_html = (ROOT / "projects/healthcare-ai/page.html").read_text(encoding="utf-8")
        sebook_html = (ROOT / "projects/sebook/page.html").read_text(encoding="utf-8")

        self.assertIn(
            'href="https://github.com/young-ok-sin/my-health-block-original-server" target="_blank" rel="noreferrer"',
            healthcare_html,
        )
        self.assertIn(
            'href="https://github.com/young-ok-sin/SEBook_backend" target="_blank" rel="noreferrer"',
            sebook_html,
        )

    def test_kepco_detail_page_keeps_pdf_and_repo_links(self):
        detail_html = (ROOT / "projects/kepco-enc/page.html").read_text(encoding="utf-8")
        self.assertIn(
            'href="../../assets/docs/kepco-labeling-analysis.pdf" target="_blank" rel="noreferrer"',
            detail_html,
        )
        self.assertIn(
            'href="https://github.com/young-ok-sin/pdf-extractor" target="_blank" rel="noreferrer"',
            detail_html,
        )

    def test_sample_project_page_contains_required_readme_sections(self):
        sample_page = ROOT / SAMPLE_PROJECT_PAGE
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
        sample_page = ROOT / SAMPLE_PROJECT_PAGE
        self.assertTrue(sample_page.exists())
        if not sample_page.exists():
            return

        detail_html = sample_page.read_text(encoding="utf-8")
        self.assertIn('<meta name="viewport" content="width=device-width, initial-scale=1.0">', detail_html)
        self.assertIn('href="../projects/shared/detail-page.css"', detail_html)
        self.assertIn('class="page-shell"', detail_html)
        self.assertIn("<pre><code>", detail_html)
        self.assertIn("<table>", detail_html)
        self.assertIn("<blockquote>", detail_html)
