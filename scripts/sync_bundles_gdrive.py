#!/usr/bin/env python3
"""Sync remaining Season 2 All-In-One Episode Bundles to Google Drive."""

import json
import pathlib
import re
import shutil
import subprocess
import sys

BUNDLES_FOLDER_ID = "1FLCOLKL2hPj6VIwfsCV6IKOjS-ewLBd9"
UPLOAD_ID_RE = re.compile(r"\(ID:\s*([A-Za-z0-9_-]+)\)")


def run_gdrive(args):
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

    existing_slugs = {b["slug"] for b in manifest["one_click_episode_bundles_folder"]["bundles"]}

    # Ensure Bundle 09 is registered
    b09_slug = "Bundle_09_Ep809_Cardiopulmonary_Diagnostics_Hemodynamics_and_PFT.md"
    if b09_slug not in existing_slugs:
        manifest["one_click_episode_bundles_folder"]["bundles"].append({
            "slug": b09_slug,
            "title": "Bundle 09 — Ep 809: Cardiopulmonary Diagnostics, Vector Loops, hs-cTn Deltoids & Body-Box DLCO (All-In-One)",
            "doc_id": "1Sgcl1cFTgvr57Z_z6i1ZvHBI_o7ZCd5eQ1BOywK8VMU",
            "doc_url": "https://docs.google.com/document/d/1Sgcl1cFTgvr57Z_z6i1ZvHBI_o7ZCd5eQ1BOywK8VMU/edit",
            "components": [
                "VOLUME_XV_CARDIOPULMONARY_DIAGNOSTICS_ECG_VECTORS_HS_TROPONIN_HEMODYNAMICS_AND_PFT.md",
                "LONGFORM_60MIN_PODCAST_EP809_CARDIOPULMONARY_DIAGNOSTICS_HEMODYNAMICS_AND_VASCULAR_MEDICINE.md",
            ],
        })
        existing_slugs.add(b09_slug)
        print("Registered existing Bundle 09 into manifest!")

    bundle_dir = root / "Episode_Bundles_Markdown"
    remaining_bundles = [
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

    print("\n--- Uploading Remaining Season 2 Bundles as Google Docs ---")
    for slug, title, comps in remaining_bundles:
        bundle_p = bundle_dir / slug
        if not bundle_p.exists():
            print(f"Skipping missing bundle: {slug}")
            continue

        if slug in existing_slugs:
            print(f"Already uploaded bundle: {slug}")
            continue

        b_doc_id = upload_file(bundle_p, BUNDLES_FOLDER_ID, "application/vnd.google-apps.document", rename_to=title)
        print(f"  [Created Bundle GDoc] {title} -> {b_doc_id}")

        manifest["one_click_episode_bundles_folder"]["bundles"].append({
            "slug": slug,
            "title": title,
            "doc_id": b_doc_id,
            "doc_url": f"https://docs.google.com/document/d/{b_doc_id}/edit",
            "components": comps,
        })
        existing_slugs.add(slug)

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print("\nUpdated drive_sync_manifest.json with all 16 bundles!")


if __name__ == "__main__":
    main()
