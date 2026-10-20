import tempfile
import unittest
from pathlib import Path
from scripts.check_profile_links import check_file, local_target


class ProfileLinksTests(unittest.TestCase):
    def test_local_target_preserves_filename_strips_fragment(self):
        with tempfile.TemporaryDirectory() as dirname:
            root = Path(dirname)
            source = root / "README.md"
            self.assertEqual(local_target(source, "docs/proof.md#heading", root),
                             root / "docs" / "proof.md")

    def test_external_and_fragment_links_are_ignored(self):
        with tempfile.TemporaryDirectory() as dirname:
            root = Path(dirname)
            source = root / "README.md"
            for ref in ("https://github.com/atomicdjt", "#overview", "mailto:example@example.com"):
                self.assertIsNone(local_target(source, ref, root))

    def test_missing_markdown_and_html_references_fail(self):
        with tempfile.TemporaryDirectory() as dirname:
            root = Path(dirname)
            readme = root / "README.md"
            readme.write_text('[missing](docs/nope.md)\n<img src="images/none.svg" />')
            result = check_file(readme, root)
            self.assertEqual(len(result), 2)

    def test_existing_relative_images_and_files_pass(self):
        with tempfile.TemporaryDirectory() as dirname:
            root = Path(dirname)
            (root / "assets").mkdir()
            (root / "assets" / "hero.svg").write_text("<svg></svg>")
            (root / "docs").mkdir()
            (root / "docs" / "guide.md").write_text("# guide")
            readme = root / "README.md"
            readme.write_text('![hero](assets/hero.svg)\n[guide](docs/guide.md#intro)')
            self.assertEqual(check_file(readme, root), [])


if __name__ == "__main__":
    unittest.main()
