"""Prepared fixed-denominator section means with an explicit empty-bin policy.

On 14 November 2026 the scientist explicitly selected averaging all three
sections while treating empty section-bins as zero, with uncertain coverage.
The caller records that choice by passing ``empty_bin_policy="zero"``.
Observed section N remains diagnostic and never becomes its denominator.

This pure module does not run an experiment, choose the policy, create masks,
fit alignment, or alter saved exploratory results. Counts must already share
one grid. Object support remains distinct from known tissue coverage.
"""
import numpy as np


def summarize_section_means(sections, *, empty_bin_policy, sections_per_condition=3):
    """Average all specified sections equally, keeping the denominator fixed.

    ``zero`` treats every section-bin with no exported PLA/ChAT as an assumed
    zero PLA count, rather than as established tissue-covered zero. ``missing``
    keeps the denominator fixed but reports a condition mean only where every
    section has observed objects. It never reweights the available subset.

    The per-arm union of observed objects supplies a common display domain for
    the two conditions. Raw arithmetic zeros outside that union remain in
    ``difference`` under the zero policy; ``display_difference`` masks them.
    This display rule is not a tissue mask. ``common_observed_union`` is the
    all-arm union for viewport bookkeeping, not cross-arm anatomy or coverage.
    """
    if empty_bin_policy not in ("zero", "missing"):
        raise ValueError("Explicit empty_bin_policy must be 'zero' or 'missing'")
    if not isinstance(sections_per_condition, int) or isinstance(sections_per_condition, bool) or sections_per_condition <= 0:
        raise ValueError("sections_per_condition must be a positive integer")
    sections = list(sections)
    if not sections:
        raise ValueError("Section-level raw counts are required")
    shape = None
    seen, physical, animal_conditions = set(), set(), {}
    for section in sections:
        for key in ("section_id", "physical_section_id", "animal_id"):
            if not isinstance(section.get(key), str) or not section[key].strip():
                raise ValueError("Explicit section, physical-section and animal identities are required")
        if section["section_id"] in seen:
            raise ValueError("Repeated section ID")
        seen.add(section["section_id"])
        arm, condition = section.get("pla_type"), section.get("condition")
        if arm not in ("HK1", "PFKP") or condition not in ("Homecage", "Running"):
            raise ValueError("Canonical separate PLA arm and condition are required")
        key = (section["physical_section_id"], arm)
        if key in physical:
            raise ValueError("Repeated physical section/PLA type cannot increase sample size")
        physical.add(key)
        animal = section["animal_id"]
        if animal in animal_conditions and animal_conditions[animal] != condition:
            raise ValueError("Conflicting condition assignments for an animal")
        animal_conditions[animal] = condition
        for key in ("pla_counts", "chat_counts"):
            values = np.asarray(section[key])
            if (values.ndim != 2 or not np.issubdtype(values.dtype, np.number) or
                    not np.isfinite(values).all() or (values < 0).any() or
                    not np.equal(values, np.floor(values)).all()):
                raise ValueError("Finite nonnegative raw count matrices are required")
            if shape is None:
                shape = values.shape
            if values.shape != shape:
                raise ValueError("Every section must use the same recorded grid")
        observed = np.asarray(section["pla_counts"]) + np.asarray(section["chat_counts"]) > 0
        if "observed_support" in section and not np.array_equal(section["observed_support"], observed):
            raise ValueError("Supplied observed support disagrees with raw PLA/ChAT counts")
    arms, common_union = {}, np.zeros(shape, dtype=bool)
    for arm in ("HK1", "PFKP"):
        part = [section for section in sections if section["pla_type"] == arm]
        means, ns, sums, complete, ids, animals = {}, {}, {}, {}, {}, {}
        union = np.zeros(shape, dtype=bool)
        for condition in ("Homecage", "Running"):
            group = [section for section in part if section["condition"] == condition]
            if len(group) != sections_per_condition:
                raise ValueError("%s %s requires exactly %d distinct physical sections" % (arm, condition, sections_per_condition))
            if len({section["animal_id"] for section in group}) != sections_per_condition:
                raise ValueError("Repeated animal within one arm/condition is not independent replication")
            total = np.zeros(shape, dtype=float)
            n = np.zeros(shape, dtype=np.int64)
            for section in group:
                pla, chat = np.asarray(section["pla_counts"]), np.asarray(section["chat_counts"])
                observed = pla + chat > 0
                total += pla
                n += observed
                union |= observed
            full = n == sections_per_condition
            raw_mean = total / sections_per_condition
            means[condition] = raw_mean if empty_bin_policy == "zero" else np.where(full, raw_mean, np.nan)
            ns[condition], sums[condition], complete[condition] = n, total, full
            ids[condition] = [section["section_id"] for section in group]
            animals[condition] = [section["animal_id"] for section in group]
        difference = means["Running"] - means["Homecage"]
        displayable = union & np.isfinite(difference)
        arms[arm] = {
            "homecage_mean": means["Homecage"], "running_mean": means["Running"],
            "difference": difference, "display_difference": np.where(displayable, difference, np.nan),
            "homecage_count_sum": sums["Homecage"], "running_count_sum": sums["Running"],
            "homecage_observed_section_n": ns["Homecage"], "running_observed_section_n": ns["Running"],
            "homecage_complete_observed_support": complete["Homecage"],
            "running_complete_observed_support": complete["Running"],
            "homecage_assumed_zero_section_n": sections_per_condition - ns["Homecage"] if empty_bin_policy == "zero" else np.zeros(shape, dtype=np.int64),
            "running_assumed_zero_section_n": sections_per_condition - ns["Running"] if empty_bin_policy == "zero" else np.zeros(shape, dtype=np.int64),
            "observed_union": union, "displayable": displayable,
            "tissue_coverage_known": np.zeros(shape, dtype=bool),
            "section_denominator": sections_per_condition, "section_ids": ids, "animal_ids": animals,
        }
        common_union |= union
    return {
        "empty_bin_policy": empty_bin_policy, "fixed_section_denominator": sections_per_condition,
        "arms": arms, "common_observed_union": common_union,
        "coverage_verified": False, "coverage_status": "unknown; no tissue mask used or inferred",
        "biological_experimental_unit": "animal", "averaging_unit": "physical section",
        "objects_are_biological_replicates": False, "inferential_tests_performed": False,
        "display_domain_meaning": "Per-arm union of exported PLA/ChAT support across both conditions; never full tissue coverage",
    }
