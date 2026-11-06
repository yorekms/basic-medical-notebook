#!/usr/bin/env python3
"""Build All-In-One NotebookLM Episode Bundles and sync the entire Basic Medical repository to Google Drive."""

from __future__ import annotations

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
SHORTCUTS_FOLDER_ID = "1J3Z25T0FD76GzWcOFUDz0jhS-ewLBd9"  # Note: actual ID set below

# Verified IDs from live gdrive mkdir / create-shortcut
EXISTING_INDEX_GDOC_ID = "1V5jsPNLKfQ6lfBLeoo-yNzz_AS2I1ChJ8TmWl8kupfw"
SHORTCUTS_INFO = {
    "name": "Original_Clinical_Diagnostics_And_Immunology_Docs_Shortcuts",
    "id": "1J3Z25T0FD76GzWcOFUDz0jhS_FYKb-oS",
    "url": "https://drive.google.com/drive/folders/1J3Z25T0FD76GzWcOFUDz0jhS_FYKb-oS",
    "shortcuts": [
        {
            "target_id": "1E233Pp0QDdEAYOjrrbSwj3AD_Aa1nCwgU-iBSS6Lq9o",
            "label": "Osmolarity Adjustment Calculation Methods",
            "shortcut_id": "1XlfjY6VB7ADXhS2B0zo2OQpu_EVKGCsS",
        },
        {
            "target_id": "1hrZ44KpO0FKTbiwgsI5x5TFiuyYIBC6cJK7ElFcBTiE",
            "label": "HLA Variability and HERV Autoimmunity",
            "shortcut_id": "1NRHzxn5_rpl9k2o03Vr33WaOKDCyHXuV",
        },
        {
            "target_id": "12LRERzdsxUdPVGKxiAiSucH87-6SP2_681mLOBHfXns",
            "label": "Viral Therapy and Complement-Mediated Injury",
            "shortcut_id": "1Nqh4zeCgun75pDQaDow0g9QA9zwyyVYm",
        },
        {
            "target_id": "1OTC332XWBCT0xuU227AQd_mzY7p49-BRGr2e_oPoQzo",
            "label": "Preventable Death, Treatment, and Longevity",
            "shortcut_id": "14iEf6F8qOEXgIX0A-aNOni6ziNa3dk6c",
        },
    ],
}

BUNDLE_SPECS = [
    {
        "slug": "Bundle_01_Ep801_Kidney_Donor_Gauntlet_mGFR_Litholink_and_Split_Scans.md",
        "title": "Bundle 01 — Ep 801: Living Kidney Donor Gauntlet, mGFR, 24h Litholink & Split Scans (All-In-One)",
        "prompt": (
            "Create a deep, longest-format behind-the-curtain medical diagnostics podcast starting from a real dilemma: "
            "why even a scientifically trained living kidney donor candidate is mystified by the 45 tests ordered before donating a kidney. "
            "Walk step-by-step through WHY serum creatinine and eGFR lie (Jaffe picrate vs enzymatic creatininase, OCT2/MATE1 tubular secretion blocked by trimethoprim, muscle mass vs Cystatin C), "
            "and what happens behind the laboratory curtain during Measured GFR (weighing the Iohexol syringe to a milligram, contralateral timed draws at 120/180/240 minutes, LC-MS/MS endo/exo peaks, and the Brochner-Mortensen quadratic correction). "
            "Unpack the 24-hour urine jug (why void #1 is discarded, catching under-collection via 20-25 mg/kg/day creatinine, UACR vs UPCR, and Litholink EQUIL2 stone supersaturation), "
            "milking the 99Mo/99mTc generator at 5 AM for MAG3 split renal function, 4-phase donor CT angiography (why surgeons prefer the 7-cm left renal vein unless anatomy or split function dictates keeping the better kidney), OGTT, APOL1 G1/G2 alleles, and post-donation adaptive hyperfiltration."
        ),
        "components": [
            "VOLUME_I_THE_LIVING_KIDNEY_DONOR_GAUNTLET_MGFR_HLA_CROSSMATCH_AND_SPLIT_FUNCTION.md",
            "DOCS_ARCHIVE_01_OSMOLARITY_AND_SOLUTION_CALCULATIONS.md",
            "LONGFORM_60MIN_PODCAST_EP801_KIDNEY_DONOR_GAUNTLET_MGFR_24HR_URINE_AND_SPLIT_SCANS.md",
        ],
    },
    {
        "slug": "Bundle_02_Ep802_HLA_Typing_Luminex_Prozone_and_Living_Cell_Crossmatch.md",
        "title": "Bundle 02 — Ep 802: Yellow-Top Living Lymphocytes, HLA NGS, Luminex Prozone & Crossmatch (All-In-One)",
        "prompt": (
            "Create an exhaustive, longest-format behind-the-curtain transplant immunology and laboratory medicine podcast answering why phlebotomy draws 6 room-temperature pale-yellow ACD tubes and green sodium heparin tubes on an organ donor. "
            "Follow those living T and B lymphocytes through Ficoll-Hypaque isolation, ABO forward/reverse typing plus Dolichos biflorus lectin A2 subtyping (enabling A2-into-O/B transplants!), and 11-locus long-range NGS HLA typing with eplet and PIRCHE-II epitope matching. "
            "Go inside the dual-laser Luminex Single-Antigen Bead analyzer to explain Mean Fluorescence Intensity (MFI) and the life-or-death C1 Complement Prozone artifact—where a lethal 23,000 MFI donor-specific antibody reads a falsely negative 420 MFI until EDTA, DTT, or 1:16 dilution strips away C1q steric blockade! "
            "Contrast Paul Terasaki's 1964 rabbit-complement CDC microdroplet tray against 3-color Flow Cytometric Crossmatching (and why 37C Pronase shaving of B-cell CD32 Fc receptors prevents false positives), plus window-period HIV/HBV/HCV NAT, occult HBV cccDNA, and 4-tube QuantiFERON-TB stimulation."
        ),
        "components": [
            "VOLUME_I_THE_LIVING_KIDNEY_DONOR_GAUNTLET_MGFR_HLA_CROSSMATCH_AND_SPLIT_FUNCTION.md",
            "DOCS_ARCHIVE_02_HLA_VARIABILITY_AND_AUTOIMMUNITY.md",
            "DOCS_ARCHIVE_03_COMPLEMENT_MEDIATED_IMMUNITY.md",
            "LONGFORM_60MIN_PODCAST_EP802_HLA_TYPING_LUMINEX_PROZONE_AND_LIVING_CELL_CROSSMATCH.md",
        ],
    },
    {
        "slug": "Bundle_03_Ep803_Eight_Colored_Tubes_Core_Chemistry_and_Immunoassay_Traps.md",
        "title": "Bundle 03 — Ep 803: Eight Colored Tubes, Core Chemistry, ISE Traps, Biotin & LC-MS/MS (All-In-One)",
        "prompt": (
            "Create an enthralling, longest-format behind-the-curtain tour of everyday blood draws, Vacutainer cap chemistry, hematology lasers, Ruthenium immunoassays, and clinical LC-MS/MS. "
            "Explain tourniquet hemoconcentration, fist-pumping pseudohyperkalemia, and the CLSI Order of Draw: SPS blood culture resins, why underfilling a 9:1 light-blue citrate tube invents a fake bleeding disorder, how Gold SST micronized silica activates Factor XII while thixotropic gel liquefies at 1,500 x g, why K2-EDTA cross-contamination creates K+ of 11, Ca2+ of 3, and zero Alkaline Phosphatase (stripping catalytic zinc!), and EDTA platelet clumping vs cold agglutinins on Coulter/Sysmex counters. "
            "Reveal why Core-Lab Indirect ISE reports a fake Na+ of 121 in hypertriglyceridemia/myeloma while undiluted Blood-Gas Direct ISE reads 140, 340-nm NADH coupled enzyme kinetics, the Four Immunoassay Saboteurs (High-Dose Biotin faking Graves' disease and masking heart-attack Troponin, Giant Prolactinoma Hook Effect, Phantom hCG heterophile antibodies, and PEG macroprolactin), BNP vs NT-proBNP on Entresto, HbA1c traps, and why Triple-Quadrupole LC-MS/MS conquered steroids and urine drug screens."
        ),
        "components": [
            "VOLUME_II_PHLEBOTOMY_VACUTAINER_CHEMISTRY_AND_AUTOMATED_CORE_LAB_ANALYZERS.md",
            "VOLUME_III_COMPLETE_BLOOD_COUNT_FLOW_CYTOMETRY_COAGULATION_AND_BLOOD_BANKING.md",
            "VOLUME_IV_IMMUNOASSAYS_ENDOCRINE_DYNAMICS_CARDIAC_BIOMARKERS_AND_LC_MS_MS.md",
            "LONGFORM_60MIN_PODCAST_EP803_EIGHT_COLORED_TUBES_CORE_CHEMISTRY_AND_IMMUNOASSAY_TRAPS.md",
        ],
    },
    {
        "slug": "Bundle_04_Ep804_Behind_the_Lead_Glass_and_the_Frozen_Section_Cryostat.md",
        "title": "Bundle 04 — Ep 804: Radiology CT/MRI/PET Physics, 5-Day Biopsies, Cryostat & Procedures (All-In-One)",
        "prompt": (
            "Create a riveting, longest-format behind-the-curtain exploration of diagnostic radiology, nuclear PET, surgical pathology biopsies, and bedside physiological procedures. "
            "Step behind the CT lead glass to unpack spinning tungsten anodes, Hounsfield linear attenuation units (-1000 air, -70 fat proving benign adrenal adenomas, +70 acute blood, +1000 bone), iodine 33.2-keV K-edge dual-energy CT, bolus-tracking ROI timing (and Valsalva fake pulmonary embolisms), and busting the contrast-nephropathy myth when eGFR >= 30. "
            "Demystify Doppler <=60-degree angle physics, Zone IV 4.2-Kelvin superconducting 3T MRI magnets (T1, T2, FLAIR CSF-nulling, and 6-minute acute stroke DWI/ADC Brownian water trapping), and 511-keV positron coincidence FDG-PET. "
            "Then answer why routine biopsies take 5 days (grossing ink -> 10% formalin -> ethanol -> xylene clearing -> 60C paraffin -> 4-um microtome -> H&E + 98C HIER DAB immunohistochemistry, and which specimens formalin ruins!) vs 15-minute intraoperative -22C cryostat frozen sections, plus Cath-Lab FFR, PFT Body-Box/DLCO, NBI colonoscopy, and EMG/NCS."
        ),
        "components": [
            "VOLUME_VII_RADIOLOGY_CT_MRI_ULTRASOUND_AND_NUCLEAR_PET_PHYSICS_BEHIND_THE_GLASS.md",
            "VOLUME_VIII_ANATOMIC_PATHOLOGY_BIOPSY_FROZEN_SECTION_IHC_NGS_AND_ENDOSCOPIC_CARDIAC_PROCEDURES.md",
            "LONGFORM_60MIN_PODCAST_EP804_BEHIND_THE_LEAD_GLASS_AND_THE_FROZEN_SECTION_CRYOSTAT.md",
        ],
    },
    {
        "slug": "Bundle_05_Ep805_The_Oncology_Workup_Tumor_Markers_Liquid_Biopsy_and_Theranostics.md",
        "title": "Bundle 05 — Ep 805: The Cancer Order Sheet — Tumor Markers, Marrow Flow, NGS, ctDNA & Theranostic PET (All-In-One)",
        "prompt": (
            "Create an authoritative, longest-format behind-the-curtain podcast covering every diagnostic test ordered in modern oncology and hematology. "
            "Explain why serum tumor markers rarely work for population screening yet guide cancer kinetics—unpacking Total vs %Free PSA (finasteride halving rule + PI-RADS fusion biopsy), why 7% of humans are genetically Lewis-negative (FUT3) and read zero CA 19-9 even with metastatic pancreatic cancer while gallstones spike it to 5,000, AFP/hCG post-orchiectomy half-life clocks, anti-thyroglobulin interference solved by LC-MS/MS, and why Rasburicase tumor-lysis blood must travel on ice. "
            "Walk through posterior iliac crest Bone Marrow Aspirate + Core ('dry tap' myelofibrosis), 10-color flow cytometry (2-hour APL Auer-rod emergency & kappa/lambda B-cell clonality), FISH, and 10^-6 clonoSEQ MRD. "
            "Then go inside solid-tumor DNA + anchored-multiplex RNA fusion NGS (MSI-High, TMB, HRD scars, VAF ~50% germline clues), Streck-tube UMI Liquid Biopsy ctDNA (and the aging-blood CHIP impostor!), stereotactic BI-RADS mammography, dual-tracer sentinel nodes, and Ga-68/Lu-177 PSMA & DOTATATE theranostics."
        ),
        "components": [
            "VOLUME_IX_ONCOLOGY_DIAGNOSTICS_TUMOR_MARKERS_MARROW_FLOW_LIQUID_BIOPSY_AND_MOLECULAR_STAGING.md",
            "DOCS_ARCHIVE_04_PREVENTABLE_DEATH_SCREENING_AND_LONGEVITY.md",
            "LONGFORM_60MIN_PODCAST_EP805_THE_ONCOLOGY_WORKUP_TUMOR_MARKERS_LIQUID_BIOPSY_MARROW_FLOW_AND_THERANOSTIC_PET.md",
        ],
    },
    {
        "slug": "Bundle_06_Ep806_ICU_Red_Alert_Orders_Shock_Gaps_Ventilator_Curves_and_Coma_EEG.md",
        "title": "Bundle 06 — Ep 806: ICU Red-Alert Orders — Shock Gaps, Stewart Ions, Ventilators, TEG & Coma EEG (All-In-One)",
        "prompt": (
            "Create a high-stakes, longest-format behind-the-curtain podcast decoding every STAT order in the Shock-Trauma ICU and Emergency Department. "
            "Start at 3 AM with Arterial Blood Gases and 128-wavelength Co-Oximetry (why finger pulse oximeters read 99% in lethal carbon monoxide poisoning), Winters' formula, the Delta-Delta ratio catching triple acid-base disorders, and Peter Stewart's Strong Ion Difference proving why 4 liters of 0.9% 'Normal' Saline (SID = 0) chemically forces hyperchloremic acidosis—plus the Osmolal Gap and Point-of-Care vs Core-Lab Lactate Gap unmasking antifreeze poisoning! "
            "Unpack Type A vs epinephrine Type B lactate, Fick SvO2/ScvO2 (why SvO2 of 85% in sepsis or cyanide is terrifying), and the Pv-aCO2 > 6 mmHg microvascular stagnation gap. "
            "Treat the ICU ventilator as a biophysics analyzer: 0.5-sec End-Inspiratory Hold (PIP vs Pplat & Driving Pressure < 15), End-Expiratory Hold Auto-PEEP, capnography, and RSBI < 105. "
            "Finish with whole-blood TEG/ROTEM trauma resuscitation, HIT 14C-SRA, eFAST/RUSH/VExUS venous congestion Doppler, ICP P2>P1 herniation waves, continuous coma cEEG, and 72-hour SSEP N20 post-arrest prognostication."
        ),
        "components": [
            "VOLUME_X_ICU_TRAUMA_AND_EMERGENCY_CRITICAL_CARE_DIAGNOSTIC_ORDERS.md",
            "LONGFORM_60MIN_PODCAST_EP806_ICU_RED_ALERT_ORDERS_SHOCK_GAPS_VENTILATOR_CURVES_TEG_POCUS_AND_COMA_EEG.md",
        ],
    },
    {
        "slug": "Bundle_07_Ep807_From_Womb_to_Heel_Stick_NIPT_Tandem_MS_Sweat_Chloride_and_Trio_Exomes.md",
        "title": "Bundle 07 — Ep 807: Prenatal cfDNA, Newborn Heel-Stick MS/MS, Sweat Chloride & NICU Trio Genomes (All-In-One)",
        "prompt": (
            "Create a deeply illuminating, longest-format behind-the-curtain podcast tracing every diagnostic test from pregnancy through newborn nursery, pediatrics, and rapid clinical genomics. "
            "Start before birth with Dennis Lo's prenatal cfDNA (NIPT): why 'fetal' cfDNA is actually 143-bp placental trophoblast DNA, why maternal obesity drops Fetal Fraction below 4%, and why Confined Placental Mosaicism means positive NIPT MUST be confirmed by amniocentesis—plus noninvasive MCA Doppler for fetal anemia and Kleihauer-Betke rose-pink HbF cells vs flow cytometry for RhoGAM dosing. "
            "Go inside the 2 AM State Newborn Screening Lab to watch five 3.2-mm paper punches from a 24-48 hour lateral heel-stick run through Electrospray Tandem Mass Spectrometry in 90 seconds (PKU, Maple Syrup Urine Disease, C8 Octanoylcarnitine MCAD deficiency), qPCR for TREC = 0 'Bubble Boy' SCID and SMN1 SMA (enabling week-1 Zolgensma gene therapy!), "
            "CCHD right-hand/foot oximetry, OAE vs NICU AABR hearing, Pilocarpine Iontophoresis Sweat Chloride for Cystic Fibrosis, capillary-vs-venous Lead, pyloric/intussusception ultrasound, SNP Microarray UPD, and 48-hour NICU Rapid Trio Whole-Genome Sequencing."
        ),
        "components": [
            "VOLUME_XI_PEDIATRICS_NEONATAL_HEEL_STICK_PRENATAL_CFDNA_AND_GENOMIC_DIAGNOSTICS.md",
            "LONGFORM_60MIN_PODCAST_EP807_FROM_WOMB_TO_HEEL_STICK_NIPT_TANDEM_MS_SWEAT_CHLORIDE_AND_TRIO_EXOMES.md",
        ],
    },
    {
        "slug": "Bundle_08_Ep808_Jeopardy_Grandmaster_Tour_Microbiology_Fluid_Taps_and_Classic_Tests.md",
        "title": "Bundle 08 — Ep 808: Jeopardy! Grandmaster Tour — MALDI-TOF, Fluid Taps, Autoimmunity & Classic Named Tests (All-In-One)",
        "prompt": (
            "Create an exhilarating, longest-format championship tour through microbiology, urinalysis, sterile body-fluid taps, rheumatology, subspecialty testing, and classic 'Jeopardy! $2,000 Clue' named medical tests! "
            "Open behind the microbiology biosafety cabinet: why 40-60 mL blood volume and antibiotic-binding resins matter in sepsis, why Chocolate Agar heats sheep blood to 80C to kill NADase, how 337-nm MALDI-TOF lasers weigh ribosomal proteins in 90 seconds (yet confuse Shigella with E. coli!), busting the raw MIC comparison fallacy, inducible D-zone clindamycin resistance, and 3.32-cycle TaqMan qPCR math. "
            "Expose the 3 famous urine dipstick blindspots (Bence Jones myeloma light chains, beta-hydroxybutyrate in early DKA, and Vitamin C false negatives), CSF Tube 1-vs-4 spectrophotometric 450-nm xanthochromia, Light's Criteria, ascitic SAAG >= 1.1, and 530-nm red-plate polarized crystal physics (Gout yellow parallel vs Pseudogout blue parallel!). "
            "Tour HEp-2 ANA (benign DFS70 vs Centromere), Crithidia kinetoplast dsDNA, 13C-urea breath, SFEMG jitter, RT-QuIC prions, Michel's skin DIF, Ara h 2 peanut IgE, FLAER/EMA/DHR flow tests, and a rapid-fire Jeopardy! Named-Test Lightning Finale!"
        ),
        "components": [
            "VOLUME_V_MICROBIOLOGY_BLOOD_CULTURES_MALDI_TOF_PCR_CT_VALUES_AND_SEROLOGY.md",
            "VOLUME_VI_URINALYSIS_BODY_FLUID_TAP_MICROSCOPY_AND_AUTOIMMUNE_RHEUMATOLOGY_PANELS.md",
            "VOLUME_XII_SPECIALTY_CLINICAL_TESTS_NEURO_GI_DERM_ALLERGY_OPHTHO_AND_JEOPARDY_COMPENDIUM.md",
            "VOLUME_XIII_MASTER_MEDICAL_TESTING_ENCYCLOPEDIA_TUBES_METHODS_TRAPS_AND_JEOPARDY_MATRIX.md",
            "LONGFORM_60MIN_PODCAST_EP808_THE_JEOPARDY_GRANDMASTER_TOUR_MICROBIOLOGY_FLUID_TAPS_AUTOIMMUNITY_AND_CLASSIC_TESTS.md",
        ],
    },
]

UPLOAD_ID_RE = re.compile(r"\(ID:\s*([A-Za-z0-9_-]+)\)")


def run_gdrive(args: List[str]) -> str:
    gdrive_bin = shutil.which("gdrive")
    if gdrive_bin and gdrive_bin.lower().endswith(".ps1"):
        cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", gdrive_bin] + args
    elif gdrive_bin:
        cmd = [gdrive_bin] + args
    else:
        cmd = ["powershell", "-NoProfile", "-Command", "gdrive " + " ".join(f'"{a}"' for a in args)]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if proc.returncode != 0:
        raise RuntimeError(f"Command failed ({proc.returncode}): {' '.join(cmd)}\n{proc.stdout}\n{proc.stderr}")
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


def build_bundles(root: pathlib.Path) -> List[pathlib.Path]:
    bundle_dir = root / "Episode_Bundles_Markdown"
    bundle_dir.mkdir(parents=True, exist_ok=True)
    built: List[pathlib.Path] = []
    for spec in BUNDLE_SPECS:
        out_path = bundle_dir / spec["slug"]
        parts = [
            f"# {spec['title']}\n",
            "## ZERO-MIXUP SINGLE-SOURCE BUNDLE FOR GOOGLE NOTEBOOKLM\n",
            "**How to use in NotebookLM (`notebook.google.com`):**\n",
            "1. Check **ONLY THIS ONE DOCUMENT** in your NotebookLM Sources sidebar (uncheck all others—every reference treatise and script needed for this episode is merged right inside this single file!).",
            "2. Click **Customize** on **Audio Overview**, choose **Longer**, and paste this exact prompt:\n",
            f"```text\n{spec['prompt']}\n```\n",
            "---\n",
        ]
        for comp_name in spec["components"]:
            comp_path = root / comp_name
            if not comp_path.exists():
                raise FileNotFoundError(f"Missing required bundle component: {comp_path}")
            comp_body = comp_path.read_text(encoding="utf-8")
            parts.append(f"\n---\n\n## INCLUDED SOURCE: `{comp_name}`\n\n{comp_body}\n")
        out_path.write_text("\n".join(parts), encoding="utf-8")
        built.append(out_path)
        print(f"Built bundle: {out_path.name} ({out_path.stat().st_size:,} bytes)")
    return built


def main() -> int:
    root = pathlib.Path(__file__).resolve().parent.parent
    print(f"Building Episode Bundles in {root / 'Episode_Bundles_Markdown'}...")
    build_bundles(root)

    md_files = sorted(root.glob("*.md"))
    picker_docs: List[Dict[str, str]] = []
    raw_uploads: List[Dict[str, str]] = []

    print(f"\nUploading {len(md_files)} Markdown volumes & scripts to Google Drive...")
    for md_path in md_files:
        clean_title = md_path.stem
        if md_path.name == "00_BASIC_MEDICAL_NOTEBOOK_INDEX_AND_SHOW_BIBLE.md":
            # Update the already-created native Google Doc in place!
            run_gdrive(
                [
                    "mutate",
                    "update",
                    EXISTING_INDEX_GDOC_ID,
                    str(md_path),
                    "--mime-type",
                    "application/vnd.google-apps.document",
                ]
            )
            doc_id = EXISTING_INDEX_GDOC_ID
            print(f"  [Updated GDoc] {clean_title} -> {doc_id}")
        else:
            doc_id = upload_file(
                md_path,
                PICKER_FOLDER_ID,
                "application/vnd.google-apps.document",
                rename_to=clean_title,
            )
            print(f"  [Created GDoc] {clean_title} -> {doc_id}")

        picker_docs.append(
            {
                "filename": md_path.name,
                "title": clean_title,
                "doc_id": doc_id,
                "doc_url": f"https://docs.google.com/document/d/{doc_id}/edit",
            }
        )

        raw_id = upload_file(md_path, ROOT_FOLDER_ID, "text/markdown")
        print(f"  [Uploaded Raw MD] {md_path.name} -> {raw_id}")
        raw_uploads.append(
            {
                "filename": md_path.name,
                "mime_type": "text/markdown",
                "file_id": raw_id,
            }
        )

    # Upload Python TTS script to root folder
    tts_script = root / "scripts" / "render_basic_medical_60min_tts.py"
    tts_id = upload_file(tts_script, ROOT_FOLDER_ID, "text/x-python")
    print(f"  [Uploaded Script] {tts_script.name} -> {tts_id}")
    raw_uploads.append(
        {
            "filename": tts_script.name,
            "mime_type": "text/x-python",
            "file_id": tts_id,
        }
    )

    # Upload all 8 All-In-One Episode Bundles as native Google Docs
    bundle_entries = []
    print(f"\nUploading {len(BUNDLE_SPECS)} All-In-One Episode Bundles as native Google Docs...")
    for spec in BUNDLE_SPECS:
        b_path = root / "Episode_Bundles_Markdown" / spec["slug"]
        b_doc_id = upload_file(
            b_path,
            BUNDLES_FOLDER_ID,
            "application/vnd.google-apps.document",
            rename_to=spec["title"],
        )
        print(f"  [Created Bundle GDoc] {spec['title']} -> {b_doc_id}")
        bundle_entries.append(
            {
                "slug": spec["slug"],
                "title": spec["title"],
                "doc_id": b_doc_id,
                "doc_url": f"https://docs.google.com/document/d/{b_doc_id}/edit",
                "components": spec["components"],
            }
        )

    manifest = {
        "notebook_title": "Basic Medical — Behind the Curtain Clinical Diagnostics & Jeopardy! Grandmaster Suite",
        "root_folder": {
            "name": "Basic Medical - Behind the Curtain Diagnostics Notebook",
            "id": ROOT_FOLDER_ID,
            "url": f"https://drive.google.com/drive/folders/{ROOT_FOLDER_ID}",
        },
        "gdocs_picker_folder": {
            "name": "Google_Docs_For_NotebookLM_Picker",
            "id": PICKER_FOLDER_ID,
            "url": f"https://drive.google.com/drive/folders/{PICKER_FOLDER_ID}",
            "docs": picker_docs,
        },
        "one_click_episode_bundles_folder": {
            "name": "One_Click_Episode_Bundles_For_NotebookLM",
            "id": BUNDLES_FOLDER_ID,
            "url": f"https://drive.google.com/drive/folders/{BUNDLES_FOLDER_ID}",
            "bundles": bundle_entries,
        },
        "shortcuts_folder": SHORTCUTS_INFO,
        "raw_uploads": raw_uploads,
    }

    manifest_path = root / "drive_sync_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    manifest_id = upload_file(manifest_path, ROOT_FOLDER_ID, "application/json")
    print(f"\nSaved and uploaded drive_sync_manifest.json -> {manifest_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
