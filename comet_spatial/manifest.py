"""Fail-closed scientific metadata and immutable-input provenance preflight.

This is a documentary schema, not an automatic anatomy/identity validator.
The supplied documents must identify the accepted alignment and existing masks.
Passing these checks establishes documented authority, file integrity, and internal
consistency; it does not establish anatomical validity by itself.
"""
import hashlib
import json
from datetime import datetime
from pathlib import Path

from .core import FixedTransform, GridSpec


CONFIRMATIONS = (
    "sample_relationships", "centroid_measurements", "existing_tissue_masks",
    "existing_fixed_alignment", "duplicate_resolution", "grid_definition",
)


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def empty_manifest():
    """Undocumented empty intake template; it blocks rather than creates maps.

    See section_template() for required per-section fields. Do not fill these
    fields from filenames or historical animal assignments.
    """
    return {
        "schema_version": 1,
        "approval": {"status": "undocumented", "documented_by": None, "documented_at": None,
                     "evidence": {"path": None, "sha256": None}},
        "confirmations": {key: {"confirmed": False, "evidence": None} for key in CONFIRMATIONS},
        "study": {"biological_experimental_unit": "animal",
                  "descriptive_averaging_unit": "physical_tissue_section",
                  "section_weighting": "equal", "scientific_question": None},
        "grid": {"x_edges": None, "y_edges": None, "coordinate_units": None,
                 "reference_space": None, "orientation": {"x_positive": None, "y_positive": None,
                                                             "display_x_increases_to": None,
                                                             "display_y_increases_to": None},
                 "provenance": None},
        "alignment_reference": {"path": None, "sha256": None, "figure_id": None},
        "source_relationships": [],
        "sections": [],
    }


def section_template():
    return {
        "section_id": None, "physical_section_id": None, "animal_id": None,
        "condition": None, "pla_type": None,
        "source": {"path": None, "sha256": None, "source_file_id": None,
                   "format": "csv", "coordinate_units": None,
                   "object_id_column": None, "centroid_x_column": None, "centroid_y_column": None,
                   "centroid_definition": {"kind": "measured_centroid", "confirmed": False,
                                           "evidence": None},
                   "pla_object_type": {"kind": None, "classification_column": None,
                                       "accepted_values": None, "evidence": None},
                   "object_selection": {"mode": "all_rows"},
                   "basis": "consolidated_object_measurements"},
        "mask": {"path": None, "sha256": None, "format": None,
                 "coordinate_space": None, "coordinate_units": None,
                 "reference_space": None,
                 "basis": "existing_tissue_mask"},
        "transform": {"matrix": None, "accepted": False, "approved_by": None,
                      "native_units": None, "aligned_units": None,
                      "reference_space": None,
                      "evidence": {"path": None, "sha256": None}},
    }


def load_manifest(path):
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def grid_from_manifest(manifest):
    value = manifest["grid"]
    return GridSpec(value["x_edges"], value["y_edges"], value["coordinate_units"],
                    value["reference_space"], value["orientation"]["x_positive"],
                    value["orientation"]["y_positive"])


def display_directions_from_manifest(manifest):
    """Require explicit screen direction; anatomical names never imply a flip.

    Legacy x_positive='right'/'left' and y_positive='up'/'down' are literal
    display directions and may be used directly. Terms such as dorsal/ventral
    require separate preserved display_x/y_increases_to metadata.
    """
    orientation = manifest["grid"]["orientation"]
    xdir = orientation.get("display_x_increases_to")
    ydir = orientation.get("display_y_increases_to")
    if xdir is None and orientation.get("x_positive") in ("right", "left"):
        xdir = orientation["x_positive"]
    if ydir is None and orientation.get("y_positive") in ("up", "down"):
        ydir = orientation["y_positive"]
    if xdir not in ("right", "left") or ydir not in ("up", "down"):
        raise ValueError("Preserved display orientation requires display_x_increases_to='right'/'left' "
                         "and display_y_increases_to='up'/'down'; anatomical terms alone are insufficient")
    return xdir, ydir


def validate_manifest(manifest, base_dir):
    """Return {status, blockers, checks}, checking assets and their SHA-256 hashes.

    This read-only check never approves anatomy, fits transforms, creates masks,
    derives centroids, or resolves repeated exports. All asset paths are relative
    to base_dir unless absolute; input files are never copied or altered here.
    """
    blockers, checks = [], []
    base_dir = Path(base_dir)
    if not isinstance(manifest, dict):
        return {"status": "blocked", "blockers": ["Manifest must be a JSON object"], "checks": []}

    def required(value, label):
        ok = isinstance(value, str) and bool(value.strip())
        if not ok:
            blockers.append(label + " must be explicitly supplied")
        return ok

    checked_assets = {}

    def asset(value, label):
        if not isinstance(value, dict):
            blockers.append(label + " must include path and SHA-256")
            return None
        raw_path, expected = value.get("path"), value.get("sha256")
        valid_path = required(raw_path, label + ".path")
        valid_hash = (isinstance(expected, str) and len(expected) == 64 and
                      all(c in "0123456789abcdef" for c in expected))
        if not valid_hash:
            blockers.append(label + ".sha256 must be a lowercase 64-character digest")
        if not valid_path:
            return None
        path = Path(raw_path)
        path = path if path.is_absolute() else base_dir / path
        if not path.is_file():
            blockers.append(label + " is missing: " + str(path))
            return None
        if valid_hash:
            try:
                cache_key = str(path.resolve())
                if cache_key not in checked_assets:
                    checked_assets[cache_key] = sha256_file(path)
                actual = checked_assets[cache_key]
            except OSError as exc:
                blockers.append(label + " is unreadable: " + str(exc))
                return None
            if actual != expected:
                blockers.append(label + " SHA-256 mismatch")
                return None
            checks.append(label + " exists and SHA-256 matches")
        return path

    if manifest.get("schema_version") != 1:
        blockers.append("schema_version must equal 1")
    approval = manifest.get("approval") or {}
    if approval.get("status") not in ("documented", "scientist_approved"):
        blockers.append("Authoritative metadata sources are not documented")
    required(approval.get("documented_by", approval.get("approved_by")), "approval.documented_by")
    documented_at = approval.get("documented_at", approval.get("approved_at"))
    if required(documented_at, "approval.documented_at"):
        try:
            datetime.fromisoformat(documented_at.replace("Z", "+00:00"))
        except ValueError:
            blockers.append("approval.documented_at must be ISO-8601")
    asset(approval.get("evidence"), "approval.evidence")
    confirmations = manifest.get("confirmations") or {}
    for key in CONFIRMATIONS:
        item = confirmations.get(key) or {}
        if item.get("confirmed") is not True:
            blockers.append("Confirmation missing: " + key)
        required(item.get("evidence"), "confirmations." + key + ".evidence")
    study = manifest.get("study") or {}
    for key, expected in (("biological_experimental_unit", "animal"),
                          ("descriptive_averaging_unit", "physical_tissue_section"),
                          ("section_weighting", "equal")):
        if study.get(key) != expected:
            blockers.append("study.%s must be %s for this initial workflow" % (key, expected))
    required(study.get("scientific_question"), "study.scientific_question")
    grid = None
    try:
        grid = grid_from_manifest(manifest)
        required(manifest["grid"].get("provenance"), "grid.provenance")
    except (KeyError, TypeError, ValueError) as exc:
        blockers.append("Shared grid, coordinate units and orientation are unresolved: " + str(exc))
    try:
        display_directions_from_manifest(manifest)
    except (KeyError, TypeError, ValueError) as exc:
        blockers.append("Display orientation is unresolved: " + str(exc))
    asset(manifest.get("alignment_reference"), "alignment_reference")
    required((manifest.get("alignment_reference") or {}).get("figure_id"), "alignment_reference.figure_id")

    sections = manifest.get("sections")
    if not isinstance(sections, list) or not sections:
        blockers.append("No confirmed section metadata supplied")
        sections = []
    seen_sections, seen_physical, seen_selection = set(), set(), set()
    selections_by_hash = {}
    animal_conditions, physical_animals, source_ids, declared_hashes = {}, {}, set(), {}
    for i, section in enumerate(sections):
        label = "sections[%d]" % i
        if not isinstance(section, dict):
            blockers.append(label + " must be an object")
            continue
        for field in ("section_id", "physical_section_id", "animal_id"):
            required(section.get(field), label + "." + field)
        sid = section.get("section_id")
        if sid in seen_sections:
            blockers.append("Repeated section_id: " + str(sid))
        seen_sections.add(sid)
        physical = (section.get("physical_section_id"), section.get("pla_type"))
        if physical in seen_physical:
            blockers.append("Physical section/PLA type would be counted twice: " + str(physical))
        seen_physical.add(physical)
        if section.get("condition") not in ("Homecage", "Running"):
            blockers.append(label + ".condition must be confirmed Homecage or Running")
        if section.get("pla_type") not in ("HK1", "PFKP"):
            blockers.append(label + ".pla_type must be confirmed HK1 or PFKP")
        aid = section.get("animal_id")
        physical_id = section.get("physical_section_id")
        if physical_id in physical_animals and physical_animals[physical_id] != aid:
            blockers.append("A physical section is assigned to different animals: " + str(physical_id))
        physical_animals[physical_id] = aid
        if aid in animal_conditions and animal_conditions[aid] != section.get("condition"):
            blockers.append("Conflicting condition assignments for animal " + str(aid))
        animal_conditions[aid] = section.get("condition")

        source, mask, transform = (section.get("source") or {}, section.get("mask") or {},
                                   section.get("transform") or {})
        asset(source, label + ".source")
        for field in ("source_file_id", "coordinate_units", "object_id_column", "centroid_x_column", "centroid_y_column"):
            required(source.get(field), label + ".source." + field)
        source_ids.add(source.get("source_file_id"))
        if source.get("source_file_id") in declared_hashes and declared_hashes[source.get("source_file_id")] != source.get("sha256"):
            blockers.append("A source_file_id refers to different input hashes")
        declared_hashes[source.get("source_file_id")] = source.get("sha256")
        if source.get("format") != "csv" or source.get("basis") != "consolidated_object_measurements":
            blockers.append(label + ": analytical source must be object-level CSV, not summary plots")
        pla_objects = source.get("pla_object_type") or {}
        if not isinstance(pla_objects, dict):
            blockers.append(label + ": source.pla_object_type must be an explicit documentary object")
            pla_objects = {}
        required(pla_objects.get("evidence"), label + ".source.pla_object_type.evidence")
        if pla_objects.get("kind") not in ("classified_mixed_source", "documented_pla_only"):
            blockers.append(label + ": source.pla_object_type must declare classified_mixed_source or documented_pla_only")
        if pla_objects.get("kind") == "classified_mixed_source":
            required(pla_objects.get("classification_column"), label + ".source.pla_object_type.classification_column")
            accepted_values = pla_objects.get("accepted_values")
            if (not isinstance(accepted_values, list) or not accepted_values or
                    not all(isinstance(value, str) and value.strip() for value in accepted_values) or
                    (isinstance(accepted_values, list) and len(set(str(v) for v in accepted_values)) != len(accepted_values))):
                blockers.append(label + ": source.pla_object_type.accepted_values must contain unique exact PLA class strings")
        elif pla_objects.get("kind") == "documented_pla_only":
            # Known class-bearing files must be checked against declared labels;
            # this declaration is reserved for documented PLA-only exports with
            # no classification field. The runner verifies the actual header.
            if pla_objects.get("classification_column") is not None or pla_objects.get("accepted_values") is not None:
                blockers.append(label + ": documented_pla_only cannot bypass an existing classification declaration")
        centroid = source.get("centroid_definition") or {}
        if centroid.get("confirmed") is not True:
            blockers.append(label + ": centroid measurement definition is unconfirmed")
        required(centroid.get("evidence"), label + ".source.centroid_definition.evidence")
        if centroid.get("kind") != "measured_centroid":
            if centroid.get("kind") != "approved_proxy":
                blockers.append(label + ": measured centroid or explicitly amended approved proxy required")
            else:
                asset(centroid.get("approved_amendment"), label + ".source.centroid_definition.approved_amendment")
        selection = source.get("object_selection") or {}
        if selection.get("mode") not in ("all_rows", "column_equals"):
            blockers.append(label + ": explicit object selection required")
        if selection.get("mode") == "column_equals":
            predicates = selection.get("predicates")
            if not isinstance(predicates, dict) or not predicates or not all(isinstance(k, str) and k for k in predicates):
                blockers.append(label + ": column_equals selection requires explicit predicates mapping")
        selected_key = (source.get("sha256"), json.dumps(selection, sort_keys=True))
        if selected_key in seen_selection:
            blockers.append(label + ": identical source/selection would be counted more than once")
        # On a shared consolidated source, two exact-value selectors are provably
        # disjoint only when they disagree on at least one common column. An
        # all_rows selector overlaps every selector. Unknown overlap is blocked.
        predicates = selection.get("predicates") if selection.get("mode") == "column_equals" else {}
        predicates = predicates if isinstance(predicates, dict) else {}
        for prior in selections_by_hash.get(source.get("sha256"), []):
            mutually_exclusive = any(prior[key] != predicates[key] for key in prior.keys() & predicates.keys())
            if not mutually_exclusive:
                blockers.append(label + ": selectors on the same input may overlap; explicit disjoint section/PLA selection required")
        selections_by_hash.setdefault(source.get("sha256"), []).append(predicates)
        seen_selection.add(selected_key)
        asset(mask, label + ".mask")
        if mask.get("format") not in ("geojson", "raster_npz"):
            blockers.append(label + ": existing mask format must be geojson or raster_npz")
        if mask.get("basis") != "existing_tissue_mask":
            blockers.append(label + ": tissue must use an existing mask, never PLA-derived support")
        if mask.get("coordinate_space") not in ("native", "aligned"):
            blockers.append(label + ": mask coordinate_space must be native or aligned")
        required(mask.get("coordinate_units"), label + ".mask.coordinate_units")
        if transform.get("accepted") is not True:
            blockers.append(label + ": pre-existing accepted fixed transform is missing")
        required(transform.get("approved_by"), label + ".transform.approved_by")
        for field in ("native_units", "aligned_units"):
            required(transform.get(field), label + ".transform." + field)
        required(transform.get("reference_space"), label + ".transform.reference_space")
        asset(transform.get("evidence"), label + ".transform.evidence")
        try:
            FixedTransform(transform.get("matrix"))
        except (TypeError, ValueError) as exc:
            blockers.append(label + ": invalid fixed transform: " + str(exc))
        if source.get("coordinate_units") != transform.get("native_units"):
            blockers.append(label + ": centroid units disagree with supplied transform native units")
        if grid and transform.get("aligned_units") != grid.coordinate_units:
            blockers.append(label + ": transform aligned units disagree with shared grid")
        if grid and transform.get("reference_space") != grid.reference_space:
            blockers.append(label + ": transform reference space disagrees with shared grid")
        expected_mask_units = (transform.get("native_units") if mask.get("coordinate_space") == "native"
                               else transform.get("aligned_units"))
        if mask.get("coordinate_units") != expected_mask_units:
            blockers.append(label + ": mask units disagree with declared coordinate space")
        if mask.get("coordinate_space") == "aligned" and grid and mask.get("reference_space") != grid.reference_space:
            blockers.append(label + ": aligned mask reference space disagrees with shared grid")

    relations = manifest.get("source_relationships")
    if not isinstance(relations, list) or not relations:
        blockers.append("Explicit source_relationships audit of primary/repeated/superseded files is required")
        relations = []
    audited, relation_ids = set(), set()
    for i, rel in enumerate(relations):
        label = "source_relationships[%d]" % i
        if not isinstance(rel, dict):
            blockers.append(label + " must be an object")
            continue
        source_id = rel.get("source_file_id")
        required(source_id, label + ".source_file_id")
        if source_id in relation_ids:
            blockers.append("Repeated source relationship ID: " + str(source_id))
        relation_ids.add(source_id)
        relationship = rel.get("relationship")
        if relationship not in ("primary", "independent", "superseded", "duplicate"):
            blockers.append(label + ": explicit source relationship required")
        if not isinstance(rel.get("included"), bool):
            blockers.append(label + ".included must be boolean")
        required(rel.get("evidence"), label + ".evidence")
        if relationship in ("superseded", "duplicate"):
            if rel.get("included") is not False:
                blockers.append(label + ": repeated/superseded source cannot enter primary counts")
            required(rel.get("primary_source_file_id"), label + ".primary_source_file_id")
        if rel.get("included") is True:
            audited.add(source_id)
            if source_id not in source_ids:
                blockers.append(label + ": included source has no section mapping")
    for missing in sorted(str(x) for x in source_ids - audited):
        blockers.append("Included source lacks a confirmed relationship audit: " + missing)
    for arm in ("HK1", "PFKP"):
        for condition in ("Homecage", "Running"):
            if not any(s.get("pla_type") == arm and s.get("condition") == condition
                       for s in sections if isinstance(s, dict)):
                blockers.append("No confirmed %s %s section" % (arm, condition))
    return {"status": "ready" if not blockers else "blocked", "blockers": blockers,
            "checks": checks, "schema_version": 1}


def preflight_manifest(path):
    path = Path(path)
    try:
        return validate_manifest(load_manifest(path), path.parent)
    except (OSError, ValueError, TypeError) as exc:
        return {"status": "blocked", "blockers": ["Cannot read manifest: " + str(exc)], "checks": []}
