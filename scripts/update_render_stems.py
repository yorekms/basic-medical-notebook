import pathlib

p = pathlib.Path(r"C:\Users\patel\.gemini\antigravity\scratch\Basic_Medical_Notebook\scripts\render_basic_medical_60min_tts.py")
text = p.read_text(encoding="utf-8")

old_stems = '''CLEAN_AUDIO_STEMS: Dict[str, str] = {
    "EP801": "EP801_Kidney_Donor_Gauntlet_mGFR_Litholink_and_Split_Scans",
    "EP802": "EP802_HLA_Typing_Luminex_Prozone_and_Living_Cell_Crossmatch",
    "EP803": "EP803_Eight_Colored_Tubes_Core_Chemistry_and_Immunoassay_Traps",
    "EP804": "EP804_Behind_the_Lead_Glass_and_the_Frozen_Section_Cryostat",
    "EP805": "EP805_The_Oncology_Workup_Tumor_Markers_Liquid_Biopsy_and_Theranostics",
    "EP806": "EP806_ICU_Red_Alert_Orders_Shock_Gaps_Ventilator_Curves_and_Coma_EEG",
    "EP807": "EP807_From_Womb_to_Heel_Stick_NIPT_Tandem_MS_Sweat_Chloride_and_Trio_Exomes",
    "EP808": "EP808_The_Jeopardy_Grandmaster_Tour_Microbiology_Fluid_Taps_and_Classic_Tests",
}'''

new_stems = '''CLEAN_AUDIO_STEMS: Dict[str, str] = {
    "EP801": "EP801_Kidney_Donor_Gauntlet_mGFR_Litholink_and_Split_Scans",
    "EP802": "EP802_HLA_Typing_Luminex_Prozone_and_Living_Cell_Crossmatch",
    "EP803": "EP803_Eight_Colored_Tubes_Core_Chemistry_and_Immunoassay_Traps",
    "EP804": "EP804_Behind_the_Lead_Glass_and_the_Frozen_Section_Cryostat",
    "EP805": "EP805_The_Oncology_Workup_Tumor_Markers_Liquid_Biopsy_and_Theranostics",
    "EP806": "EP806_ICU_Red_Alert_Orders_Shock_Gaps_Ventilator_Curves_and_Coma_EEG",
    "EP807": "EP807_From_Womb_to_Heel_Stick_NIPT_Tandem_MS_Sweat_Chloride_and_Trio_Exomes",
    "EP808": "EP808_The_Jeopardy_Grandmaster_Tour_Microbiology_Fluid_Taps_and_Classic_Tests",
    "EP809": "EP809_Cardiopulmonary_Diagnostics_Hemodynamics_and_Vascular_Medicine",
    "EP810": "EP810_Gastroenterology_Hepatology_and_Metabolic_Nutrition",
    "EP811": "EP811_Endocrinology_Dynamic_Testing_and_Neuroendocrine_Disorders",
    "EP812": "EP812_Preventable_Death_Longevity_and_Screening_Medicine",
    "EP813": "EP813_The_Neurodiagnostic_Vault_EEG_EMG_Evoked_Potentials_and_CSF",
    "EP814": "EP814_Infectious_Disease_Serology_Virology_and_Parasitology",
    "EP815": "EP815_Blood_Banking_Immunohematology_and_Advanced_Hemostasis",
    "EP816": "EP816_Cytogenetics_Chromosomal_Microarrays_and_Long_Read_Genomics",
}'''

if old_stems in text:
    text = text.replace(old_stems, new_stems)
    p.write_text(text, encoding="utf-8")
    print("Updated CLEAN_AUDIO_STEMS successfully!")
else:
    print("Could not find old_stems block.")
