import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
DETAIL_CSS = ROOT / "projects/shared/detail-page.css"


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
        self.assertIn("max-width: none;", image_block)
        self.assertIn("height: auto;", image_block)
        self.assertNotIn("width: max(", image_block)


if __name__ == "__main__":
    unittest.main()
