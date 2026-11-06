#!/usr/bin/env python3
import json
import pathlib

src = pathlib.Path(r"C:\Users\patel\.gemini\antigravity\scratch\Basic_Medical_Notebook\scripts\build_all_16_bundles.py").read_text(encoding="utf-8")
target = pathlib.Path(r"C:\Users\patel\.gemini\antigravity\scratch\Basic_Medical_Notebook\scripts\build_bundles_and_sync_drive.py").read_text(encoding="utf-8")

manifest_p = pathlib.Path(r"C:\Users\patel\.gemini\antigravity\scratch\Podcast_Automation_Suite\notebooks_manifest.json")
with open(manifest_p, "r", encoding="utf-8") as f:
    manifest = json.load(f)

episodes = {ep["ep"]: ep for ep in manifest["notebooks"]["basic_medical"]["episodes"]}

idx_start = src.find("bundle_map = {")
idx_end = src.find("root = pathlib.Path")
bundle_map_code = src[idx_start:idx_end].strip()

exec_env = {}
exec(bundle_map_code, exec_env)
bundle_map = exec_env["bundle_map"]

spec_start = target.find("BUNDLE_SPECS = [")
spec_end = target.find("def run_gdrive")

new_specs = []
for ep_num in sorted(bundle_map.keys()):
    slug, title, comps = bundle_map[ep_num]
    prompt = episodes[ep_num]["prompt"].replace('"', '\\"')
    entry = f"""    {{
        "slug": "{slug}",
        "title": "{title}",
        "prompt": (
            "{prompt}"
        ),
        "components": {json.dumps(comps, indent=12)},
    }},"""
    new_specs.append(entry)

new_bundle_specs_str = "BUNDLE_SPECS = [\n" + "\n".join(new_specs) + "\n]\n\n\n"
new_target = target[:spec_start] + new_bundle_specs_str + target[spec_end:]

pathlib.Path(r"C:\Users\patel\.gemini\antigravity\scratch\Basic_Medical_Notebook\scripts\build_bundles_and_sync_drive.py").write_text(new_target, encoding="utf-8")
print("Updated build_bundles_and_sync_drive.py successfully with all 16 BUNDLE_SPECS!")
