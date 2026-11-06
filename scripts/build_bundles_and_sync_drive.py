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
            "Deep dive into the living kidney donor gauntlet: measured GFR vs estimated equations, iohexol plasma clearance HPLC, 24-hour Litholink chemistry collection traps, nuclear MAG3 split renal function, and contrast-enhanced renal CTA vascular mapping."
        ),
        "components": [
            "VOLUME_I_THE_LIVING_KIDNEY_DONOR_GAUNTLET_MGFR_HLA_CROSSMATCH_AND_SPLIT_FUNCTION.md",
            "DOCS_ARCHIVE_01_OSMOLARITY_AND_SOLUTION_CALCULATIONS.md",
            "LONGFORM_60MIN_PODCAST_EP801_KIDNEY_DONOR_GAUNTLET_MGFR_24HR_URINE_AND_SPLIT_SCANS.md"
],
    },
    {
        "slug": "Bundle_02_Ep802_HLA_Typing_Luminex_Prozone_and_Living_Cell_Crossmatch.md",
        "title": "Bundle 02 — Ep 802: Yellow-Top Living Lymphocytes, HLA NGS, Luminex Prozone & Crossmatch (All-In-One)",
        "prompt": (
            "Unpack the transplant immunology gauntlet: ACD-A yellow-top viable lymphocytes, 11-locus HLA high-resolution NGS, Luminex single-antigen bead MFI, complement C1q prozone hooks, and Pronase flow cytometric living-cell crossmatch."
        ),
        "components": [
            "VOLUME_I_THE_LIVING_KIDNEY_DONOR_GAUNTLET_MGFR_HLA_CROSSMATCH_AND_SPLIT_FUNCTION.md",
            "DOCS_ARCHIVE_02_HLA_VARIABILITY_AND_AUTOIMMUNITY.md",
            "DOCS_ARCHIVE_03_COMPLEMENT_MEDIATED_IMMUNITY.md",
            "LONGFORM_60MIN_PODCAST_EP802_HLA_TYPING_LUMINEX_PROZONE_AND_LIVING_CELL_CROSSMATCH.md"
],
    },
    {
        "slug": "Bundle_03_Ep803_Eight_Colored_Tubes_Core_Chemistry_and_Immunoassay_Traps.md",
        "title": "Bundle 03 — Ep 803: Eight Colored Vacutainers, Core Lab Chemistry & Immunoassay Traps (All-In-One)",
        "prompt": (
            "Explore the phlebotomy draw sequence, eight colored Vacutainer tube chemistries, direct vs indirect ISE pseudohyponatremia, high-dose hook effects, streptavidin-biotin sandwich sabotage, and gold-standard LC-MS/MS."
        ),
        "components": [
            "VOLUME_II_PHLEBOTOMY_VACUTAINER_CHEMISTRY_AND_AUTOMATED_CORE_LAB_ANALYZERS.md",
            "VOLUME_III_COMPLETE_BLOOD_COUNT_FLOW_CYTOMETRY_COAGULATION_AND_BLOOD_BANKING.md",
            "VOLUME_IV_IMMUNOASSAYS_ENDOCRINE_DYNAMICS_CARDIAC_BIOMARKERS_AND_LC_MS_MS.md",
            "LONGFORM_60MIN_PODCAST_EP803_EIGHT_COLORED_TUBES_CORE_CHEMISTRY_AND_IMMUNOASSAY_TRAPS.md"
],
    },
    {
        "slug": "Bundle_04_Ep804_Behind_the_Lead_Glass_and_the_Cryostat.md",
        "title": "Bundle 04 — Ep 804: Behind the Lead Glass & The Cryostat (All-In-One)",
        "prompt": (
            "Go behind the lead glass and into the pathology lab: CT Hounsfield physics, 3T MRI superconducting gradient coils, 511-keV coincidence PET detectors, 20-minute OR cryostat frozen sections vs 5-day FFPE tissue processing."
        ),
        "components": [
            "VOLUME_VII_RADIOLOGY_CT_MRI_ULTRASOUND_AND_NUCLEAR_PET_PHYSICS_BEHIND_THE_GLASS.md",
            "VOLUME_VIII_ANATOMIC_PATHOLOGY_BIOPSY_FROZEN_SECTION_IHC_NGS_AND_ENDOSCOPIC_CARDIAC_PROCEDURES.md",
            "LONGFORM_60MIN_PODCAST_EP804_BEHIND_THE_LEAD_GLASS_AND_THE_FROZEN_SECTION_CRYOSTAT.md"
],
    },
    {
        "slug": "Bundle_05_Ep805_The_Oncology_Workup_Tumor_Markers_and_Liquid_Biopsy.md",
        "title": "Bundle 05 — Ep 805: The Cancer Order Sheet, Tumor Markers, Liquid Biopsy & Theranostics (All-In-One)",
        "prompt": (
            "Follow the complete cancer diagnostic workup: tumor markers CEA, PSA, CA-125, bone marrow 12-color flow cytometry for MRD, comprehensive solid tumor NGS panels, ctDNA liquid biopsies distinguishing tumor from CHIP, and theranostic radioligand PET."
        ),
        "components": [
            "VOLUME_IX_ONCOLOGY_DIAGNOSTICS_TUMOR_MARKERS_MARROW_FLOW_LIQUID_BIOPSY_AND_MOLECULAR_STAGING.md",
            "LONGFORM_60MIN_PODCAST_EP805_THE_ONCOLOGY_WORKUP_TUMOR_MARKERS_LIQUID_BIOPSY_MARROW_FLOW_AND_THERANOSTIC_PET.md"
],
    },
    {
        "slug": "Bundle_06_Ep806_ICU_Red_Alert_Orders_Shock_Ventilator_Curves_and_Coma_EEG.md",
        "title": "Bundle 06 — Ep 806: ICU Red-Alert Orders, Shock Gaps, Ventilator Curves & TEG (All-In-One)",
        "prompt": (
            "ICU red-alert diagnostic orders: Stewart strong ion difference, mixed venous oxygen and venoarterial pCO2 gap in shock, mechanical ventilator flow-volume curves, rotational thromboelastography (TEG), VExUS ultrasound, and continuous coma EEG."
        ),
        "components": [
            "VOLUME_X_ICU_TRAUMA_AND_EMERGENCY_CRITICAL_CARE_DIAGNOSTIC_ORDERS.md",
            "LONGFORM_60MIN_PODCAST_EP806_ICU_RED_ALERT_ORDERS_SHOCK_GAPS_VENTILATOR_CURVES_TEG_POCUS_AND_COMA_EEG.md"
],
    },
    {
        "slug": "Bundle_07_Ep807_From_Womb_to_Heel_Stick_Prenatal_cfDNA_and_Trio_Exomes.md",
        "title": "Bundle 07 — Ep 807: From Womb to Heel-Stick, Prenatal cfDNA, 5-Punch Heel-Stick & Trio Exomes (All-In-One)",
        "prompt": (
            "From prenatal cell-free DNA maternal plasma screening and fetal fraction traps through the 5-punch newborn heel-stick Guthrie card tandem mass spec (MS/MS), sweat chloride pilocarpine iontophoresis, and rapid NICU trio whole exomes."
        ),
        "components": [
            "VOLUME_XI_PEDIATRICS_NEONATAL_HEEL_STICK_PRENATAL_CFDNA_AND_GENOMIC_DIAGNOSTICS.md",
            "LONGFORM_60MIN_PODCAST_EP807_FROM_WOMB_TO_HEEL_STICK_NIPT_TANDEM_MS_SWEAT_CHLORIDE_AND_TRIO_EXOMES.md"
],
    },
    {
        "slug": "Bundle_08_Ep808_The_Jeopardy_Grandmaster_Diagnostic_Tour.md",
        "title": "Bundle 08 — Ep 808: The Jeopardy! Grandmaster Diagnostic Tour (All-In-One)",
        "prompt": (
            "The ultimate Jeopardy! grandmaster clinical diagnostic tour: 90-second MALDI-TOF mass spec, continuous blood culture optical monitoring, urine dipstick falsehoods, polarized crystal microscopy for gout vs pseudogout, Crithidia luciliae immunofluorescence, and classic named tests."
        ),
        "components": [
            "VOLUME_V_MICROBIOLOGY_BLOOD_CULTURES_MALDI_TOF_PCR_CT_VALUES_AND_SEROLOGY.md",
            "VOLUME_VI_URINALYSIS_BODY_FLUID_TAP_MICROSCOPY_AND_AUTOIMMUNE_RHEUMATOLOGY_PANELS.md",
            "VOLUME_XII_SPECIALTY_CLINICAL_TESTS_NEURO_GI_DERM_ALLERGY_OPHTHO_AND_JEOPARDY_COMPENDIUM.md",
            "VOLUME_XIII_MASTER_MEDICAL_TESTING_ENCYCLOPEDIA_TUBES_METHODS_TRAPS_AND_JEOPARDY_MATRIX.md",
            "LONGFORM_60MIN_PODCAST_EP808_THE_JEOPARDY_GRANDMASTER_TOUR_MICROBIOLOGY_FLUID_TAPS_AUTOIMMUNITY_AND_CLASSIC_TESTS.md"
],
    },
    {
        "slug": "Bundle_09_Ep809_Cardiopulmonary_Diagnostics_Hemodynamics_and_PFT.md",
        "title": "Bundle 09 — Ep 809: Cardiopulmonary Diagnostics, Vector Loops, hs-cTn Deltoids & Body-Box DLCO (All-In-One)",
        "prompt": (
            "Deep dive into cardiopulmonary diagnostics: 12-lead ECG vector loops and limb lead reversal traps, high-sensitivity troponin rapid 0/1h ESC algorithms and 99th percentile URL sex cutoffs, SPECT myocardial perfusion coronary steal vs dobutamine, Cath-Lab pressure wire FFR and iFR, and PFT body plethysmography Boyle's law thoracic gas volume and single-breath DLCO Krogh equations."
        ),
        "components": [
            "VOLUME_XV_CARDIOPULMONARY_DIAGNOSTICS_ECG_VECTORS_HS_TROPONIN_HEMODYNAMICS_AND_PFT.md",
            "LONGFORM_60MIN_PODCAST_EP809_CARDIOPULMONARY_DIAGNOSTICS_HEMODYNAMICS_AND_VASCULAR_MEDICINE.md"
],
    },
    {
        "slug": "Bundle_10_Ep810_Gastroenterology_Hepatology_and_Nutrition.md",
        "title": "Bundle 10 — Ep 810: Gastroenterology, Hepatology, Paracentesis SAAG, Chicago Manometry & Breath Physics (All-In-One)",
        "prompt": (
            "Comprehensive masterclass on gastroenterology, hepatology, and nutrition testing: the R-factor equation [(ALT/ULN)/(ALP/ULN)] classifying hepatocellular vs cholestatic injury, De Ritis AST/ALT ratio and P5P deficiency, the acute Wilson disease crisis with Bilirubin/ALP > 2 and Coombs-negative hemolysis, FibroScan shear wave kPa elastography, paracentesis SAAG >= 1.1 portal hypertension, 13C-urea and H2/CH4 breath testing, celiac total IgA/tTG cascade, fecal calprotectin and elastase, stool osmotic gap, and Chicago Classification v4.0 high-resolution manometry."
        ),
        "components": [
            "VOLUME_XVI_GASTROENTEROLOGY_HEPATOLOGY_AND_NUTRITION_DIAGNOSTICS.md",
            "LONGFORM_60MIN_PODCAST_EP810_GASTROENTEROLOGY_HEPATOLOGY_AND_METABOLIC_NUTRITION.md"
],
    },
    {
        "slug": "Bundle_11_Ep811_Endocrinology_Dynamic_Testing_and_Mass_Spectrometry.md",
        "title": "Bundle 11 — Ep 811: Endocrinology Dynamic Testing, Adrenal Vein Sampling & Mass Spectrometry (All-In-One)",
        "prompt": (
            "Deep exploration of dynamic endocrine testing and steroid mass spectrometry: why static hormone levels lie in pulsatile axes, Cushing's 3-step screening (1-mg dexamethasone suppression with LC-MS/MS serum dex check > 140-200 ng/dL, 24-hr UFC, late-night salivary cortisol), Adrenal Vein Sampling (AVS) Cortisol Selectivity Index and Lateralization Index >= 4.0 for primary aldosteronism, seated ARR drug washouts, Cosyntropin stim test and 17-OHP, supine resting plasma free metanephrines for pheochromocytoma, and hypertonic saline copeptin infusion for diabetes insipidus."
        ),
        "components": [
            "VOLUME_XVII_ENDOCRINOLOGY_DYNAMIC_TESTING_MASS_SPECTROMETRY_AND_ADRENAL_VEIN_SAMPLING.md",
            "LONGFORM_60MIN_PODCAST_EP811_ENDOCRINOLOGY_DYNAMIC_TESTING_AND_NEUROENDOCRINE_DISORDERS.md"
],
    },
    {
        "slug": "Bundle_12_Ep812_Preventable_Death_Longevity_and_Screening.md",
        "title": "Bundle 12 — Ep 812: Preventable Death, Evidence-Based Screening Architecture & Longevity (All-In-One)",
        "prompt": (
            "Masterclass on evidence-based screening mathematics and longevity diagnostics: Bayes' theorem in clinical practice, lead-time bias, length-time bias, overdiagnosis, and number needed to screen (NNS); Apolipoprotein B (ApoB) total atherogenic particle burden vs calculated LDL-C, once-in-a-lifetime molar Lp(a) nmol/L assays, and hs-CRP residual inflammation; non-contrast ECG-gated Coronary Artery Calcium (CAC) Agatston scoring (density factor 1-4 and the power of zero); Low-Dose CT lung cancer screening (USPSTF 20 pack-year criteria, Lung-RADS); screening colonoscopy vs Cologuard mt-sDNA vs annual FIT; cervical high-risk HPV 16/18 PCR; DEXA T-score vs Z-score and Trabecular Bone Score; and debunking the whole-body executive scan fallacy."
        ),
        "components": [
            "VOLUME_XVIII_PREVENTABLE_DEATH_LONGEVITY_AND_EVIDENCE_BASED_SCREENING_ARCHITECTURE.md",
            "DOCS_ARCHIVE_04_PREVENTABLE_DEATH_SCREENING_AND_LONGEVITY.md",
            "LONGFORM_60MIN_PODCAST_EP812_PREVENTABLE_DEATH_LONGEVITY_AND_SCREENING_MEDICINE.md"
],
    },
    {
        "slug": "Bundle_13_Ep813_Neurodiagnostics_EEG_EMG_and_CSF_Biomarkers.md",
        "title": "Bundle 13 — Ep 813: The Neurodiagnostic Vault, 10-20 EEG, SFEMG Jitter & Prion RT-QuIC (All-In-One)",
        "prompt": (
            "Behind the scenes in clinical neurophysiology and the neurodiagnostic vault: 10-20 EEG electrode physics, bipolar vs referential montages, normal alpha/beta/theta/delta rhythms, epileptiform spikes and 3-Hz spike-and-wave discharges, continuous ICU EEG in non-convulsive status; Motor and Sensory NCS (CMAP, SNAP, conduction velocity and conduction block in demyelination), late responses F-wave and H-reflex; Needle EMG insertional and spontaneous rest activity (fibrillations, positive sharp waves), neurogenic vs myopathic MUAPs; Single-Fiber EMG (SFEMG) mean consecutive difference (MCD) jitter and impulse blocking in Myasthenia Gravis; Evoked potentials VEP P100 delay in optic neuritis, BAEP waves I-V, SSEP median nerve N20 bilateral absence at 72h post-arrest; and CSF diagnostics: albuminocytologic dissociation, oligoclonal bands (OCB isoelectric focusing with IgG immunoblotting), IgG index > 0.70, autoimmune encephalitis panels, and Prion disease RT-QuIC 90.3% sensitivity / 99.5-100% specificity."
        ),
        "components": [
            "VOLUME_XIX_NEURODIAGNOSTICS_EMG_NCS_EEG_AND_CSF_BIOMARKERS.md",
            "LONGFORM_60MIN_PODCAST_EP813_THE_NEURODIAGNOSTIC_VAULT_EEG_EMG_EVOKED_POTENTIALS_AND_CSF.md"
],
    },
    {
        "slug": "Bundle_14_Ep814_Infectious_Disease_Serology_Virology_and_Molecular.md",
        "title": "Bundle 14 — Ep 814: Infectious Disease Serology, Syphilis Reverse Algorithm, HBV Core Windows & Tick Panels (All-In-One)",
        "prompt": (
            "Comprehensive masterclass on infectious disease serology, virology, and molecular diagnostics: Syphilis Traditional vs CDC Reverse Sequence Algorithm (treponemal EIA/CIA screen, reflex quantitative RPR, second treponemal TP-PA/FTA-ABS resolution), biological false positives, and the RPR prozone effect in secondary syphilis; Hepatitis B 6-marker serology matrix and the diagnostic Core Window where IgM Anti-HBc is the sole marker; Modern HIV testing algorithm (4th/5th gen Ag/Ab combo screen with p24 antigen, reflex Geenius differentiation, reflex HIV RNA NAT for acute window); Vector-borne Lyme disease modified two-tiered testing (MTTT), strict Western blot band criteria (IgM 2 of 3 within 30 days vs IgG 5 of 10), Babesia Maltese cross tetrads, Anaplasma/Ehrlichia morulae; and Multiplex syndromic PCR panels (BioFire FilmArray respiratory, GI, and meningitis/encephalitis panels), cycle threshold (Ct value) interpretation, and avoiding the asymptomatic shedding trap."
        ),
        "components": [
            "VOLUME_XX_INFECTIOUS_DISEASE_SEROLOGY_VIROLOGY_AND_MOLECULAR_DIAGNOSTICS.md",
            "LONGFORM_60MIN_PODCAST_EP814_INFECTIOUS_DISEASE_SEROLOGY_VIROLOGY_AND_PARASITOLOGY.md"
],
    },
    {
        "slug": "Bundle_15_Ep815_Blood_Banking_Immunohematology_and_Advanced_Hemostasis.md",
        "title": "Bundle 15 — Ep 815: Blood Banking, 11-Cell Rule-Outs, Daratumumab DTT, Rosner Index & VWD Multimers (All-In-One)",
        "prompt": (
            "Behind the curtain of the blood bank and advanced hemostasis lab: Type & Screen vs Type & Crossmatch (immediate-spin vs AHG vs electronic crossmatch); ABO discrepancies (Group I cold agglutinins, Group II A2 with anti-A1, Group III rouleaux, Bombay Oh phenotype); Rh D typing, weak D vs partial D RHD genotyping, RhIG prophylaxis and Kleihauer-Betke acid elution dosing calculation; 11-cell antibody rule-out panels (the 3x3 p=0.05 rule, dosage effects, and Ficin/Papain enzyme cleavage); Daratumumab (anti-CD38) panreactivity neutralized via 0.2 M Dithiothreitol (DTT) treatment of reagent RBCs (and Kell antigen destruction requiring K-negative blood); DAT/Coombs polyspecific vs monospecific (anti-IgG vs anti-C3d) and acid elution; aPTT mixing studies and the Rosner Index [(mix - normal) / patient * 100] with >12-15% inhibitor cutoff; Lupus Anticoagulant 3-step testing (dRVVT screen, mix, confirm ratio > 1.20); von Willebrand Disease (VWD) complete subtyping cascade (VWF:Ag, VWF:RCo or GP1bM, ratio < 0.7 for Type 2, Factor VIII binding, low-dose RIPA for 2B, and SDS-agarose multimer electrophoresis); HIT 4T score, PF4 ELISA, and 14C-Serotonin Release Assay SRA; and viscoelastic TEG/ROTEM parameters (R/CT, K/CFT, alpha angle, MA/MCF, LY30/ML, citrated kaolin vs heparinase, FIBTEM) guiding massive transfusion protocols."
        ),
        "components": [
            "VOLUME_XXI_IMMUNOHEMATOLOGY_BLOOD_BANKING_AND_ADVANCED_HEMOSTASIS.md",
            "LONGFORM_60MIN_PODCAST_EP815_BLOOD_BANKING_IMMUNOHEMATOLOGY_AND_ADVANCED_HEMOSTASIS.md"
],
    },
    {
        "slug": "Bundle_16_Ep816_Cytogenetics_Chromosomal_Microarrays_and_Long_Read_Genomics.md",
        "title": "Bundle 16 — Ep 816: Cytogenetics, 550-Band Karyotypes, Dual-Fusion FISH, SNP Arrays & Nanopore Pseudogenes (All-In-One)",
        "prompt": (
            "Behind the scenes of cytogenetics, chromosomal microarrays, and next-generation sequencing: specimen requirements (sodium heparin green top for viable cells, never EDTA or formalin), PHA T-cell stimulation, Colcemid mitotic arrest, hypotonic KCl swelling, Carnoy's fixative, G-banding (GTG) 400-550 band routine vs 700-850 prometaphase high-res, ISCN 2024 nomenclature rules (translocations, inversions, deletions); FISH probe architectures: dual-color dual-fusion (BCR-ABL1, PML-RARA), break-apart split probes (ALK, ROS1, EWSR1, MYC), locus-specific enumerators (HER2/ERBB2 with CEP17 ratio >= 2.0), centromeric CEP probes; MLPA and MS-MLPA methylation quantification for Prader-Willi/Angelman (15q11-q13 SNRPN) and Beckwith-Wiedemann (11p15 H19/IGF2); Chromosomal Microarray (aCGH vs SNP array) Log2 ratios and B-allele frequency (BAF) detecting CN-LOH, UPD, and consanguinity, plus microarray blind spots; Illumina NovaSeq X SBS sequencing-by-synthesis, library prep, target read depth (100x germline vs 500-1000x somatic), Phred Q30 accuracy, VAF, and ACMG/AMP 5-tier classification; and Long-Read Third-Generation Sequencing (Oxford Nanopore R10.4.1 flow cells and PacBio HiFi SMRT CCS) resolving clinical blind spots: homologous pseudogenes (CYP21A2 in CAH, SMN1 in SMA, PMS2 in Lynch), repeat expansions (C9orf72 in ALS, DMPK in DM1, FXN, FMR1), direct native 5mC and 5hmC profiling, and chromosome phasing."
        ),
        "components": [
            "VOLUME_XXII_CYTOGENETICS_CHROMOSOMAL_MICROARRAYS_AND_LONG_READ_GENOMICS.md",
            "LONGFORM_60MIN_PODCAST_EP816_CYTOGENETICS_CHROMOSOMAL_MICROARRAYS_AND_LONG_READ_GENOMICS.md"
],
    },
]


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
