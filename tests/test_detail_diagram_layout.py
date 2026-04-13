import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
DETAIL_CSS = ROOT / "projects/shared/detail-page.css"
DETAIL_LOADER = ROOT / "projects/shared/detail-page-loader.js"
MOA_DIAGRAM = ROOT / "projects/moa/assets/ai-pipeline-sequence.svg"
DETAIL_PROJECT_PAGES = [
    ROOT / "projects/moa/page.html",
    ROOT / "projects/healthcare-ai/page.html",
    ROOT / "projects/sebook/page.html",
    ROOT / "projects/rawfishs/page.html",
    ROOT / "projects/kepco-enc/page.html",
]


def css_block(css, selector):
    return css.split(f"{selector} {{", 1)[1].split("}", 1)[0]


class DetailDiagramLayoutTest(unittest.TestCase):
    def test_doc_figure_keeps_diagram_overflow_inside_image_container(self):
        css = DETAIL_CSS.read_text(encoding="utf-8")
        figure_block = css_block(css, ".doc-figure")
        image_block = css_block(css, ".doc-figure img")

        self.assertIn("width: 100%;", figure_block)
        self.assertIn("max-width: 100%;", figure_block)
        self.assertIn("min-width: 0;", figure_block)
        self.assertIn("overflow-x: auto;", figure_block)
        self.assertIn("overflow-y: hidden;", figure_block)

        self.assertIn("width: auto;", image_block)
        self.assertIn("max-width: 100%;", image_block)
        self.assertIn("height: auto;", image_block)
        self.assertNotIn("width: max(", image_block)

    def test_readme_layout_grid_items_can_shrink_around_wide_diagrams(self):
        css = DETAIL_CSS.read_text(encoding="utf-8")
        content_column_block = css_block(css, ".content-column")
        document_block = css_block(css, ".markdown-document")

        self.assertIn("min-width: 0;", content_column_block)
        self.assertIn("min-width: 0;", document_block)

    def test_doc_figure_limits_diagram_display_size(self):
        css = DETAIL_CSS.read_text(encoding="utf-8")
        image_block = css_block(css, ".doc-figure img")

        self.assertIn("max-height:", image_block)
        self.assertIn("max-width: 100%;", image_block)

    def test_readme_tables_wrap_inside_document_panel(self):
        css = DETAIL_CSS.read_text(encoding="utf-8")
        table_block = css_block(css, ".markdown-document table")
        cell_block = css_block(css, ".markdown-document th,\n.markdown-document td")

        self.assertIn("table-layout: fixed;", table_block)
        self.assertIn("overflow-wrap: anywhere;", cell_block)

    def test_moa_diagram_uses_readable_korean_labels(self):
        svg = MOA_DIAGRAM.read_text(encoding="utf-8")

        self.assertTrue(svg.startswith('<?xml version="1.0" encoding="UTF-8"?>'))

        for phrase in [
            "\ubaa9\ud45c \uc0dd\uc131 \uc694\uccad",
            "\ud6c4\ucc98\ub9ac\ub294 \ube44\ub3d9\uae30\ub85c \uc9c4\ud589",
            "\uc601\uc0c1 \uc0dd\uc131 \uc694\uccad",
            "\uc644\ub8cc \ub610\ub294 \uc2e4\ud328 \uc0c1\ud0dc \ubc18\uc601",
        ]:
            self.assertIn(phrase, svg)

        for broken_fragment in ["\uf9cf", "\u936e", "\u6e72", "?\\uc579"]:
            self.assertNotIn(broken_fragment, svg)

    def test_moa_diagram_keeps_original_exported_sequence_asset(self):
        svg = MOA_DIAGRAM.read_text(encoding="utf-8")

        self.assertIn('id="mermaid-', svg)
        self.assertIn('width="1879.3001708984375"', svg)
        self.assertIn('height="1392.599609375"', svg)

    def test_detail_loader_adds_click_to_zoom_for_diagrams(self):
        loader = DETAIL_LOADER.read_text(encoding="utf-8")

        self.assertIn("setupFigureZoom", loader)
        self.assertIn("dialog", loader)
        self.assertIn("showModal", loader)
        self.assertIn("data-zoom-ready", loader)
        self.assertIn("Open enlarged diagram", loader)

    def test_detail_loader_cache_busts_svg_diagram_assets(self):
        loader = DETAIL_LOADER.read_text(encoding="utf-8")

        self.assertIn("DETAIL_ASSET_VERSION", loader)
        self.assertIn("url.searchParams.set(\"v\", DETAIL_ASSET_VERSION)", loader)

    def test_direct_project_pages_load_versioned_detail_loader(self):
        for page in DETAIL_PROJECT_PAGES:
            with self.subTest(page=page.relative_to(ROOT)):
                detail_html = page.read_text(encoding="utf-8")

                self.assertIn('src="../shared/detail-page-loader.js?v=', detail_html)


if __name__ == "__main__":
    unittest.main()
