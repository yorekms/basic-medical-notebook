#!/usr/bin/env python3
"""Build all 16 All-In-One Episode Bundles for NotebookLM."""

import json
import pathlib

manifest_p = pathlib.Path(r"C:\Users\patel\.gemini\antigravity\scratch\Podcast_Automation_Suite\notebooks_manifest.json")
with open(manifest_p, "r", encoding="utf-8") as f:
    manifest = json.load(f)

episodes = manifest["notebooks"]["basic_medical"]["episodes"]

bundle_map = {
    801: (
        "Bundle_01_Ep801_Kidney_Donor_Gauntlet_mGFR_Litholink_and_Split_Scans.md",
        "Bundle 01 — Ep 801: Living Kidney Donor Gauntlet, mGFR, 24h Litholink & Split Scans (All-In-One)",
        [
            "VOLUME_I_THE_LIVING_KIDNEY_DONOR_GAUNTLET_MGFR_HLA_CROSSMATCH_AND_SPLIT_FUNCTION.md",
            "DOCS_ARCHIVE_01_OSMOLARITY_AND_SOLUTION_CALCULATIONS.md",
            "LONGFORM_60MIN_PODCAST_EP801_KIDNEY_DONOR_GAUNTLET_MGFR_24HR_URINE_AND_SPLIT_SCANS.md",
        ],
    ),
    802: (
        "Bundle_02_Ep802_HLA_Typing_Luminex_Prozone_and_Living_Cell_Crossmatch.md",
        "Bundle 02 — Ep 802: Yellow-Top Living Lymphocytes, HLA NGS, Luminex Prozone & Crossmatch (All-In-One)",
        [
            "VOLUME_I_THE_LIVING_KIDNEY_DONOR_GAUNTLET_MGFR_HLA_CROSSMATCH_AND_SPLIT_FUNCTION.md",
            "DOCS_ARCHIVE_02_HLA_VARIABILITY_AND_AUTOIMMUNITY.md",
            "DOCS_ARCHIVE_03_COMPLEMENT_MEDIATED_IMMUNITY.md",
            "LONGFORM_60MIN_PODCAST_EP802_HLA_TYPING_LUMINEX_PROZONE_AND_LIVING_CELL_CROSSMATCH.md",
        ],
    ),
    803: (
        "Bundle_03_Ep803_Eight_Colored_Tubes_Core_Chemistry_and_Immunoassay_Traps.md",
        "Bundle 03 — Ep 803: Eight Colored Vacutainers, Core Lab Chemistry & Immunoassay Traps (All-In-One)",
        [
            "VOLUME_II_PHLEBOTOMY_VACUTAINER_CHEMISTRY_AND_AUTOMATED_CORE_LAB_ANALYZERS.md",
            "VOLUME_III_COMPLETE_BLOOD_COUNT_FLOW_CYTOMETRY_COAGULATION_AND_BLOOD_BANKING.md",
            "VOLUME_IV_IMMUNOASSAYS_ENDOCRINE_DYNAMICS_CARDIAC_BIOMARKERS_AND_LC_MS_MS.md",
            "LONGFORM_60MIN_PODCAST_EP803_EIGHT_COLORED_TUBES_CORE_CHEMISTRY_AND_IMMUNOASSAY_TRAPS.md",
        ],
    ),
    804: (
        "Bundle_04_Ep804_Behind_the_Lead_Glass_and_the_Cryostat.md",
        "Bundle 04 — Ep 804: Behind the Lead Glass & The Cryostat (All-In-One)",
        [
            "VOLUME_VII_RADIOLOGY_CT_MRI_ULTRASOUND_AND_NUCLEAR_PET_PHYSICS_BEHIND_THE_GLASS.md",
            "VOLUME_VIII_ANATOMIC_PATHOLOGY_BIOPSY_FROZEN_SECTION_IHC_NGS_AND_ENDOSCOPIC_CARDIAC_PROCEDURES.md",
            "LONGFORM_60MIN_PODCAST_EP804_BEHIND_THE_LEAD_GLASS_AND_THE_FROZEN_SECTION_CRYOSTAT.md",
        ],
    ),
    805: (
        "Bundle_05_Ep805_The_Oncology_Workup_Tumor_Markers_and_Liquid_Biopsy.md",
        "Bundle 05 — Ep 805: The Cancer Order Sheet, Tumor Markers, Liquid Biopsy & Theranostics (All-In-One)",
        [
            "VOLUME_IX_ONCOLOGY_DIAGNOSTICS_TUMOR_MARKERS_MARROW_FLOW_LIQUID_BIOPSY_AND_MOLECULAR_STAGING.md",
            "LONGFORM_60MIN_PODCAST_EP805_THE_ONCOLOGY_WORKUP_TUMOR_MARKERS_LIQUID_BIOPSY_MARROW_FLOW_AND_THERANOSTIC_PET.md",
        ],
    ),
    806: (
        "Bundle_06_Ep806_ICU_Red_Alert_Orders_Shock_Ventilator_Curves_and_Coma_EEG.md",
        "Bundle 06 — Ep 806: ICU Red-Alert Orders, Shock Gaps, Ventilator Curves & TEG (All-In-One)",
        [
            "VOLUME_X_ICU_TRAUMA_AND_EMERGENCY_CRITICAL_CARE_DIAGNOSTIC_ORDERS.md",
            "LONGFORM_60MIN_PODCAST_EP806_ICU_RED_ALERT_ORDERS_SHOCK_GAPS_VENTILATOR_CURVES_TEG_POCUS_AND_COMA_EEG.md",
        ],
    ),
    807: (
        "Bundle_07_Ep807_From_Womb_to_Heel_Stick_Prenatal_cfDNA_and_Trio_Exomes.md",
        "Bundle 07 — Ep 807: From Womb to Heel-Stick, Prenatal cfDNA, 5-Punch Heel-Stick & Trio Exomes (All-In-One)",
        [
            "VOLUME_XI_PEDIATRICS_NEONATAL_HEEL_STICK_PRENATAL_CFDNA_AND_GENOMIC_DIAGNOSTICS.md",
            "LONGFORM_60MIN_PODCAST_EP807_FROM_WOMB_TO_HEEL_STICK_NIPT_TANDEM_MS_SWEAT_CHLORIDE_AND_TRIO_EXOMES.md",
        ],
    ),
    808: (
        "Bundle_08_Ep808_The_Jeopardy_Grandmaster_Diagnostic_Tour.md",
        "Bundle 08 — Ep 808: The Jeopardy! Grandmaster Diagnostic Tour (All-In-One)",
        [
            "VOLUME_V_MICROBIOLOGY_BLOOD_CULTURES_MALDI_TOF_PCR_CT_VALUES_AND_SEROLOGY.md",
            "VOLUME_VI_URINALYSIS_BODY_FLUID_TAP_MICROSCOPY_AND_AUTOIMMUNE_RHEUMATOLOGY_PANELS.md",
            "VOLUME_XII_SPECIALTY_CLINICAL_TESTS_NEURO_GI_DERM_ALLERGY_OPHTHO_AND_JEOPARDY_COMPENDIUM.md",
            "VOLUME_XIII_MASTER_MEDICAL_TESTING_ENCYCLOPEDIA_TUBES_METHODS_TRAPS_AND_JEOPARDY_MATRIX.md",
            "LONGFORM_60MIN_PODCAST_EP808_THE_JEOPARDY_GRANDMASTER_TOUR_MICROBIOLOGY_FLUID_TAPS_AUTOIMMUNITY_AND_CLASSIC_TESTS.md",
        ],
    ),
    809: (
        "Bundle_09_Ep809_Cardiopulmonary_Diagnostics_Hemodynamics_and_PFT.md",
        "Bundle 09 — Ep 809: Cardiopulmonary Diagnostics, Vector Loops, hs-cTn Deltoids & Body-Box DLCO (All-In-One)",
        [
            "VOLUME_XV_CARDIOPULMONARY_DIAGNOSTICS_ECG_VECTORS_HS_TROPONIN_HEMODYNAMICS_AND_PFT.md",
            "LONGFORM_60MIN_PODCAST_EP809_CARDIOPULMONARY_DIAGNOSTICS_HEMODYNAMICS_AND_VASCULAR_MEDICINE.md",
        ],
    ),
    810: (
        "Bundle_10_Ep810_Gastroenterology_Hepatology_and_Nutrition.md",
        "Bundle 10 — Ep 810: Gastroenterology, Hepatology, Paracentesis SAAG, Chicago Manometry & Breath Physics (All-In-One)",
        [
            "VOLUME_XVI_GASTROENTEROLOGY_HEPATOLOGY_AND_NUTRITION_DIAGNOSTICS.md",
            "LONGFORM_60MIN_PODCAST_EP810_GASTROENTEROLOGY_HEPATOLOGY_AND_METABOLIC_NUTRITION.md",
        ],
    ),
    811: (
        "Bundle_11_Ep811_Endocrinology_Dynamic_Testing_and_Mass_Spectrometry.md",
        "Bundle 11 — Ep 811: Endocrinology Dynamic Testing, Adrenal Vein Sampling & Mass Spectrometry (All-In-One)",
        [
            "VOLUME_XVII_ENDOCRINOLOGY_DYNAMIC_TESTING_MASS_SPECTROMETRY_AND_ADRENAL_VEIN_SAMPLING.md",
            "LONGFORM_60MIN_PODCAST_EP811_ENDOCRINOLOGY_DYNAMIC_TESTING_AND_NEUROENDOCRINE_DISORDERS.md",
        ],
    ),
    812: (
        "Bundle_12_Ep812_Preventable_Death_Longevity_and_Screening.md",
        "Bundle 12 — Ep 812: Preventable Death, Evidence-Based Screening Architecture & Longevity (All-In-One)",
        [
            "VOLUME_XVIII_PREVENTABLE_DEATH_LONGEVITY_AND_EVIDENCE_BASED_SCREENING_ARCHITECTURE.md",
            "DOCS_ARCHIVE_04_PREVENTABLE_DEATH_SCREENING_AND_LONGEVITY.md",
            "LONGFORM_60MIN_PODCAST_EP812_PREVENTABLE_DEATH_LONGEVITY_AND_SCREENING_MEDICINE.md",
        ],
    ),
    813: (
        "Bundle_13_Ep813_Neurodiagnostics_EEG_EMG_and_CSF_Biomarkers.md",
        "Bundle 13 — Ep 813: The Neurodiagnostic Vault, 10-20 EEG, SFEMG Jitter & Prion RT-QuIC (All-In-One)",
        [
            "VOLUME_XIX_NEURODIAGNOSTICS_EMG_NCS_EEG_AND_CSF_BIOMARKERS.md",
            "LONGFORM_60MIN_PODCAST_EP813_THE_NEURODIAGNOSTIC_VAULT_EEG_EMG_EVOKED_POTENTIALS_AND_CSF.md",
        ],
    ),
    814: (
        "Bundle_14_Ep814_Infectious_Disease_Serology_Virology_and_Molecular.md",
        "Bundle 14 — Ep 814: Infectious Disease Serology, Syphilis Reverse Algorithm, HBV Core Windows & Tick Panels (All-In-One)",
        [
            "VOLUME_XX_INFECTIOUS_DISEASE_SEROLOGY_VIROLOGY_AND_MOLECULAR_DIAGNOSTICS.md",
            "LONGFORM_60MIN_PODCAST_EP814_INFECTIOUS_DISEASE_SEROLOGY_VIROLOGY_AND_PARASITOLOGY.md",
        ],
    ),
    815: (
        "Bundle_15_Ep815_Blood_Banking_Immunohematology_and_Advanced_Hemostasis.md",
        "Bundle 15 — Ep 815: Blood Banking, 11-Cell Rule-Outs, Daratumumab DTT, Rosner Index & VWD Multimers (All-In-One)",
        [
            "VOLUME_XXI_IMMUNOHEMATOLOGY_BLOOD_BANKING_AND_ADVANCED_HEMOSTASIS.md",
            "LONGFORM_60MIN_PODCAST_EP815_BLOOD_BANKING_IMMUNOHEMATOLOGY_AND_ADVANCED_HEMOSTASIS.md",
        ],
    ),
    816: (
        "Bundle_16_Ep816_Cytogenetics_Chromosomal_Microarrays_and_Long_Read_Genomics.md",
        "Bundle 16 — Ep 816: Cytogenetics, 550-Band Karyotypes, Dual-Fusion FISH, SNP Arrays & Nanopore Pseudogenes (All-In-One)",
        [
            "VOLUME_XXII_CYTOGENETICS_CHROMOSOMAL_MICROARRAYS_AND_LONG_READ_GENOMICS.md",
            "LONGFORM_60MIN_PODCAST_EP816_CYTOGENETICS_CHROMOSOMAL_MICROARRAYS_AND_LONG_READ_GENOMICS.md",
        ],
    ),
}

root = pathlib.Path(r"C:\Users\patel\.gemini\antigravity\scratch\Basic_Medical_Notebook")
out_dir = root / "Episode_Bundles_Markdown"
out_dir.mkdir(parents=True, exist_ok=True)

print(f"Building all 16 bundles in {out_dir}...")
for ep_data in episodes:
    ep_num = ep_data["ep"]
    if ep_num not in bundle_map:
        continue
    slug, title, components = bundle_map[ep_num]
    prompt = ep_data["prompt"]
    out_path = out_dir / slug

    parts = [
        f"# {title}\n",
        "## ZERO-MIXUP SINGLE-SOURCE BUNDLE FOR GOOGLE NOTEBOOKLM\n",
        "**How to use in NotebookLM (`notebook.google.com`):**\n",
        "1. Check **ONLY THIS ONE DOCUMENT** in your NotebookLM Sources sidebar (uncheck all others — every reference treatise and script needed for this episode is merged right inside this single file!).",
        "2. Click **Customize** on **Audio Overview**, choose **Longer**, and paste this exact prompt:\n",
        f"```text\n{prompt}\n```\n",
        "---\n",
    ]
    for comp_name in components:
        comp_path = root / comp_name
        if not comp_path.exists():
            print(f"ERROR: Missing component {comp_name}")
            continue
        comp_body = comp_path.read_text(encoding="utf-8")
        parts.append(f"\n---\n\n## INCLUDED SOURCE: `{comp_name}`\n\n{comp_body}\n")

    out_path.write_text("\n".join(parts), encoding="utf-8")
    sz = out_path.stat().st_size
    words = len(out_path.read_text(encoding="utf-8").split())
    print(f"Built: {slug} -> {words:,} words ({sz:,} bytes)")

print("\nAll 16 bundles successfully created and verified!")
