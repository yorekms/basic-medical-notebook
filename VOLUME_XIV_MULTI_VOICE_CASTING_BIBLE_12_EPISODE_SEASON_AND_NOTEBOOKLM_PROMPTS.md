# Volume XIV: Multi-Voice Casting Bible, 12-Episode 60-Minute Season Architecture & Copy-Paste NotebookLM Steering Prompts

> **Design Philosophy**: Every episode of ***Behind the Curtain: How Medical Diagnostics Actually Work*** pairs **three distinct studio voices** in a fast-moving, zero-jargon-left-unexplained narrative arc: **(1) The Ordering Physician**, **(2) The Curious Scientist-Patient / Devil's Advocate**, and **(3) The Behind-the-Curtain Laboratory Technologist, Histotechnologist, or Imaging Specialist** who actually touches the blood tube, bone marrow aspirate, tissue cassette, or scanner console after the clinic door closes.

---

## 1. Zero-Overlap 21-Voice Studio Roster (`Cast Modes A–G`)

All **8 unabridged 60-minute marathon scripts (`EP801`–`EP808`)** map cleanly with **zero voice collisions** to both **`gemini-3.8-flash-tts`** and zero-API-key neural **`edge-tts`** (`scripts/render_basic_medical_60min_tts.py`):

| Cast Mode | Episodes | Character Name | Dramatic Role | `gemini-3.8-flash-tts` Voice | `edge-tts` Neural Voice |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **Mode A** | `EP801`, `EP802` | **Dr. Rachel Halpern** | Transplant Nephrologist & Living Donor Medical Director | `Sulafat` (*Warm, incisive*) | `en-US-AvaMultilingualNeural` |
| **Mode A** | `EP801`, `EP802` | **Prof. Evan Reid** | PhD Biophysicist & Prospective Living Kidney Donor | `Sadaltager` (*Knowledgeable baritone*) | `en-US-AndrewMultilingualNeural` |
| **Mode A** | `EP801`, `EP802` | **Carlos Mendez** | Lead `LC-MS/MS`, Nuclear Clearance & `HLA` Specialist (`CHS`) | `Orus` (*Firm, hands-on bench pro*) | `en-US-BrianMultilingualNeural` |
| **Mode B** | `EP803`, `EP809` | **Dr. Nathan Sterling** | Director of Clinical Chemistry, Toxicology & Core Lab | `Charon` (*Resonant, authoritative*) | `en-US-ChristopherNeural` |
| **Mode B** | `EP803`, `EP809` | **Dr. Maya Lin** | Internal Medicine Diagnostician & Patient Advocate | `Zephyr` (*Bright, probing*) | `en-US-EmmaMultilingualNeural` |
| **Mode B** | `EP803`, `EP809` | **Denise Okafor** | Lead Core-Lab `TLA`, Hematology & Immunoassay Scientist (`MLS`) | `Autonoe` (*Crisp, energetic*) | `en-GB-SoniaNeural` |
| **Mode E** | `EP804`, `EP810` | **Dr. Victor Chen** | Diagnostic Radiologist & Nuclear Medicine Physician | `Iapetus` (*Clear, vivid*) | `en-US-EricNeural` |
| **Mode E** | `EP804`, `EP810` | **Dr. Elena Rostova** | Surgical Pathologist & Invasive Cardiopulmonary Specialist | `Erinome` (*Articulate, precise*) | `en-US-MichelleNeural` |
| **Mode E** | `EP804`, `EP810` | **Marcus Bell** | Chief `CT/MRI` Technologist & Frozen-Section Histotech (`HTL`) | `Fenrir` (*Grounded, tactile*) | `en-US-RogerNeural` |
| **Mode C** | `EP805`, `EP811` | **Dr. Julian Vance** | Medical Oncologist & Precision Cancer Genomics Director | `Rasalgethi` (*Measured gravitas*) | `en-GB-RyanNeural` |
| **Mode C** | `EP805`, `EP811` | **Dr. Clara Sterling** | Cancer Biologist & Devil's-Advocate Questioner | `Aoede` (*Quick-witted, warm*) | `en-US-JennyNeural` |
| **Mode C** | `EP805`, `EP811` | **Tariq Al-Mansoor** | Lead 10-Color Flow Cytometry, `NGS/FISH` & Theranostics Tech | `Algenib` (*Authoritative bench lead*) | `en-US-SteffanNeural` |
| **Mode D** | `EP806` | **Dr. Kendra Brooks** | Shock-Trauma & Pulmonary/Critical Care Intensivist | `Kore` (*Commanding, calm under fire*) | `en-US-AriaNeural` |
| **Mode D** | `EP806` | **Sam Callahan** | Emergency Medicine Physician & Quantitative Skeptic | `Achird` (*Direct, grounded*) | `en-US-GuyNeural` |
| **Mode D** | `EP806` | **Hannah Lindqvist** | Lead STAT Blood-Gas, `TEG/ROTEM` & Coma `cEEG` Specialist | `Vindemiatrix` (*Composed, precise*) | `en-GB-LibbyNeural` |
| **Mode F** | `EP807` | **Dr. Priya Nair** | Pediatrician, Neonatologist & Biochemical Medical Geneticist | `Despina` (*Warm, lucid*) | `en-IN-NeerjaNeural` |
| **Mode F** | `EP807` | **Leo Vance** | New-Parent Scientist & Diagnostic Sleuth | `Puck` (*Upbeat, curious*) | `en-AU-WilliamNeural` |
| **Mode F** | `EP807` | **Grace Takahashi** | State Newborn-Screening `MS/MS`, Sweat-`Cl` & Trio-Genome Tech | `Leda` (*Clear, meticulous*) | `en-US-AnaNeural` |
| **Mode G** | `EP808`, `EP812` | **Dr. Arthur Pendelton** | Infectious Disease, Rheum & *Jeopardy!* Diagnostic Grandmaster | `Gacrux` (*Encyclopedic, witty*) | `en-GB-ThomasNeural` |
| **Mode G** | `EP808`, `EP812` | **Zoe Patel** | Chief Medical Resident & Diagnostic Challenger | `Callirrhoe` (*Sharp, lively*) | `en-AU-NatashaNeural` |
| **Mode G** | `EP808`, `EP812` | **Matteo Rossi** | Veteran `MALDI-TOF` Microbiologist & Polarized-Light Microscopist | `Schedar` (*Seasoned bench craftsman*) | `en-IE-ConnorNeural` |

---

## 2. Copy-Paste Google NotebookLM `"Longer"` Audio Overview Steering Prompts

When generating podcasts inside **Google NotebookLM (`notebook.google.com`)**:
1. Select **either** the matching **One-Click Episode Bundle** inside `One_Click_Episode_Bundles_For_NotebookLM/` **or** the listed individual Google Docs from `Google_Docs_For_NotebookLM_Picker/`.
2. Click **Audio Overview -> Customize -> Longer**, and paste the prompt below verbatim!

---

### Episode 801 — *Puzzled in the Donor Chair: Measured Iohexol GFR, 24-Hour Litholink Stone Jugs & Split Nuclear Renal Scans*
- **Scripted File**: `LONGFORM_60MIN_PODCAST_EP801_KIDNEY_DONOR_GAUNTLET_MGFR_24HR_URINE_AND_SPLIT_SCANS.md`
- **Primary Sources**: `VOLUME_I` + `DOCS_ARCHIVE_01`
- **NotebookLM `"Longer"` Prompt**:
```text
Create a deep, longest-format behind-the-curtain medical diagnostics podcast starting from a real dilemma: why even a scientifically trained living kidney donor candidate is mystified by the 45 tests ordered before donating a kidney. Walk step-by-step through WHY serum creatinine and eGFR lie (Jaffe picrate vs enzymatic creatininase, OCT2/MATE1 tubular secretion blocked by trimethoprim, muscle mass vs Cystatin C), and what happens behind the laboratory curtain during Measured GFR (weighing the Iohexol syringe to a milligram, contralateral timed draws at 120/180/240 minutes, LC-MS/MS endo/exo peaks, and the Brochner-Mortensen quadratic correction). Unpack the 24-hour urine jug (why void #1 is discarded, catching under-collection via 20-25 mg/kg/day creatinine, UACR vs UPCR, and Litholink EQUIL2 stone supersaturation), milking the 99Mo/99mTc generator at 5 AM for MAG3 split renal function, 4-phase donor CT angiography (why surgeons prefer the 7-cm left renal vein unless anatomy or split function dictates keeping the better kidney), OGTT, APOL1 G1/G2 alleles, and post-donation adaptive hyperfiltration.
```

### Episode 802 — *Yellow-Top Living Lymphocytes: 11-Locus HLA NGS, Luminex Single-Antigen Beads, The C1 Prozone Trap & Physical Crossmatching*
- **Scripted File**: `LONGFORM_60MIN_PODCAST_EP802_HLA_TYPING_LUMINEX_PROZONE_AND_LIVING_CELL_CROSSMATCH.md`
- **Primary Sources**: `VOLUME_I` + `DOCS_ARCHIVE_02` + `DOCS_ARCHIVE_03`
- **NotebookLM `"Longer"` Prompt**:
```text
Create an exhaustive, longest-format behind-the-curtain transplant immunology and laboratory medicine podcast answering why phlebotomy draws 6 room-temperature pale-yellow ACD tubes and green sodium heparin tubes on an organ donor. Follow those living T and B lymphocytes through Ficoll-Hypaque isolation, ABO forward/reverse typing plus Dolichos biflorus lectin A2 subtyping (enabling A2-into-O/B transplants!), and 11-locus long-range NGS HLA typing with eplet and PIRCHE-II epitope matching. Go inside the dual-laser Luminex Single-Antigen Bead analyzer to explain Mean Fluorescence Intensity (MFI) and the life-or-death C1 Complement Prozone artifact—where a lethal 23,000 MFI donor-specific antibody reads a falsely negative 420 MFI until EDTA, DTT, or 1:16 dilution strips away C1q steric blockade! Contrast Paul Terasaki's 1964 rabbit-complement CDC microdroplet tray against 3-color Flow Cytometric Crossmatching (and why 37C Pronase shaving of B-cell CD32 Fc receptors prevents false positives), plus window-period HIV/HBV/HCV NAT, occult HBV cccDNA, and 4-tube QuantiFERON-TB stimulation.
```

### Episode 803 — *Why Eight Colored Tubes in Strict Order? Core Chemistry, ISE Pseudohyponatremia, Biotin Sabotage & Tandem Mass Spec*
- **Scripted File**: `LONGFORM_60MIN_PODCAST_EP803_EIGHT_COLORED_TUBES_CORE_CHEMISTRY_AND_IMMUNOASSAY_TRAPS.md`
- **Primary Sources**: `VOLUME_II` + `VOLUME_III` + `VOLUME_IV`
- **NotebookLM `"Longer"` Prompt**:
```text
Create an enthralling, longest-format behind-the-curtain tour of everyday blood draws, Vacutainer cap chemistry, hematology lasers, Ruthenium immunoassays, and clinical LC-MS/MS. Explain tourniquet hemoconcentration, fist-pumping pseudohyperkalemia, and the CLSI Order of Draw: SPS blood culture resins, why underfilling a 9:1 light-blue citrate tube invents a fake bleeding disorder, how Gold SST micronized silica activates Factor XII while thixotropic gel liquefies at 1,500 x g, why K2-EDTA cross-contamination creates K+ of 11, Ca2+ of 3, and zero Alkaline Phosphatase (stripping catalytic zinc!), and EDTA platelet clumping vs cold agglutinins on Coulter/Sysmex counters. Reveal why Core-Lab Indirect ISE reports a fake Na+ of 121 in hypertriglyceridemia/myeloma while undiluted Blood-Gas Direct ISE reads 140, 340-nm NADH coupled enzyme kinetics, the Four Immunoassay Saboteurs (High-Dose Biotin faking Graves' disease and masking heart-attack Troponin, Giant Prolactinoma Hook Effect, Phantom hCG heterophile antibodies, and PEG macroprolactin), BNP vs NT-proBNP on Entresto, HbA1c traps, and why Triple-Quadrupole LC-MS/MS conquered steroids and urine drug screens.
```

### Episode 804 — *Behind the Lead Glass & The `-22°C` Cryostat: CT Hounsfield Physics, 3T MRI Pulse Sequences, 5-Day FFPE Biopsies & Invasive Physiology*
- **Scripted File**: `LONGFORM_60MIN_PODCAST_EP804_BEHIND_THE_LEAD_GLASS_AND_THE_FROZEN_SECTION_CRYOSTAT.md`
- **Primary Sources**: `VOLUME_VII` + `VOLUME_VIII`
- **NotebookLM `"Longer"` Prompt**:
```text
Create a riveting, longest-format behind-the-curtain exploration of diagnostic radiology, nuclear PET, surgical pathology biopsies, and bedside physiological procedures. Step behind the CT lead glass to unpack spinning tungsten anodes, Hounsfield linear attenuation units (-1000 air, -70 fat proving benign adrenal adenomas, +70 acute blood, +1000 bone), iodine 33.2-keV K-edge dual-energy CT, bolus-tracking ROI timing (and Valsalva fake pulmonary embolisms), and busting the contrast-nephropathy myth when eGFR >= 30. Demystify Doppler <=60-degree angle physics, Zone IV 4.2-Kelvin superconducting 3T MRI magnets (T1, T2, FLAIR CSF-nulling, and 6-minute acute stroke DWI/ADC Brownian water trapping), and 511-keV positron coincidence FDG-PET. Then answer why routine biopsies take 5 days (grossing ink -> 10% formalin -> ethanol -> xylene clearing -> 60C paraffin -> 4-um microtome -> H&E + 98C HIER DAB immunohistochemistry, and which specimens formalin ruins!) vs 15-minute intraoperative -22C cryostat frozen sections, plus Cath-Lab FFR, PFT Body-Box/DLCO, NBI colonoscopy, and EMG/NCS.
```

### Episode 805 — *Decoding the Cancer Order Sheet: Tumor Marker Traps, 10-Color Leukemia Flow, Solid-Tumor RNA/DNA NGS, Liquid Biopsy ctDNA & Theranostic PET*
- **Scripted File**: `LONGFORM_60MIN_PODCAST_EP805_THE_ONCOLOGY_WORKUP_TUMOR_MARKERS_LIQUID_BIOPSY_MARROW_FLOW_AND_THERANOSTIC_PET.md`
- **Primary Sources**: `VOLUME_IX` + `VOLUME_VIII` + `DOCS_ARCHIVE_04`
- **NotebookLM `"Longer"` Prompt**:
```text
Create an authoritative, longest-format behind-the-curtain podcast covering every diagnostic test ordered in modern oncology and hematology. Explain why serum tumor markers rarely work for population screening yet guide cancer kinetics—unpacking Total vs %Free PSA (finasteride halving rule + PI-RADS fusion biopsy), why 7% of humans are genetically Lewis-negative (FUT3) and read zero CA 19-9 even with metastatic pancreatic cancer while gallstones spike it to 5,000, AFP/hCG post-orchiectomy half-life clocks, anti-thyroglobulin interference solved by LC-MS/MS, and why Rasburicase tumor-lysis blood must travel on ice. Walk through posterior iliac crest Bone Marrow Aspirate + Core ("dry tap" myelofibrosis), 10-color flow cytometry (2-hour APL Auer-rod emergency & kappa/lambda B-cell clonality), FISH, and 10^-6 clonoSEQ MRD. Then go inside solid-tumor DNA + anchored-multiplex RNA fusion NGS (MSI-High, TMB, HRD scars, VAF ~50% germline clues), Streck-tube UMI Liquid Biopsy ctDNA (and the aging-blood CHIP impostor!), stereotactic BI-RADS mammography, dual-tracer sentinel nodes, and Ga-68/Lu-177 PSMA & DOTATATE theranostics.
```

### Episode 806 — *ICU Red-Alert Orders: Stewart Strong Ions, Shock Venous Gaps, Ventilator Plateau Curves, Trauma TEG Cups, VExUS POCUS & Coma Neuro-Telemetry*
- **Scripted File**: `LONGFORM_60MIN_PODCAST_EP806_ICU_RED_ALERT_ORDERS_SHOCK_GAPS_VENTILATOR_CURVES_TEG_POCUS_AND_COMA_EEG.md`
- **Primary Sources**: `VOLUME_X` + `VOLUME_II` + `VOLUME_III`
- **NotebookLM `"Longer"` Prompt**:
```text
Create a high-stakes, longest-format behind-the-curtain podcast decoding every STAT order in the Shock-Trauma ICU and Emergency Department. Start at 3 AM with Arterial Blood Gases and 128-wavelength Co-Oximetry (why finger pulse oximeters read 99% in lethal carbon monoxide poisoning), Winters' formula, the Delta-Delta ratio catching triple acid-base disorders, and Peter Stewart's Strong Ion Difference proving why 4 liters of 0.9% "Normal" Saline (SID = 0) chemically forces hyperchloremic acidosis—plus the Osmolal Gap and Point-of-Care vs Core-Lab Lactate Gap unmasking antifreeze poisoning! Unpack Type A vs epinephrine Type B lactate, Fick SvO2/ScvO2 (why SvO2 of 85% in sepsis or cyanide is terrifying), and the Pv-aCO2 > 6 mmHg microvascular stagnation gap. Treat the ICU ventilator as a biophysics analyzer: 0.5-sec End-Inspiratory Hold (PIP vs Pplat & Driving Pressure < 15), End-Expiratory Hold Auto-PEEP, capnography, and RSBI < 105. Finish with whole-blood TEG/ROTEM trauma resuscitation, HIT 14C-SRA, eFAST/RUSH/VExUS venous congestion Doppler, ICP P2>P1 herniation waves, continuous coma cEEG, and 72-hour SSEP N20 post-arrest prognostication.
```

### Episode 807 — *From Womb to Heel-Stick: Prenatal cfDNA Mosaicism, Five Dried Blood Spots, Tandem Mass Spec, Pilocarpine Sweat Chloride & 48-Hour NICU Trio Genomes*
- **Scripted File**: `LONGFORM_60MIN_PODCAST_EP807_FROM_WOMB_TO_HEEL_STICK_NIPT_TANDEM_MS_SWEAT_CHLORIDE_AND_TRIO_EXOMES.md`
- **Primary Sources**: `VOLUME_XI`
- **NotebookLM `"Longer"` Prompt**:
```text
Create a deeply illuminating, longest-format behind-the-curtain podcast tracing every diagnostic test from pregnancy through newborn nursery, pediatrics, and rapid clinical genomics. Start before birth with Dennis Lo's prenatal cfDNA (NIPT): why "fetal" cfDNA is actually 143-bp placental trophoblast DNA, why maternal obesity drops Fetal Fraction below 4%, and why Confined Placental Mosaicism means positive NIPT MUST be confirmed by amniocentesis—plus noninvasive MCA Doppler for fetal anemia and Kleihauer-Betke rose-pink HbF cells vs flow cytometry for RhoGAM dosing. Go inside the 2 AM State Newborn Screening Lab to watch five 3.2-mm paper punches from a 24-48 hour lateral heel-stick run through Electrospray Tandem Mass Spectrometry in 90 seconds (PKU, Maple Syrup Urine Disease, C8 Octanoylcarnitine MCAD deficiency), qPCR for TREC = 0 "Bubble Boy" SCID and SMN1 SMA (enabling week-1 Zolgensma gene therapy!), CCHD right-hand/foot oximetry, OAE vs NICU AABR hearing, Pilocarpine Iontophoresis Sweat Chloride for Cystic Fibrosis, capillary-vs-venous Lead, pyloric/intussusception ultrasound, SNP Microarray UPD, and 48-hour NICU Rapid Trio Whole-Genome Sequencing.
```

### Episode 808 — *The Jeopardy! Grandmaster Diagnostic Tour: 90-Second MALDI-TOF Lasers, Dipstick Lies, Polarized Crystal Physics, Crithidia DNA & Classic Named Tests*
- **Scripted File**: `LONGFORM_60MIN_PODCAST_EP808_THE_JEOPARDY_GRANDMASTER_TOUR_MICROBIOLOGY_FLUID_TAPS_AUTOIMMUNITY_AND_CLASSIC_TESTS.md`
- **Primary Sources**: `VOLUME_V` + `VOLUME_VI` + `VOLUME_XII` + `VOLUME_XIII`
- **NotebookLM `"Longer"` Prompt**:
```text
Create an exhilarating, longest-format championship tour through microbiology, urinalysis, sterile body-fluid taps, rheumatology, subspecialty testing, and classic "Jeopardy! $2,000 Clue" named medical tests! Open behind the microbiology biosafety cabinet: why 40-60 mL blood volume and antibiotic-binding resins matter in sepsis, why Chocolate Agar heats sheep blood to 80C to kill NADase, how 337-nm MALDI-TOF lasers weigh ribosomal proteins in 90 seconds (yet confuse Shigella with E. coli!), busting the raw MIC comparison fallacy, inducible D-zone clindamycin resistance, and 3.32-cycle TaqMan qPCR math. Expose the 3 famous urine dipstick blindspots (Bence Jones myeloma light chains, beta-hydroxybutyrate in early DKA, and Vitamin C false negatives), CSF Tube 1-vs-4 spectrophotometric 450-nm xanthochromia, Light's Criteria, ascitic SAAG >= 1.1, and 530-nm red-plate polarized crystal physics (Gout yellow parallel vs Pseudogout blue parallel!). Tour HEp-2 ANA (benign DFS70 vs Centromere), Crithidia kinetoplast dsDNA, 13C-urea breath, SFEMG jitter, RT-QuIC prions, Michel's skin DIF, Ara h 2 peanut IgE, FLAER/EMA/DHR flow tests, and a rapid-fire Jeopardy! Named-Test Lightning Finale!
```

---

## 3. Bonus Modular Expansion Blueprints (`Episodes 809–812`) for NotebookLM Custom Runs

Want four more focused hour-long episodes directly inside NotebookLM? Combine the existing Google Docs in `Google_Docs_For_NotebookLM_Picker/` with these prompts:
- **Episode 809 (*Cardiology & Pulmonary Diagnostic Masterclass*)**: Select `VOLUME_IV` + `VOLUME_VII` + `VOLUME_VIII` — Deep dive on `12-lead ECG` vector physics & lead-reversal traps, `hs-cTnI/T` `0/1h` deltas, Stress Echo vs `99mTc-Sestamibi` coronary steal vs Cardiac `CTA` (`FFR-CT`) vs Cath-Lab pressure-wire `FFR/iFR` + `IVUS/OCT`, `Swan-Ganz` thermodilution vs Fick, and Body-Box Plethysmography + `DLCO`.
- **Episode 810 (*Gastroenterology, Hepatology & Nutrition Diagnostics*)**: Select `VOLUME_II` + `VOLUME_VI` + `VOLUME_VIII` + `VOLUME_XII` — Liver injury patterns (`R-factor`, `P5P` `AST:ALT`, `Bilirubin:ALP > 2` Wilson's, `FibroScan` elastography, `SAAG` paracentesis), `13C-Urea` & `H2/CH4` breath physics, `tTG-IgA` Celiac traps, Fecal Calprotectin/Elastase/Osmotic Gap, Chicago v4.0 High-Res Manometry, and `NBI` Endoscopy.
- **Episode 811 (*Endocrinology's Dynamic Provocation & Mass-Spec Revolution*)**: Select `VOLUME_IV` + `VOLUME_XI` + `VOLUME_XII` — Why static hormone levels fail in pulsatile axes: Overnight `1-mg` Dexamethasone (with `LC-MS/MS` serum dex check!) -> Late-Night Salivary Cortisol -> Inferior Petrosal Sinus Sampling; Cosyntropin + `17-OHP`; Seated Aldosterone-Renin Ratio -> **Adrenal Vein Sampling** (`Cortisol Selectivity Index`); Supine Plasma Metanephrines; `Copeptin` Water Deprivation; and Equilibrium Dialysis `LC-MS/MS`.
- **Episode 812 (*Preventable Death, Longevity & Evidence-Based Screening Architecture*)**: Select `DOCS_ARCHIVE_04` + `VOLUME_IV` + `VOLUME_IX` + `VOLUME_XIII` — Bayes' theorem screening math (`Lead-Time` & `Length-Time` bias), `ApoB` + once-in-a-lifetime `Lp(a)` + `CAC` Coronary Calcium Agatston scoring vs `CT` Angiography, Low-Dose Lung `CT`, Colonoscopy vs `mt-sDNA` (`Cologuard`) vs `FIT`, `HPV` Cervical primary screening, `DEXA` trabecular bone scores, and why whole-body "executive" scans backfire without pre-test calibration.
