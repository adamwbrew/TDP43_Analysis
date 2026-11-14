#!/usr/bin/env python3
"""Open the saved COMET Explorer using only Python's standard library.

Run ``python3 scripts/serve_app.py`` from a checkout. Only ``outputs/app`` is
served, on this computer; raw inputs and the rest of the repository are outside
the server's document root. No analysis is rerun.
"""

import argparse
import errno
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys
import webbrowser


DEFAULT_PORT = 8050


def app_directory(project_root=None):
    """Find the saved viewer independently of the caller's working directory."""
    root = Path(project_root) if project_root is not None else Path(__file__).resolve().parents[1]
    directory = (root / "outputs" / "app").resolve()
    if not (directory / "index.html").is_file():
        raise FileNotFoundError(
            "The saved app is missing: %s\n"
            "Use the complete repository checkout or download the saved Explorer "
            "bundle described in README.md. Raw data are not needed to view it."
            % (directory / "index.html")
        )
    return directory


class AppRequestHandler(SimpleHTTPRequestHandler):
    """Serve the app without exposing outside files through symbolic links."""

    def send_head(self):
        candidate = Path(self.translate_path(self.path)).resolve()
        candidates = [candidate]
        if candidate.is_dir():
            candidates.extend(candidate / name for name in ("index.html", "index.htm"))
        for path in candidates:
            try:
                path.resolve().relative_to(Path(self.directory).resolve())
            except ValueError:
                self.send_error(403, "Files outside the saved app are unavailable")
                return None
        return super().send_head()

    def list_directory(self, path):
        self.send_error(404, "Directory listing is unavailable")
        return None


def port_number(value):
    try:
        port = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("Port must be an integer from 1 to 65535")
    if not 1 <= port <= 65535:
        raise argparse.ArgumentTypeError("Port must be an integer from 1 to 65535")
    return port


def main(argv=None, *, project_root=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=port_number, default=DEFAULT_PORT,
                        help="Local port (default: %(default)s)")
    parser.add_argument("--no-browser", action="store_true",
                        help="Print the address without opening a browser")
    args = parser.parse_args(argv)
    try:
        directory = app_directory(project_root)
    except FileNotFoundError as error:
        print(str(error), file=sys.stderr)
        return 1

    handler = partial(AppRequestHandler, directory=str(directory))
    try:
        server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    except OSError as error:
        if error.errno == errno.EADDRINUSE:
            print(
                "Port %s is already in use. If the Explorer is already running, "
                "open http://127.0.0.1:%s/. Otherwise choose another port:\n"
                "  python3 scripts/serve_app.py --port %s"
                % (args.port, args.port, 8051 if args.port == DEFAULT_PORT else DEFAULT_PORT),
                file=sys.stderr,
            )
        else:
            print("Could not start the local Explorer: %s" % error, file=sys.stderr)
        return 1

    address = "http://127.0.0.1:%s/" % server.server_port
    print("COMET Explorer: %s" % address, flush=True)
    print("Viewing saved results; no analysis is running. Keep this terminal open.")
    print("Press Ctrl+C to stop the local server.", flush=True)
    with server:
        if not args.no_browser:
            try:
                opened = webbrowser.open(address)
            except webbrowser.Error:
                opened = False
            if not opened:
                print("Open the address above in your browser.", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nExplorer server stopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
