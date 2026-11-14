"""Offline portability and script safety under the project's unittest runner."""
import base64
import json
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch

from scripts import build_spatial_explorer as explorer


class ExplorerAssemblyTests(unittest.TestCase):
    def test_saved_html_carries_data_and_historical_image_without_script_injection(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            files = {
                "outputs/native_atlas/payload.json": {"exports": [{"file_id": "source</script><script>"}]},
                "metadata/input_manifest.json": [],
                "outputs/inventory/file_audit.json": [],
                "outputs/inventory/summary.json": {},
                "outputs/native_atlas/historical_context.json": {"figures": [{"path": "outputs/native_atlas/historical_figures/example.png", "caption": "Historical dataset"}]},
            }
            for relative, value in files.items():
                p = root / relative
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(json.dumps(value))
            from PIL import Image
            image_path = root / "outputs/native_atlas/historical_figures/example.png"
            image_path.parent.mkdir(parents=True, exist_ok=True)
            Image.new("RGB", (4, 4), "navy").save(image_path)
            expected_image = base64.b64encode(image_path.read_bytes()).decode("ascii")
            with patch.object(explorer, "get_plotlyjs", return_value="/* locally embedded plotting runtime */"):
                info = explorer.build(root)
            result = Path(info["path"]).read_text()
            image_path.unlink()  # Standalone output must still contain all pixels.
            self.assertIn("data:image/png;base64," + expected_image, result)
            self.assertIn('"path":"outputs/native_atlas/historical_figures/example.png"', result)
            self.assertIn("source\\u003c/script>\\u003cscript>", result)
            self.assertNotIn("source</script>", result)
            self.assertNotIn("__PAYLOAD__", result)
            self.assertNotIn("__PLOTLY__", result)
            self.assertFalse(info["network_required"])
            self.assertIsNone(re.search(r'<script[^>]+src=["\']https?://', result))

    def test_supporting_navigation_resolves_to_existing_project_files(self):
        template = (explorer.ROOT / "scripts/spatial_explorer.html").read_text()
        base = explorer.ROOT / "outputs/app"
        for relative in re.findall(r'href="([^"]+)"', template):
            if relative == "input_audit.html":
                continue
            with self.subTest(relative=relative):
                self.assertFalse(relative.startswith(("http:", "https:")))
                self.assertTrue((base / relative).is_file())


if __name__ == "__main__":
    unittest.main()
