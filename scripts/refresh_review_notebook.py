"""Execute just the self-contained presentation cell; retain validated raw outputs."""
from pathlib import Path
import json
import os
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / "tmp/matplotlib"))
os.environ.setdefault("IPYTHONDIR", str(ROOT / "tmp/ipython"))
os.environ.setdefault("JUPYTER_RUNTIME_DIR", str(ROOT / "tmp/jupyter_runtime"))
import nbformat
from nbclient import NotebookClient
from jupyter_client.kernelspec import KernelSpecManager
from scripts.build_notebook import review_cells


def main():
    path = ROOT / "TDP43_COMET_analysis.ipynb"
    original = nbformat.read(path, as_version=4)
    cells = review_cells()
    mini = nbformat.v4.new_notebook(cells=cells)
    with tempfile.TemporaryDirectory(dir=ROOT / "tmp") as temp:
        kernel = Path(temp) / "tdp43-local"; kernel.mkdir()
        (kernel / "kernel.json").write_text(json.dumps({"argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"], "display_name": "TDP43 local", "language": "python"}))
        client = NotebookClient(mini, timeout=300, kernel_name="tdp43-local", resources={"metadata": {"path": str(ROOT)}})
        client.km = client.create_kernel_manager()
        client.km.kernel_spec_manager = KernelSpecManager(kernel_dirs=[temp])
        client.execute()
    if mini.cells[1].execution_count is None or any(o.output_type == "error" for o in mini.cells[1].get("outputs", [])):
        raise RuntimeError("Presentation cell execution failed")
    # A second refresh replaces only this self-contained section, never raw cells.
    heading = cells[0].source.splitlines()[0]
    start = next((i for i,c in enumerate(original.cells) if c.cell_type == 'markdown' and c.source.startswith(heading)), None)
    if start is not None:
        original.cells[start:start+2] = mini.cells
    else:
        position = next(i for i,c in enumerate(original.cells) if c.cell_type == 'markdown' and c.source.startswith('## Strict PDF results'))
        original.cells[position:position] = mini.cells
    for cell in original.cells:
        if cell.cell_type == 'markdown' and 'The scientist-ready request remains' in cell.source:
            first, rest = cell.source.split('The scientist-ready request remains', 1)
            _, after = rest.split('\n\n', 1)
            cell.source = first + 'The scientist-facing checklist contains eight plain-language questions about the experiment and existing records in `docs/scientist_questions.md`. Technical conversion, coordinate mapping and code validation are work for the analysis team with the imaging analyst; see `docs/technical_handoff_requirements.md`.\n\n' + after
    original.metadata['review_presentation_refresh'] = {'scope': 'One self-contained cached-data presentation cell executed; prior raw-analysis outputs preserved.', 'raw_recomputed_this_refresh': False}
    nbformat.validate(original)
    temporary = path.with_suffix('.tmp.ipynb')
    nbformat.write(original, temporary); temporary.replace(path)
    print('Saved three new review figures in one executed presentation cell; prior raw results preserved.')


if __name__ == '__main__':
    main()
