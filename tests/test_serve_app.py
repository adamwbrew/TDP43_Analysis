"""The convenience launcher serves saved outputs without exposing raw inputs."""

from contextlib import redirect_stderr
import errno
from io import StringIO
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from scripts.serve_app import AppRequestHandler, app_directory, main


class AppLauncherTests(unittest.TestCase):
    def saved_app(self, root):
        directory = Path(root) / "outputs" / "app"
        directory.mkdir(parents=True)
        (directory / "index.html").write_text("<!doctype html><title>Saved COMET</title>")
        return directory

    def test_saved_app_is_found_without_analysis_inputs(self):
        with tempfile.TemporaryDirectory() as root:
            directory = self.saved_app(root)
            self.assertEqual(app_directory(root), directory.resolve())

    def test_missing_saved_app_explains_how_to_get_it_without_starting_server(self):
        with tempfile.TemporaryDirectory() as root, patch("scripts.serve_app.ThreadingHTTPServer") as server:
            output = StringIO()
            with redirect_stderr(output):
                self.assertEqual(main(["--no-browser"], project_root=root), 1)
            self.assertIn("saved app is missing", output.getvalue())
            self.assertIn("Raw data are not needed", output.getvalue())
            server.assert_not_called()

    def test_symlink_cannot_serve_a_raw_file_outside_the_app(self):
        with tempfile.TemporaryDirectory() as root:
            directory = self.saved_app(root)
            raw = Path(root) / "raw.csv"
            raw.write_text("private source data")
            (directory / "outside.csv").symlink_to(raw)
            handler = object.__new__(AppRequestHandler)
            handler.directory = str(directory)
            handler.path = "/outside.csv"
            handler.send_error = Mock()
            self.assertIsNone(handler.send_head())
            handler.send_error.assert_called_once_with(403, "Files outside the saved app are unavailable")

    def test_directory_index_cannot_bypass_symlink_check(self):
        with tempfile.TemporaryDirectory() as root:
            directory = self.saved_app(root)
            raw = Path(root) / "raw.csv"
            raw.write_text("private source data")
            (directory / "index.html").unlink()
            (directory / "index.html").symlink_to(raw)
            handler = object.__new__(AppRequestHandler)
            handler.directory = str(directory)
            handler.path = "/"
            handler.send_error = Mock()
            self.assertIsNone(handler.send_head())
            handler.send_error.assert_called_once_with(403, "Files outside the saved app are unavailable")

    def test_server_binds_only_loopback_and_port_conflict_is_actionable(self):
        with tempfile.TemporaryDirectory() as root:
            self.saved_app(root)
            output = StringIO()
            with patch("scripts.serve_app.ThreadingHTTPServer", side_effect=OSError(errno.EADDRINUSE, "in use")) as server:
                with redirect_stderr(output):
                    self.assertEqual(main(["--no-browser"], project_root=root), 1)
            self.assertEqual(server.call_args.args[0], ("127.0.0.1", 8050))
            self.assertIn("--port 8051", output.getvalue())


if __name__ == "__main__":
    unittest.main()
