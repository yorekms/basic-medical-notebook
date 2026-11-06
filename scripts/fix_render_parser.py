import pathlib

p = pathlib.Path(r"C:\Users\patel\.gemini\antigravity\scratch\Basic_Medical_Notebook\scripts\render_basic_medical_60min_tts.py")
text = p.read_text(encoding="utf-8")

# 1. Update regex
old_re = 'SPEAKER_LINE_RE = re.compile(r"^\\*\\*\\[?([^*\\\]:]+)\\]?:\\*\\*\\s*(.*)$")'
new_re = 'SPEAKER_LINE_RE = re.compile(r"^\\*\\*\\[?([^*\\\]:]+?)\\]?(?::\\*\\*|\\*\\*:)\\s*(.*)$")'

if old_re in text:
    text = text.replace(old_re, new_re)
    print("Replaced SPEAKER_LINE_RE successfully!")
else:
    print("Could not find old_re")

# 2. Update match condition
old_match = """        match = SPEAKER_LINE_RE.match(stripped)
        if match:
            flush()
            current_speaker = match.group(1).strip()"""

new_match = """        match = SPEAKER_LINE_RE.match(stripped)
        if match and match.group(1).strip() in SPEAKER_PROFILES:
            flush()
            current_speaker = match.group(1).strip()"""

if old_match in text:
    text = text.replace(old_match, new_match)
    print("Replaced match check successfully!")
else:
    print("Could not find old_match")

p.write_text(text, encoding="utf-8")
