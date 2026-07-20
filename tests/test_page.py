from html.parser import HTMLParser
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.images = []
        self.text_chunks = []
        self.coming_soon = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "a":
            self.links.append(attrs)
        if attrs.get("aria-disabled") == "true":
            self.coming_soon.append(attrs)
        if tag == "img":
            self.images.append(attrs)

    def handle_data(self, data):
        self.text_chunks.append(data)


class StructGenProjectPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = INDEX.read_text(encoding="utf-8")
        cls.parser = PageParser()
        cls.parser.feed(cls.html)
        cls.text = " ".join(" ".join(cls.parser.text_chunks).split())

    def test_required_sections_and_copy_are_present(self):
        required_ids = {
            "top",
            "teaser",
            "abstract",
            "structured-context",
            "structgen",
            "benchmark",
            "results",
        }
        self.assertTrue(required_ids.issubset(self.parser.ids))
        for phrase in (
            "StructGen: Disambiguating Multi-Reference Image Generation",
            "ACM MM 2026",
            "400 cases",
            "8 subsets",
            "Both authors contributed equally to this research.",
            "Corresponding authors.",
        ):
            self.assertIn(phrase, self.text)

    def test_public_resource_links_are_live(self):
        hrefs = {link.get("href") for link in self.parser.links}
        self.assertIn("https://github.com/jianingPeng0382/StructGenCode", hrefs)
        self.assertIn("https://arxiv.org/abs/2607.15619", hrefs)
        self.assertIn("https://arxiv.org/pdf/2607.15619", hrefs)
        self.assertIn(
            "https://huggingface.co/datasets/jianingPeng0382/StructGen", hrefs
        )
        self.assertEqual(self.parser.coming_soon, [])

    def test_citation_section_uses_the_published_arxiv_record(self):
        self.assertIn('id="citation"', self.html)
        self.assertIn("peng2026structgendisambiguatingmultireferenceimage", self.html)
        self.assertIn("https://arxiv.org/abs/2607.15619", self.html)

    def test_citation_restores_the_copyable_historical_layout(self):
        css = (ROOT / "static/css/site.css").read_text(encoding="utf-8")
        self.assertIn('class="container page-container citation-container"', self.html)
        self.assertIn('class="citation-heading"', self.html)
        self.assertIn('id="copy-citation"', self.html)
        self.assertIn('id="citation-code"', self.html)
        self.assertIn(".copy-button", css)
        self.assertIn("background: var(--primary) !important", css)
        self.assertIn("color: var(--secondary)", css)

    def test_citation_copy_button_uses_the_clipboard(self):
        js = (ROOT / "static/js/site.js").read_text(encoding="utf-8")
        self.assertIn('document.querySelector("#copy-citation")', js)
        self.assertIn('document.querySelector("#citation-code code")', js)
        self.assertIn("navigator.clipboard.writeText(citation)", js)
        self.assertIn('label.textContent = "Copied!"', js)

    def test_images_are_accessible_and_local(self):
        self.assertGreaterEqual(len(self.parser.images), 5)
        for image in self.parser.images:
            src = image.get("src", "")
            self.assertTrue(src.startswith("static/images/"), src)
            self.assertTrue(image.get("alt", "").strip(), src)
            self.assertTrue((ROOT / src).is_file(), src)

    def test_page_has_no_removed_probex_features(self):
        for removed in ("More Works", "Statcounter", "mathjax", "carousel"):
            self.assertNotIn(removed.lower(), self.html.lower())

    def test_relative_assets_exist(self):
        for asset in (
            "static/css/site.css",
            "static/js/site.js",
            "static/images/favicon.png",
            "static/images/favicon.jpg",
            "static/images/apple-touch-icon.png",
            "static/images/og-banner.png",
        ):
            self.assertTrue((ROOT / asset).is_file(), asset)

    def test_loader_has_a_javascript_failure_fallback(self):
        css = (ROOT / "static/css/site.css").read_text(encoding="utf-8")
        js = (ROOT / "static/js/site.js").read_text(encoding="utf-8")
        self.assertIn(".page-loader", css)
        self.assertIn("display: none", css)
        self.assertIn("html.is-loading .page-loader", css)
        self.assertIn("window.setTimeout(hideLoader, 3000)", js)

    def test_social_metadata_uses_the_final_absolute_pages_url(self):
        pages_url = "https://jianingpeng0382.github.io/StructGen/"
        self.assertIn(f'<link rel="canonical" href="{pages_url}">', self.html)
        self.assertIn(f'<meta property="og:url" content="{pages_url}">', self.html)
        self.assertIn(
            f'<meta property="og:image" content="{pages_url}static/images/og-banner.png">',
            self.html,
        )

    def test_attribution_and_license_are_explicit(self):
        self.assertIn("ProbeX", self.text)
        self.assertIn("Academic Project Page Template", self.text)
        self.assertIn("CC BY-SA 4.0", self.text)
        self.assertTrue((ROOT / "LICENSE").is_file())

    def test_refreshed_abstract_omits_redundant_code_sentence(self):
        self.assertNotIn("The code is available at", self.text)

    def test_venue_precedes_authors_and_affiliations_are_compact(self):
        venue_position = self.html.index('<p class="venue">ACM MM 2026</p>')
        author_position = self.html.index('<div class="author-list"')
        self.assertLess(venue_position, author_position)
        affiliation_start = self.html.index('<div class="affiliations"')
        affiliation_end = self.html.index("</div>", affiliation_start)
        affiliation_html = self.html[affiliation_start:affiliation_end]
        for location in ("Beijing, China", "Shanghai, China"):
            self.assertNotIn(location, affiliation_html)

    def test_refreshed_sections_use_the_approved_figures(self):
        self.assertIn(
            "Structured Context Modeling Framework",
            self.text,
        )
        self.assertIn("Structured Data Curation Pipeline", self.text)
        self.assertIn('src="static/images/dataset-comparison.webp"', self.html)
        self.assertIn('src="static/images/text-generation.webp"', self.html)
        self.assertIn('class="paper-figure paired-figures"', self.html)
        self.assertIn("all references are provided as textual descriptions", self.text)

    def test_reference_buttons_match_the_compact_dark_bar(self):
        css = (ROOT / "static/css/site.css").read_text(encoding="utf-8")
        self.assertIn("min-height: 44px", css)
        self.assertIn("font-size: 16px", css)
        self.assertIn("border-radius: 12px", css)
        self.assertIn("opacity: 1", css)
        self.assertIn('class="fas fa-file-pdf"', self.html)
        self.assertIn('class="fab fa-github"', self.html)
        self.assertIn('class="ai ai-arxiv"', self.html)
        self.assertIn('class="resource-icon resource-icon-dataset"', self.html)

    def test_probe_x_icon_fonts_are_vendored_locally(self):
        for stylesheet in (
            "static/css/fontawesome.all.min.css",
            "static/css/academicons.min.css",
        ):
            self.assertIn(f'<link rel="stylesheet" href="{stylesheet}">', self.html)
            self.assertTrue((ROOT / stylesheet).is_file(), stylesheet)

        for font in (
            "static/webfonts/fa-solid-900.woff2",
            "static/webfonts/fa-brands-400.woff2",
            "static/fonts/academicons.woff",
        ):
            self.assertTrue((ROOT / font).is_file(), font)

    def test_desktop_title_is_constrained_to_two_logical_lines(self):
        css = (ROOT / "static/css/site.css").read_text(encoding="utf-8")
        self.assertIn("font-size: 36px", css)
        self.assertIn("white-space: nowrap", css)
        self.assertIn(".title-line", css)

    def test_results_figures_share_the_same_width(self):
        css = (ROOT / "static/css/site.css").read_text(encoding="utf-8")
        self.assertIn(".results-figure,\n.text-generation-figure", css)
        self.assertIn("width: 96%", css)

    def test_white_figure_sections_and_pipeline_alignment(self):
        css = (ROOT / "static/css/site.css").read_text(encoding="utf-8")
        self.assertIn(
            'class="section section-muted section-figure-white" id="structgen"',
            self.html,
        )
        self.assertIn(
            'class="section section-muted section-figure-white" id="results"',
            self.html,
        )
        self.assertIn(".section-figure-white", css)
        self.assertIn("grid-template-columns: 1.2fr 1.9fr", css)
        self.assertIn('width="1600" height="648"', self.html)
        self.assertIn("height: auto", css)

    def test_benchmark_emphasis_uses_dark_text(self):
        css = (ROOT / "static/css/site.css").read_text(encoding="utf-8")
        self.assertIn(".section-copy strong", css)
        self.assertIn("color: var(--ink-strong)", css)


if __name__ == "__main__":
    unittest.main()
