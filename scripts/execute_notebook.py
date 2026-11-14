"""Execute with this Python, validate all outputs, then atomically save notebook."""
from pathlib import Path
import json
import os
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / "tmp/matplotlib"))
os.environ.setdefault("IPYTHONDIR", str(ROOT / "tmp/ipython"))
os.environ.setdefault("JUPYTER_RUNTIME_DIR", str(ROOT / "tmp/jupyter_runtime"))
import nbformat
from nbclient import NotebookClient
from jupyter_client.kernelspec import KernelSpecManager


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "TDP43_COMET_analysis.ipynb"
    notebook = nbformat.read(path, as_version=4)
    (ROOT / "tmp").mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir=ROOT / "tmp") as temp:
        kernel = Path(temp) / "tdp43-local"; kernel.mkdir()
        (kernel / "kernel.json").write_text(json.dumps({"argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"], "display_name": "TDP43 local", "language": "python"}))
        client = NotebookClient(notebook, timeout=600, kernel_name="tdp43-local", resources={"metadata": {"path": str(ROOT)}})
        client.km = client.create_kernel_manager()
        client.km.kernel_spec_manager = KernelSpecManager(kernel_dirs=[temp])
        client.execute()
    cells = [c for c in notebook.cells if c.cell_type == "code" and c.source.strip()]
    if not cells or any(c.execution_count is None for c in cells):
        raise RuntimeError("Some code cells did not execute")
    if any(o.output_type == "error" for c in cells for o in c.get("outputs", [])):
        raise RuntimeError("Notebook contains error outputs")
    nbformat.validate(notebook)
    temporary = path.with_suffix(".tmp.ipynb")
    nbformat.write(notebook, temporary)
    temporary.replace(path)
    validation_path = ROOT / "outputs/validation.json"
    if validation_path.exists():
        validation = json.loads(validation_path.read_text())
        validation["notebook_execution"] = "passed"
        validation["executed_code_cells"] = len(cells)
        validation["saved_notebook"] = str(path.resolve())
        validation_path.write_text(json.dumps(validation, indent=2) + "\n")
    print("Executed and validated %d code cells; saved %s" % (len(cells), path))


if __name__ == "__main__":
    main()
