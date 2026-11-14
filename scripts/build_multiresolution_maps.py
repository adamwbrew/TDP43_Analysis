#!/usr/bin/env python3
"""Fresh 1000/500/250/100-unit exploratory bins and full PLA point detail."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from comet_spatial.multiresolution import build_multiresolution_maps


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=ROOT / "metadata/analysis_manifest.json")
    parser.add_argument("--authorization", type=Path, default=ROOT / "metadata/exploratory_authorization.json")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "outputs/exploratory_multiresolution")
    parser.add_argument("--baseline-run", type=Path)
    args = parser.parse_args(argv)
    baseline = args.baseline_run
    if baseline is None and (ROOT / "outputs/exploratory/latest_run.json").exists():
        baseline = Path(json.loads((ROOT / "outputs/exploratory/latest_run.json").read_text())["run_directory"])
    try:
        directory = build_multiresolution_maps(args.manifest.resolve(), args.authorization.resolve(), args.output_dir.resolve(),
                                              baseline_directory=baseline)
    except (OSError, KeyError, TypeError, ValueError) as exc:
        print("MULTIRESOLUTION RUN BLOCKED: " + str(exc))
        return 2
    print("EXPLORATORY MULTIRESOLUTION RUN COMPLETE: " + str(directory))
    print("Every PLA point retained. Strict PDF results remain pending.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
