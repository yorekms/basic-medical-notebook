#!/usr/bin/env python3
"""Sync Season 2 Basic Medical volumes, scripts, and bundles to Google Drive."""

import json
import pathlib
import re
import shutil
import subprocess
import sys
from typing import Dict, List

ROOT_FOLDER_ID = "1KmlsWV495OKHpvhCqoG0nMH_zkH9k0rS"
PICKER_FOLDER_ID = "1WAj6DP_C8wlB3xnfrKa9VuGdnBMLOabi"
BUNDLES_FOLDER_ID = "1FLCOLKL2hPj6VIwfsCV6IKOjS-ewLBd9"
EXISTING_INDEX_GDOC_ID = "1V5jsPNLKfQ6lfBLeoo-yNzz_AS2I1ChJ8TmWl8kupfw"

UPLOAD_ID_RE = re.compile(r"\(ID:\s*([A-Za-z0-9_-]+)\)")


def run_gdrive(args: List[str]) -> str:
    gdrive_bin = shutil.which("gdrive")
    if not gdrive_bin:
        raise RuntimeError("gdrive executable not found on PATH")
    proc = subprocess.run(
        [gdrive_bin] + args,
        capture_output=True,
        text=True,
        encoding="utf-8",
        shell=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"gdrive error ({proc.returncode}): {' '.join(args)}\n{proc.stdout}\n{proc.stderr}"
        )
    return proc.stdout.strip()


def upload_file(local_path: pathlib.Path, parent_id: str, mime_type: str, rename_to: str = "") -> str:
    out = run_gdrive(["mutate", "upload", str(local_path), "--parent", parent_id, "--mime-type", mime_type])
    m = UPLOAD_ID_RE.search(out)
    if not m:
        raise RuntimeError(f"Could not parse file ID from gdrive output: {out}")
    file_id = m.group(1)
    if rename_to:
        run_gdrive(["mutate", "rename", file_id, rename_to])
    return file_id


def main():
    root = pathlib.Path(r"C:\Users\patel\.gemini\antigravity\scratch\Basic_Medical_Notebook")
    manifest_path = root / "drive_sync_manifest.json"

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    existing_picker_filenames = {d["filename"] for d in manifest["gdocs_picker_folder"].get("docs", [])}
    existing_bundle_slugs = {d["slug"] for d in manifest["one_click_episode_bundles_folder"].get("docs", [])}

    print("--- 1. Updating Master Index Show Bible GDoc in place ---")
    index_md = root / "00_BASIC_MEDICAL_NOTEBOOK_INDEX_AND_SHOW_BIBLE.md"
    run_gdrive([
        "mutate", "update", EXISTING_INDEX_GDOC_ID, str(index_md),
        "--mime-type", "application/vnd.google-apps.document"
    ])
    print(f"Updated Master Index GDoc: {EXISTING_INDEX_GDOC_ID}")

    # Season 2 new markdown files
    new_season2_mds = [
        "VOLUME_XV_CARDIOPULMONARY_DIAGNOSTICS_ECG_VECTORS_HS_TROPONIN_HEMODYNAMICS_AND_PFT.md",
        "VOLUME_XVI_GASTROENTEROLOGY_HEPATOLOGY_AND_NUTRITION_DIAGNOSTICS.md",
        "VOLUME_XVII_ENDOCRINOLOGY_DYNAMIC_TESTING_MASS_SPECTROMETRY_AND_ADRENAL_VEIN_SAMPLING.md",
        "VOLUME_XVIII_PREVENTABLE_DEATH_LONGEVITY_AND_EVIDENCE_BASED_SCREENING_ARCHITECTURE.md",
        "VOLUME_XIX_NEURODIAGNOSTICS_EMG_NCS_EEG_AND_CSF_BIOMARKERS.md",
        "VOLUME_XX_INFECTIOUS_DISEASE_SEROLOGY_VIROLOGY_AND_MOLECULAR_DIAGNOSTICS.md",
        "VOLUME_XXI_IMMUNOHEMATOLOGY_BLOOD_BANKING_AND_ADVANCED_HEMOSTASIS.md",
        "VOLUME_XXII_CYTOGENETICS_CHROMOSOMAL_MICROARRAYS_AND_LONG_READ_GENOMICS.md",
        "LONGFORM_60MIN_PODCAST_EP809_CARDIOPULMONARY_DIAGNOSTICS_HEMODYNAMICS_AND_VASCULAR_MEDICINE.md",
        "LONGFORM_60MIN_PODCAST_EP810_GASTROENTEROLOGY_HEPATOLOGY_AND_METABOLIC_NUTRITION.md",
        "LONGFORM_60MIN_PODCAST_EP811_ENDOCRINOLOGY_DYNAMIC_TESTING_AND_NEUROENDOCRINE_DISORDERS.md",
        "LONGFORM_60MIN_PODCAST_EP812_PREVENTABLE_DEATH_LONGEVITY_AND_SCREENING_MEDICINE.md",
        "LONGFORM_60MIN_PODCAST_EP813_THE_NEURODIAGNOSTIC_VAULT_EEG_EMG_EVOKED_POTENTIALS_AND_CSF.md",
        "LONGFORM_60MIN_PODCAST_EP814_INFECTIOUS_DISEASE_SEROLOGY_VIROLOGY_AND_PARASITOLOGY.md",
        "LONGFORM_60MIN_PODCAST_EP815_BLOOD_BANKING_IMMUNOHEMATOLOGY_AND_ADVANCED_HEMOSTASIS.md",
        "LONGFORM_60MIN_PODCAST_EP816_CYTOGENETICS_CHROMOSOMAL_MICROARRAYS_AND_LONG_READ_GENOMICS.md",
    ]

    print("\n--- 2. Uploading Season 2 Volumes & Scripts as Google Docs ---")
    for fname in new_season2_mds:
        local_p = root / fname
        if not local_p.exists():
            print(f"Skipping missing file: {fname}")
            continue

        clean_title = local_p.stem
        if fname in existing_picker_filenames:
            print(f"Already uploaded in picker: {fname}")
            continue

        doc_id = upload_file(local_p, PICKER_FOLDER_ID, "application/vnd.google-apps.document", rename_to=clean_title)
        print(f"  [Created GDoc] {clean_title} -> {doc_id}")

        manifest["gdocs_picker_folder"]["docs"].append({
            "filename": fname,
            "title": clean_title,
            "doc_id": doc_id,
            "doc_url": f"https://docs.google.com/document/d/{doc_id}/edit",
        })

        raw_id = upload_file(local_p, ROOT_FOLDER_ID, "text/markdown")
        print(f"  [Uploaded Raw MD] {fname} -> {raw_id}")
        manifest["raw_uploads"].append({
            "filename": fname,
            "mime_type": "text/markdown",
            "file_id": raw_id,
        })

    # Season 2 Bundles: Bundles 09 through 16
    bundle_dir = root / "Episode_Bundles_Markdown"
    new_bundles = [
        ("Bundle_09_Ep809_Cardiopulmonary_Diagnostics_Hemodynamics_and_PFT.md", "Bundle 09 — Ep 809: Cardiopulmonary Diagnostics, Vector Loops, hs-cTn Deltoids & Body-Box DLCO (All-In-One)", [
            "VOLUME_XV_CARDIOPULMONARY_DIAGNOSTICS_ECG_VECTORS_HS_TROPONIN_HEMODYNAMICS_AND_PFT.md",
            "LONGFORM_60MIN_PODCAST_EP809_CARDIOPULMONARY_DIAGNOSTICS_HEMODYNAMICS_AND_VASCULAR_MEDICINE.md",
        ]),
        ("Bundle_10_Ep810_Gastroenterology_Hepatology_and_Nutrition.md", "Bundle 10 — Ep 810: Gastroenterology, Hepatology, Paracentesis SAAG, Chicago Manometry & Breath Physics (All-In-One)", [
            "VOLUME_XVI_GASTROENTEROLOGY_HEPATOLOGY_AND_NUTRITION_DIAGNOSTICS.md",
            "LONGFORM_60MIN_PODCAST_EP810_GASTROENTEROLOGY_HEPATOLOGY_AND_METABOLIC_NUTRITION.md",
        ]),
        ("Bundle_11_Ep811_Endocrinology_Dynamic_Testing_and_Mass_Spectrometry.md", "Bundle 11 — Ep 811: Endocrinology Dynamic Testing, Adrenal Vein Sampling & Mass Spectrometry (All-In-One)", [
            "VOLUME_XVII_ENDOCRINOLOGY_DYNAMIC_TESTING_MASS_SPECTROMETRY_AND_ADRENAL_VEIN_SAMPLING.md",
            "LONGFORM_60MIN_PODCAST_EP811_ENDOCRINOLOGY_DYNAMIC_TESTING_AND_NEUROENDOCRINE_DISORDERS.md",
        ]),
        ("Bundle_12_Ep812_Preventable_Death_Longevity_and_Screening.md", "Bundle 12 — Ep 812: Preventable Death, Evidence-Based Screening Architecture & Longevity (All-In-One)", [
            "VOLUME_XVIII_PREVENTABLE_DEATH_LONGEVITY_AND_EVIDENCE_BASED_SCREENING_ARCHITECTURE.md",
            "DOCS_ARCHIVE_04_PREVENTABLE_DEATH_SCREENING_AND_LONGEVITY.md",
            "LONGFORM_60MIN_PODCAST_EP812_PREVENTABLE_DEATH_LONGEVITY_AND_SCREENING_MEDICINE.md",
        ]),
        ("Bundle_13_Ep813_Neurodiagnostics_EEG_EMG_and_CSF_Biomarkers.md", "Bundle 13 — Ep 813: The Neurodiagnostic Vault, 10-20 EEG, SFEMG Jitter & Prion RT-QuIC (All-In-One)", [
            "VOLUME_XIX_NEURODIAGNOSTICS_EMG_NCS_EEG_AND_CSF_BIOMARKERS.md",
            "LONGFORM_60MIN_PODCAST_EP813_THE_NEURODIAGNOSTIC_VAULT_EEG_EMG_EVOKED_POTENTIALS_AND_CSF.md",
        ]),
        ("Bundle_14_Ep814_Infectious_Disease_Serology_Virology_and_Molecular.md", "Bundle 14 — Ep 814: Infectious Disease Serology, Syphilis Reverse Algorithm, HBV Core Windows & Tick Panels (All-In-One)", [
            "VOLUME_XX_INFECTIOUS_DISEASE_SEROLOGY_VIROLOGY_AND_MOLECULAR_DIAGNOSTICS.md",
            "LONGFORM_60MIN_PODCAST_EP814_INFECTIOUS_DISEASE_SEROLOGY_VIROLOGY_AND_PARASITOLOGY.md",
        ]),
        ("Bundle_15_Ep815_Blood_Banking_Immunohematology_and_Advanced_Hemostasis.md", "Bundle 15 — Ep 815: Blood Banking, 11-Cell Rule-Outs, Daratumumab DTT, Rosner Index & VWD Multimers (All-In-One)", [
            "VOLUME_XXI_IMMUNOHEMATOLOGY_BLOOD_BANKING_AND_ADVANCED_HEMOSTASIS.md",
            "LONGFORM_60MIN_PODCAST_EP815_BLOOD_BANKING_IMMUNOHEMATOLOGY_AND_ADVANCED_HEMOSTASIS.md",
        ]),
        ("Bundle_16_Ep816_Cytogenetics_Chromosomal_Microarrays_and_Long_Read_Genomics.md", "Bundle 16 — Ep 816: Cytogenetics, 550-Band Karyotypes, Dual-Fusion FISH, SNP Arrays & Nanopore Pseudogenes (All-In-One)", [
            "VOLUME_XXII_CYTOGENETICS_CHROMOSOMAL_MICROARRAYS_AND_LONG_READ_GENOMICS.md",
            "LONGFORM_60MIN_PODCAST_EP816_CYTOGENETICS_CHROMOSOMAL_MICROARRAYS_AND_LONG_READ_GENOMICS.md",
        ]),
    ]

    print("\n--- 3. Uploading Season 2 All-In-One Episode Bundles as Google Docs ---")
    for slug, title, comps in new_bundles:
        bundle_p = bundle_dir / slug
        if not bundle_p.exists():
            print(f"Skipping missing bundle: {slug}")
            continue

        if slug in existing_bundle_slugs:
            print(f"Already uploaded bundle: {slug}")
            continue

        b_doc_id = upload_file(bundle_p, BUNDLES_FOLDER_ID, "application/vnd.google-apps.document", rename_to=title)
        print(f"  [Created Bundle GDoc] {title} -> {b_doc_id}")

        manifest["one_click_episode_bundles_folder"]["docs"].append({
            "slug": slug,
            "title": title,
            "doc_id": b_doc_id,
            "doc_url": f"https://docs.google.com/document/d/{b_doc_id}/edit",
            "components": comps,
        })

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print("\nUpdated drive_sync_manifest.json with all new Google Drive Doc IDs!")


if __name__ == "__main__":
    main()
