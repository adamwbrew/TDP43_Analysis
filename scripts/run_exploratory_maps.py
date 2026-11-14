#!/usr/bin/env python3
"""Run explicitly authorized exploratory object-support maps; strict results stay pending."""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from comet_spatial.exploratory import run_exploratory_maps


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=ROOT / "metadata/analysis_manifest.json")
    parser.add_argument("--authorization", type=Path, default=ROOT / "metadata/exploratory_authorization.json")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "outputs/exploratory")
    args = parser.parse_args(argv)
    try:
        destination = run_exploratory_maps(args.manifest.resolve(), args.authorization.resolve(), args.output_dir.resolve())
    except (OSError, KeyError, TypeError, ValueError) as exc:
        print("EXPLORATORY RUN BLOCKED: " + str(exc))
        return 2
    print("EXPLORATORY RUN COMPLETE: " + str(destination))
    print("Strict PDF results remain pending; observed-object support is not tissue coverage.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
