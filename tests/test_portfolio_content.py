import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class PortfolioContentTest(unittest.TestCase):
    def test_kepco_card_links_to_detail_page(self):
        index_html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="kepco-enc.html"', index_html)

    def test_kepco_detail_page_contains_required_sections(self):
        detail_html = (ROOT / "kepco-enc.html").read_text(encoding="utf-8")
        for title in [
            "참여 프로젝트",
            "문서 OCR 관련 프로젝트",
            "도메인 특화 검색 시스템 개발",
            "기타 업무",
            "자료 링크",
        ]:
            self.assertIn(f"<h3>{title}</h3>", detail_html)

    def test_kepco_detail_page_contains_ocr_and_search_content(self):
        detail_html = (ROOT / "kepco-enc.html").read_text(encoding="utf-8")
        for phrase in [
            "문서 라벨링",
            "라벨링 결과를 바탕으로 하이퍼파라미터 튜닝",
            "OCR 라이브러리 비교",
            "표선 제거 전처리 개선",
            "OCR 하이퍼파라미터 튜닝",
            "영어 PDF 원문을 RAG에 적합한 검색형 문장 데이터로 변환하는 전처리 파이프라인",
            "문장 단위로 저장",
            "Paper PDF Extractor",
            "라벨링 결과 분석 PDF 바로 열기",
        ]:
            self.assertIn(phrase, detail_html)

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

    def test_kepco_detail_page_keeps_detail_page_shell(self):
        detail_html = (ROOT / "kepco-enc.html").read_text(encoding="utf-8")
        self.assertIn('<meta name="viewport" content="width=device-width, initial-scale=1.0">', detail_html)
        self.assertIn('class="page-shell"', detail_html)
