import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
DETAIL_PAGES = {
    "moa.html": "projects/moa/page.html",
    "healthcare-ai.html": "projects/healthcare-ai/page.html",
    "sebook.html": "projects/sebook/page.html",
    "rawfishs.html": "projects/rawfishs/page.html",
    "kepco-enc.html": "projects/kepco-enc/page.html",
    "digital-sprout.html": "projects/digital-sprout/page.html",
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
                self.assertIn(f'src="{SHARED_DETAIL_LOADER}?v=', detail_html)
                self.assertIn(f'data-detail-source="{project_page}"', detail_html)

    def test_project_folder_pages_exist(self):
        for project_page in DETAIL_PAGES.values():
            with self.subTest(page=project_page):
                self.assertTrue((ROOT / project_page).exists())

    def test_kepco_card_links_to_detail_page(self):
        index_html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="kepco-enc.html"', index_html)

    def test_rawfishs_card_links_to_detail_page(self):
        index_html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="rawfishs.html"', index_html)

    def test_digital_sprout_activity_card_links_to_detail_page(self):
        index_html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="digital-sprout.html"', index_html)

    def test_digital_sprout_page_does_not_show_operation_flow_image(self):
        detail_html = (ROOT / "projects/digital-sprout/page.html").read_text(encoding="utf-8")

        self.assertNotIn("camp-mentoring-flow.svg", detail_html)
        self.assertFalse((ROOT / "projects/digital-sprout/assets/camp-mentoring-flow.svg").exists())

    def test_digital_sprout_tech_stack_table_gives_more_space_to_method_and_reason(self):
        detail_html = (ROOT / "projects/digital-sprout/page.html").read_text(encoding="utf-8")
        tech_stack_table = detail_html.split('<h2 id="tech-stack">Tech Stack</h2>', 1)[1].split("</table>", 1)[0]

        self.assertIn('<col style="width: 20%;">', tech_stack_table)
        self.assertIn('<col style="width: 34%;">', tech_stack_table)
        self.assertIn('<col style="width: 46%;">', tech_stack_table)
        self.assertLess(
            tech_stack_table.index('<col style="width: 20%;">'),
            tech_stack_table.index('<col style="width: 34%;">'),
        )
        self.assertLess(
            tech_stack_table.index('<col style="width: 34%;">'),
            tech_stack_table.index('<col style="width: 46%;">'),
        )

    def test_digital_sprout_sidebar_meta_values_are_korean(self):
        detail_html = (ROOT / "projects/digital-sprout/page.html").read_text(encoding="utf-8")
        meta_block = detail_html.split('<div class="doc-meta-list">', 1)[1].split("</div>\n          </div>", 1)[0]

        self.assertIn("<strong>Status</strong>", meta_block)
        self.assertIn("<strong>Role</strong>", meta_block)
        self.assertIn("<strong>Focus</strong>", meta_block)
        self.assertIn("<span>대외활동 · 멘토링</span>", meta_block)
        self.assertIn("<span>팀장, 운영 총괄, 인공지능 실습 멘토</span>", meta_block)
        self.assertIn("<span>학생 참여 유도, 수업 운영, 현장 문제 해결</span>", meta_block)
        for phrase in [
            "external-activity",
            "team-lead",
            "operation manager",
            "AI practice mentor",
            "student engagement",
            "lesson operation",
            "on-site problem solving",
        ]:
            self.assertNotIn(phrase, meta_block)

    def test_digital_sprout_page_labels_activity_as_experience(self):
        detail_html = (ROOT / "projects/digital-sprout/page.html").read_text(encoding="utf-8")

        self.assertIn('<p class="side-label">Experience</p>', detail_html)
        self.assertIn('<p class="eyebrow">Experience</p>', detail_html)
        self.assertNotIn('<p class="side-label">경험</p>', detail_html)
        self.assertNotIn('<p class="eyebrow">경험</p>', detail_html)
        self.assertNotIn('<p class="side-label">Project</p>', detail_html)
        self.assertNotIn('<p class="eyebrow">Project</p>', detail_html)

    def test_digital_sprout_features_section_is_labeled_as_major_activities(self):
        detail_html = (ROOT / "projects/digital-sprout/page.html").read_text(encoding="utf-8")

        self.assertIn('<h2 id="features">주요 활동</h2>', detail_html)
        self.assertIn('<li><a href="#features">주요 활동</a></li>', detail_html)
        self.assertNotIn('<h2 id="features">Key Features</h2>', detail_html)
        self.assertNotIn('<li><a href="#features">Key Features</a></li>', detail_html)

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
                expected_heading = "Experience" if project_page == "projects/digital-sprout/page.html" else "Project"
                expected_features = "주요 활동" if project_page == "projects/digital-sprout/page.html" else "Key Features"
                for phrase in [
                    expected_heading,
                    "Overview",
                    "Tech Stack",
                    expected_features,
                    "Retrospective",
                    "Links",
                ]:
                    self.assertIn(phrase, detail_html)
                if project_page == "projects/digital-sprout/page.html":
                    self.assertIn("활동 내용", detail_html)
                else:
                    self.assertIn("개발 내용", detail_html)
                self.assertNotIn('class="toc-box"', detail_html)
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
                    'href="#development"',
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

    def test_all_detail_pages_use_home_style_header_navigation(self):
        for project_page in DETAIL_PAGES.values():
            with self.subTest(page=project_page):
                detail_html = (ROOT / project_page).read_text(encoding="utf-8")
                header_block = detail_html.split("<header", 1)[1].split("</header>", 1)[0]
                self.assertIn('<a class="brand" href="../../index.html">shin yeong ok</a>', header_block)
                self.assertIn('href="../../index.html#projects"', header_block)
                self.assertIn('href="../../index.html#external-activity"', header_block)
                self.assertIn('href="../../index.html#experience"', header_block)
                self.assertIn('href="../../index.html#credentials"', header_block)
                self.assertIn('href="https://github.com/young-ok-sin" target="_blank" rel="noreferrer"', header_block)
                self.assertNotIn(">Back</a>", header_block)
                self.assertNotIn("shin yeong ok / ", header_block)

    def test_all_detail_pages_use_development_details_lists(self):
        for project_page in DETAIL_PAGES.values():
            with self.subTest(page=project_page):
                detail_html = (ROOT / project_page).read_text(encoding="utf-8")
                if project_page == "projects/digital-sprout/page.html":
                    self.assertIn('<h2 id="development">활동 내용</h2>', detail_html)
                else:
                    self.assertIn('<h2 id="development">개발 내용</h2>', detail_html)
                self.assertIn('class="development-list"', detail_html)
                self.assertIn('class="development-item"', detail_html)
                self.assertIn('class="development-summary"', detail_html)
                self.assertIn('class="development-points"', detail_html)
                self.assertNotIn('class="troubleshooting-entry"', detail_html)
                self.assertNotIn('class="troubleshooting-tile"', detail_html)

    def test_css_contains_shared_detail_page_mobile_rules(self):
        css = (ROOT / SHARED_DETAIL_CSS).read_text(encoding="utf-8")
        self.assertIn(".detail-page", css)
        self.assertIn(".detail-page .page-shell[data-readme-layout=\"true\"]", css)
        self.assertIn(".detail-page .markdown-document", css)
        self.assertIn(".doc-action", css)

    def test_detail_page_loader_bypasses_stale_browser_cache(self):
        loader_js = (ROOT / SHARED_DETAIL_LOADER).read_text(encoding="utf-8")
        self.assertIn("cache: \"no-store\"", loader_js)

    def test_detail_pages_keep_fixed_top_header_layout(self):
        css = (ROOT / SHARED_DETAIL_CSS).read_text(encoding="utf-8")
        self.assertIn(".detail-page .site-header", css)
        self.assertIn("position: fixed;", css)
        self.assertIn("scroll-padding-top:", css)
        self.assertIn(".detail-page .page-shell", css)

    def test_detail_pages_preserve_project_identity(self):
        expected_labels = {
            "projects/moa/page.html": ["MoA", "state-transition", "polling"],
            "projects/healthcare-ai/page.html": ["Healthcare AI", "blockchain", "spring-boot"],
            "projects/sebook/page.html": ["SEBook", "recommendation", "community"],
            "projects/rawfishs/page.html": ["Rawfishs", "websocket", "Redis", "action item"],
            "projects/kepco-enc/page.html": ["KEPCO", "Paper PDF Extractor", "ocr"],
            "projects/digital-sprout/page.html": [
                "디지털 새싹 캠프",
                "team-lead",
                "Neobot",
                "wumt.da",
            ],
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
            "상태 정합성과 동시성 제어 보강",
            "외부 연동이 포함된 기능은 요청-응답 흐름과 후처리 흐름을 분리해야 안정적으로 운영할 수 있다는 점을 확인했습니다.",
        ]:
            self.assertIn(phrase, detail_html)
        self.assertNotIn(
            "이 문서에서는 MoA에서 맡았던 목표 생성, 비동기 파이프라인, 상태 정합성 문제를 포트폴리오용 README 형식으로 정리했습니다.",
            detail_html,
        )
        self.assertNotIn('class="badge-row"', detail_html)

    def test_moa_page_includes_ai_pipeline_diagram_asset(self):
        detail_html = (ROOT / "projects/moa/page.html").read_text(encoding="utf-8")
        asset_path = ROOT / "projects/moa/assets/ai-pipeline-sequence.svg"

        self.assertTrue(asset_path.exists())
        self.assertIn('src="/projects/moa/assets/ai-pipeline-sequence.svg"', detail_html)
        self.assertIn('class="doc-figure"', detail_html)

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

    def test_credentials_section_merges_microsoft_fundamentals_and_adds_engineer_cert(self):
        index_html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn("<h4>Certificates</h4>", index_html)
        self.assertIn("정보처리기사", index_html)
        self.assertIn("Microsoft Fundamentals Certifications (AZ-900, AI-900)", index_html)
        self.assertNotIn("AZ-900: Microsoft Azure Fundamentals", index_html)
        self.assertNotIn("AI-900: Microsoft Azure AI Fundamentals", index_html)

        certificates_block = index_html.split("<h4>Certificates</h4>", 1)[1].split("</article>", 1)[0]
        awards_block = index_html.split("<h4>Awards</h4>", 1)[1].split("</article>", 1)[0]
        self.assertNotIn("<span>4</span>", certificates_block)
        self.assertNotIn("<span>2</span>", awards_block)

    def test_home_css_keeps_hero_line_breaks_at_word_level(self):
        css = (ROOT / HOME_CSS).read_text(encoding="utf-8")
        self.assertIn("word-break: keep-all;", css)
        self.assertIn("overflow-wrap: normal;", css)
        self.assertIn("text-wrap: balance;", css)

    def test_home_css_does_not_cap_hero_heading_width(self):
        css = (ROOT / HOME_CSS).read_text(encoding="utf-8")
        hero_heading_block = css.split(".hero-panel h2 {", 1)[1].split("}", 1)[0]
        self.assertNotIn("max-width:", hero_heading_block)
