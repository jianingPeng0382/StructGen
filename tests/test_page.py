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
            "bibtex",
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

    def test_public_links_and_disabled_placeholders(self):
        hrefs = {link.get("href") for link in self.parser.links}
        self.assertIn("https://github.com/jianingPeng0382/StructGen", hrefs)
        self.assertIn(
            "https://huggingface.co/datasets/jianingPeng0382/StructGen", hrefs
        )
        self.assertGreaterEqual(len(self.parser.coming_soon), 2)
        for link in self.parser.coming_soon:
            self.assertNotIn("href", link)
            self.assertEqual(link.get("tabindex"), "-1")

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
            "static/images/favicon.svg",
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
        pages_url = "https://jianingpeng0382.github.io/StructGen-Project-Page/"
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
        self.assertIn('class="resource-icon resource-icon-github"', self.html)
        self.assertIn('class="resource-icon resource-icon-arxiv"', self.html)
        self.assertIn('class="resource-icon resource-icon-dataset"', self.html)

    def test_desktop_title_is_constrained_to_two_logical_lines(self):
        css = (ROOT / "static/css/site.css").read_text(encoding="utf-8")
        self.assertIn("font-size: 36px", css)
        self.assertIn("white-space: nowrap", css)
        self.assertIn(".title-line", css)

    def test_results_figures_share_the_same_width(self):
        css = (ROOT / "static/css/site.css").read_text(encoding="utf-8")
        self.assertIn(".results-figure,\n.text-generation-figure", css)
        self.assertIn("width: 96%", css)

    def test_benchmark_emphasis_uses_dark_text(self):
        css = (ROOT / "static/css/site.css").read_text(encoding="utf-8")
        self.assertIn(".section-copy strong", css)
        self.assertIn("color: var(--ink-strong)", css)


if __name__ == "__main__":
    unittest.main()
