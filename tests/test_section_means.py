"""Fictional arithmetic and explicit empty-bin conventions; no actual run."""
import unittest

import numpy as np

from comet_spatial.section_means import summarize_section_means


def fixture():
    sections = []
    for arm in ("HK1", "PFKP"):
        for condition, values in (("Homecage", (3, 5, 4)), ("Running", (7, 8, 9))):
            for i, value in enumerate(values):
                sid = arm + "_" + condition + str(i)
                sections.append({"section_id": sid, "physical_section_id": "physical_" + sid,
                    "animal_id": condition + str(i), "pla_type": arm, "condition": condition,
                    # Bin0: stated triples; bin1: no objects; bin2: ChAT-only.
                    "pla_counts": np.asarray([[value, 0, 0]]), "chat_counts": np.asarray([[0, 0, 1]])})
    return sections


class FixedSectionMeansTests(unittest.TestCase):
    def test_three_section_arithmetic_and_explicit_coverage_flags(self):
        result = summarize_section_means(fixture(), empty_bin_policy="zero")
        self.assertEqual(result["fixed_section_denominator"], 3)
        self.assertFalse(result["coverage_verified"])
        self.assertFalse(result["objects_are_biological_replicates"])
        for arm in result["arms"].values():
            self.assertEqual(arm["homecage_mean"][0, 0], 4)
            self.assertEqual(arm["running_mean"][0, 0], 8)
            self.assertEqual(arm["difference"][0, 0], 4)
            self.assertFalse(arm["tissue_coverage_known"].any())

    def test_all_empty_bins_are_assumed_zero_but_outside_union_display_domain(self):
        arm = summarize_section_means(fixture(), empty_bin_policy="zero")["arms"]["HK1"]
        self.assertEqual(arm["homecage_mean"][0, 1], 0)
        self.assertEqual(arm["difference"][0, 1], 0)
        self.assertEqual(arm["homecage_assumed_zero_section_n"][0, 1], 3)
        self.assertFalse(arm["displayable"][0, 1])
        self.assertTrue(np.isnan(arm["display_difference"][0, 1]))
        self.assertEqual(arm["homecage_assumed_zero_section_n"][0, 2], 0)
        self.assertTrue(arm["displayable"][0, 2])  # All three ChAT-only bins retain PLA0.

    def test_missing_policy_keeps_denominator_three_without_available_subset_reweighting(self):
        sections = fixture()
        sections[0]["pla_counts"][0, 0] = 0
        zero = summarize_section_means(sections, empty_bin_policy="zero")["arms"]["HK1"]
        missing = summarize_section_means(sections, empty_bin_policy="missing")["arms"]["HK1"]
        self.assertEqual(zero["homecage_mean"][0, 0], 3)  # (0+5+4)/3, never /2.
        self.assertEqual(zero["homecage_assumed_zero_section_n"][0, 0], 1)
        self.assertTrue(np.isnan(missing["homecage_mean"][0, 0]))
        self.assertTrue(np.isnan(missing["difference"][0, 0]))
        self.assertEqual(missing["section_denominator"], 3)
        self.assertEqual(missing["homecage_observed_section_n"][0, 0], 2)
        self.assertTrue(np.isnan(missing["homecage_mean"][0, 1]))
        self.assertEqual(missing["homecage_mean"][0, 2], 0)

    def test_condition_with_no_objects_can_compare_only_under_explicit_zero_policy(self):
        sections = fixture()
        for section in sections:
            if section["pla_type"] == "HK1" and section["condition"] == "Homecage":
                section["pla_counts"][0, 0] = 0
        zero = summarize_section_means(sections, empty_bin_policy="zero")["arms"]["HK1"]
        missing = summarize_section_means(sections, empty_bin_policy="missing")["arms"]["HK1"]
        self.assertEqual(zero["difference"][0, 0], 8)
        self.assertTrue(zero["observed_union"][0, 0])
        self.assertTrue(zero["displayable"][0, 0])
        self.assertFalse(missing["displayable"][0, 0])

    def test_arms_remain_separate_and_repeated_sections_or_animals_rejected(self):
        sections = fixture()
        for section in sections:
            if section["pla_type"] == "PFKP" and section["condition"] == "Running":
                section["pla_counts"][0, 0] = 1
        result = summarize_section_means(sections, empty_bin_policy="zero")
        self.assertEqual(result["arms"]["HK1"]["difference"][0, 0], 4)
        self.assertEqual(result["arms"]["PFKP"]["difference"][0, 0], -3)
        sections[1]["animal_id"] = sections[0]["animal_id"]
        with self.assertRaisesRegex(ValueError, "Repeated animal"):
            summarize_section_means(sections, empty_bin_policy="zero")

    def test_explicit_policy_and_exact_three_sections_required(self):
        with self.assertRaisesRegex(ValueError, "Explicit empty_bin_policy"):
            summarize_section_means(fixture(), empty_bin_policy="guess")
        with self.assertRaisesRegex(ValueError, "exactly 3"):
            summarize_section_means(fixture()[:-1], empty_bin_policy="zero")


if __name__ == "__main__":
    unittest.main()
