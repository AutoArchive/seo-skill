from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CODE = ROOT / "skills" / "configure-google-seo-export" / "assets" / "Code.gs"
MANIFEST = ROOT / "skills" / "configure-google-seo-export" / "assets" / "appsscript.json"


class GoogleNativeExportPolicyTests(unittest.TestCase):
    def test_template_has_only_placeholder_routing(self) -> None:
        text = CODE.read_text(encoding="utf-8")
        self.assertIn("DRIVE_FOLDER_ID", text)
        self.assertIn("GA4_PROPERTY_ID", text)
        self.assertNotIn("@gmail.com", text)
        self.assertNotRegex(text, r"folderId:\s*'[A-Za-z0-9_-]{20,}'")
        self.assertNotRegex(text, r"propertyId:\s*'\d{6,}'")

    def test_manifest_keeps_provider_data_read_only(self) -> None:
        text = MANIFEST.read_text(encoding="utf-8")
        self.assertIn("analytics.readonly", text)
        self.assertIn("webmasters.readonly", text)
        self.assertNotIn('"https://www.googleapis.com/auth/analytics"', text)
        self.assertNotIn('"https://www.googleapis.com/auth/webmasters"', text)


if __name__ == "__main__":
    unittest.main()
